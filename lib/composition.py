"""Composition and class-group analogues for Kingdom Come / QGA Chapter 8.

Pedagogical **Model** lifts of Gauss composition to flux topographs / flywheels
on the gauged Hopf lattice. Not claimed to be classical composition (Open Problem 6).
"""

from __future__ import annotations

from typing import Literal

import numpy as np

from .flux_topograph import (
    FluxTopograph,
    build_flux_topograph,
    class_number_analogue as topograph_class_number,
    classify_topograph_type,
    equivalence_distance,
    magic_island_score,
    reduced_representative,
)
from .hopf_lattice import q_mult, q_normalize

Array = np.ndarray
ComposeMethod = Literal["value_sum", "value_product", "point_mult", "value_bilinear"]


def compose_flywheels(
    topo_a: FluxTopograph,
    topo_b: FluxTopograph,
    *,
    method: ComposeMethod = "value_sum",
    functional: str | None = None,
) -> FluxTopograph:
    """Compose two flux topographs / flywheels (Model candidate).

    Methods
    -------
    value_sum :
        Pointwise average of values on a shared vertex index set.
    value_product :
        Pointwise product of values (normalized by max abs).
    value_bilinear :
        (V_a + V_b + V_a * V_b) / 3 — soft bilinear blend.
    point_mult :
        Quaternion multiply corresponding points, then recompute functional.

    Requires equal number of points (same discrete lattice sample).
    """
    a = np.asarray(topo_a.points, dtype=float)
    b = np.asarray(topo_b.points, dtype=float)
    if len(a) != len(b):
        raise ValueError("compose_flywheels requires equal-length point sets")

    edges = list(topo_a.edges) if topo_a.edges else list(topo_b.edges)
    fname = functional or topo_a.functional or "hopf_height"

    if method == "point_mult":
        pts = np.stack(
            [q_normalize(q_mult(a[i], b[i])) for i in range(len(a))],
            axis=0,
        )
        if fname in ("norm", "hopf_y1", "hopf_height", "phase", "index_wave"):
            return build_flux_topograph(pts, edges=edges, functional=fname)  # type: ignore[arg-type]
        return FluxTopograph(
            points=pts,
            values=0.5 * (topo_a.values + topo_b.values),
            edges=edges,
            functional=str(fname),
            meta={"compose_method": method, "parents": (topo_a.functional, topo_b.functional)},
        )

    va = np.asarray(topo_a.values, dtype=float)
    vb = np.asarray(topo_b.values, dtype=float)
    if method == "value_sum":
        values = 0.5 * (va + vb)
    elif method == "value_product":
        values = va * vb
        m = np.max(np.abs(values)) + 1e-12
        values = values / m
    elif method == "value_bilinear":
        values = (va + vb + va * vb) / 3.0
    else:
        raise ValueError(f"unknown method: {method}")

    # points: average then renorm (shared geometry)
    pts = np.stack(
        [q_normalize(0.5 * (a[i] + b[i])) for i in range(len(a))],
        axis=0,
    )
    return FluxTopograph(
        points=pts,
        values=values,
        edges=edges,
        functional=f"compose({method})",
        meta={
            "compose_method": method,
            "parents": (topo_a.functional, topo_b.functional),
            "source_functional": fname,
        },
    )


# Alias used in prose
compose_topographs = compose_flywheels


def reduce_composition(
    topo: FluxTopograph,
    *,
    gauge_sequences=None,
) -> dict:
    """Reduce a composed topograph and return classification + island score."""
    rep, meta = reduced_representative(topo, gauge_sequences=gauge_sequences)
    clf = classify_topograph_type(rep, gauge_sequences=gauge_sequences)
    return {
        "topograph": rep,
        "classification": clf,
        "reduction_meta": meta,
        "magic_island_score": magic_island_score(rep, gauge_sequences=gauge_sequences),
    }


def composition_table(
    reduced_set: list[FluxTopograph],
    *,
    method: ComposeMethod = "value_sum",
    dedup_tol: float = 0.05,
) -> dict:
    """Build an n×n composition table of class indices (Model).

    Each entry (i,j) is the index of the reduced class nearest to
    reduce(compose(class_i, class_j)), or -1 if no match within tol.
    """
    n = len(reduced_set)
    table = np.full((n, n), -1, dtype=int)
    details: list[dict] = []
    for i in range(n):
        for j in range(n):
            composed = compose_flywheels(reduced_set[i], reduced_set[j], method=method)
            reduced = reduce_composition(composed)["topograph"]
            best_k = -1
            best_d = float("inf")
            for k, rep in enumerate(reduced_set):
                d = equivalence_distance(reduced, rep)["combined"]
                if d < best_d:
                    best_d = d
                    best_k = k
            if best_d <= dedup_tol:
                table[i, j] = best_k
            else:
                # append new class? for table we mark -1 and record distance
                table[i, j] = -1
            details.append({"i": i, "j": j, "class": int(table[i, j]), "distance": best_d})
    return {
        "table": table,
        "order": n,
        "method": method,
        "dedup_tol": dedup_tol,
        "details": details,
        "closure_fraction": float(np.mean(table >= 0)) if n else 0.0,
    }


def is_associative_up_to_equivalence(
    reduced_set: list[FluxTopograph],
    *,
    method: ComposeMethod = "value_sum",
    samples: int = 20,
    tol: float = 0.08,
    seed: int = 0,
) -> dict:
    """Estimate associativity of composition on a small set (OP6 diagnostic).

    Samples triples (a,b,c) and compares (a*b)*c vs a*(b*c) via
    ``equivalence_distance`` after reduction.
    """
    n = len(reduced_set)
    if n == 0:
        return {"associativity_score": float("nan"), "n_tests": 0, "n_pass": 0}
    rng = np.random.default_rng(seed)
    n_tests = min(samples, max(1, n**3))
    n_pass = 0
    distances = []
    for _ in range(n_tests):
        i, j, k = (int(rng.integers(0, n)) for _ in range(3))
        a, b, c = reduced_set[i], reduced_set[j], reduced_set[k]
        ab = compose_flywheels(a, b, method=method)
        left = reduce_composition(compose_flywheels(ab, c, method=method))["topograph"]
        bc = compose_flywheels(b, c, method=method)
        right = reduce_composition(compose_flywheels(a, bc, method=method))["topograph"]
        d = equivalence_distance(left, right)["combined"]
        distances.append(d)
        if d <= tol:
            n_pass += 1
    return {
        "associativity_score": float(n_pass / n_tests) if n_tests else float("nan"),
        "n_tests": n_tests,
        "n_pass": n_pass,
        "mean_distance": float(np.mean(distances)) if distances else float("nan"),
        "tol": tol,
        "method": method,
    }


def class_group_analogue(
    reduced_set: list[FluxTopograph] | FluxTopograph,
    *,
    method: ComposeMethod = "value_sum",
    dedup_tol: float = 0.05,
    samples: int = 12,
) -> dict:
    """Build a class-group analogue from a seed topograph or reduced set.

    If a single topograph is passed, uses Chapter 6 ``class_number_analogue``
    to generate an initial reduced set, then builds a composition table.
    """
    if isinstance(reduced_set, FluxTopograph):
        cn = topograph_class_number(reduced_set, dedup_tol=dedup_tol)
        reps = [r["topograph"] for r in cn["reduced"]]
        base_order = cn["class_number_analogue"]
        by_type = cn["by_type"]
    else:
        reps = list(reduced_set)
        base_order = len(reps)
        by_type = {}
        for r in reps:
            t = classify_topograph_type(r)["type"]
            by_type[t] = by_type.get(t, 0) + 1

    if not reps:
        return {
            "order": 0,
            "structure": "trivial",
            "table": None,
            "associativity": {},
            "by_type": {},
            "closure_fraction": 0.0,
        }

    table = composition_table(reps, method=method, dedup_tol=dedup_tol)
    assoc = is_associative_up_to_equivalence(
        reps, method=method, samples=samples, tol=max(dedup_tol, 0.08)
    )

    # crude structure hint
    if table["closure_fraction"] >= 0.95 and assoc["associativity_score"] >= 0.8:
        structure = f"approx_group_order_{len(reps)}"
    elif table["closure_fraction"] >= 0.5:
        structure = "partial_magma"
    else:
        structure = "open_or_non_closed"

    return {
        "order": len(reps),
        "structure": structure,
        "by_type": by_type,
        "table": table["table"],
        "closure_fraction": table["closure_fraction"],
        "associativity": assoc,
        "method": method,
        "dedup_tol": dedup_tol,
        "base_order_hint": base_order,
        "representatives": reps,
    }


def identity_candidate(topo: FluxTopograph) -> FluxTopograph:
    """Return a near-identity topograph on the same points (flat values)."""
    return FluxTopograph(
        points=topo.points.copy(),
        values=np.zeros(len(topo.values)),
        edges=list(topo.edges),
        functional="identity_flat",
        meta={"role": "identity_candidate"},
    )
