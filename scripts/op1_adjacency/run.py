#!/usr/bin/env python3
"""OP1 adjacency harness: fiber coincidence and gauge keep-rate.

Software facts on the candidate graph in ``lib.hopf_lattice``. Does not
resolve OP1. Does not replace ``candidate_adjacency``.

``--dump-graph`` writes ``<stem>_graph.json`` (kind ``qga_adjacency_graph_v1``)
beside the OP1 row. structure_group witness only; refused for candidate.
Not ``export_fiber_curves``.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from importlib.metadata import version
from pathlib import Path
from typing import Any, Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flux_hopf_lib.hopf.fibration import hopf_map as lib_hopf_map
from flux_hopf_lib.quaternion.hurwitz import HURWITZ_UNITS
from lib.hopf_lattice import (
    adjacency_equivariance_score,
    apply_gauge_step,
    candidate_adjacency,
    hopf_map,
    hopf_project_points,
    nearest_index_map,
    q_mult,
    q_normalize,
    sample_angle_lattice,
    sample_structure_group_fiber,
    stereographic,
    structure_group_adjacency,
    hopf_fiber_clusters,
    consecutive_structure_group_along,
    bases_are_octahedron_poles,
)

I_UNIT = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
SCHEMA = "op1_adjacency_v1"
PRESETS_PATH = Path(__file__).resolve().parent / "presets.yaml"

AXIS_NAMES = {
    (1.0, 0.0, 0.0, 0.0): "1",
    (-1.0, 0.0, 0.0, 0.0): "-1",
    (0.0, 1.0, 0.0, 0.0): "i",
    (0.0, -1.0, 0.0, 0.0): "-i",
    (0.0, 0.0, 1.0, 0.0): "j",
    (0.0, 0.0, -1.0, 0.0): "-j",
    (0.0, 0.0, 0.0, 1.0): "k",
    (0.0, 0.0, 0.0, -1.0): "-k",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit(
            "PyYAML is required for presets.yaml. Install with: "
            "python3 -m pip install -e '.[dev]'"
        ) from exc
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise SystemExit(f"presets file is not a mapping: {path}")
    return data


def load_preset(name: str, path: Path = PRESETS_PATH) -> dict[str, Any]:
    data = _load_yaml(path)
    if name not in data or name == "sweep":
        keys = [k for k in data if k != "sweep"]
        raise SystemExit(f"unknown preset {name!r}; have {keys}")
    preset = dict(data[name])
    preset["_sweep"] = dict(data.get("sweep") or {})
    preset["_name"] = name
    return preset


def adj_kwargs(preset: dict[str, Any]) -> dict[str, Any]:
    return {
        "base_angle_thresh": float(preset["base_angle_thresh"]),
        "fiber_phase_bins": int(preset["fiber_phase_bins"]),
        "same_fiber_eta_tol": float(preset["same_fiber_eta_tol"]),
        "same_fiber_xi1_tol": float(preset["same_fiber_xi1_tol"]),
    }


def sg_kwargs(preset: dict[str, Any]) -> dict[str, Any]:
    return {
        "same_fiber_base_tol": float(preset.get("sg_same_fiber_base_tol", 1e-3)),
        "gauge_section": str(preset.get("sg_gauge_section", "min_index")),
        "inter_kind": str(preset.get("sg_inter_kind", "spherical_delaunay")),
    }


RULES = {
    "candidate": candidate_adjacency,
    "structure_group": structure_group_adjacency,
}


def rule_kwargs(rule: str, preset: dict[str, Any]) -> dict[str, Any]:
    if rule == "candidate":
        return adj_kwargs(preset)
    if rule == "structure_group":
        return sg_kwargs(preset)
    raise SystemExit(f"unknown rule {rule!r}")


def pin_header() -> dict[str, Any]:
    ver = version("flux-hopf-lib")
    parts = tuple(int(p) for p in ver.split(".")[:3])
    if parts < (0, 3, 1):
        raise SystemExit(f"need flux-hopf-lib>=0.3.1, got {ver}")
    q = np.array([0.0, 0.0, 1.0, 0.0])
    y_book = hopf_map(q)
    y_lib = np.array([float(c) for c in lib_hopf_map(0.0, 0.0, 1.0, 0.0)])
    want = np.array([0.0, 0.0, -1.0])
    if not np.allclose(y_book, want, atol=1e-12):
        raise SystemExit(f"book hopf_map((0,0,1,0)) != (0,0,-1): {y_book}")
    if not np.allclose(y_lib, want, atol=1e-12):
        raise SystemExit(f"lib hopf_map(0,0,1,0) != (0,0,-1): {y_lib}")
    if len(HURWITZ_UNITS) != 24:
        raise SystemExit(f"HURWITZ_UNITS has {len(HURWITZ_UNITS)}, not 24")
    return {
        "schema": SCHEMA,
        "claim": "Software fact",
        "op1_status": "Open",
        "flux_hopf_lib": ver,
        "hopf_map_0010": [0.0, 0.0, -1.0],
        "n_hurwitz_units": 24,
    }


def chart_angles(points: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Same inverse as ``candidate_adjacency`` (portal angle chart)."""
    x1, x2, x3, x4 = np.asarray(points, dtype=float).T
    eta = np.arctan2(np.sqrt(x3**2 + x4**2), np.sqrt(x1**2 + x2**2))
    xi1 = np.arctan2(x2, x1)
    xi2 = np.arctan2(x4, x3)
    return eta, xi1, xi2


def wrapped_delta(a: float, b: float) -> float:
    return abs(((a - b + np.pi) % (2.0 * np.pi)) - np.pi)


def base_angle(yi: np.ndarray, yj: np.ndarray) -> float:
    c = float(np.clip(np.dot(yi, yj), -1.0, 1.0))
    return float(np.arccos(c))


def distance_to_structure_group_fiber(q_i: np.ndarray, q_j: np.ndarray) -> float:
    """Min Euclidean distance from q_j to the left-U(1) circle through q_i.

    Same circle as ``sample_structure_group_fiber`` / ``common_phase``.
    Closed form so the 1e-3 threshold means on the curve, not on a 64-sample.
    """
    qi = q_normalize(np.asarray(q_i, dtype=float).reshape(4))
    qj = q_normalize(np.asarray(q_j, dtype=float).reshape(4))
    a = qi
    b = q_mult(I_UNIT, qi)
    v = np.array([float(np.dot(a, qj)), float(np.dot(b, qj))])
    n = float(np.linalg.norm(v))
    if n < 1e-15:
        return float(np.linalg.norm(qj - a))
    closest = (v[0] / n) * a + (v[1] / n) * b
    return float(np.linalg.norm(closest - qj))


def sample_min_distance_to_fiber(
    q_i: np.ndarray, q_j: np.ndarray, n_points: int
) -> float:
    curve = sample_structure_group_fiber(q_i, n_points=n_points)["points"]
    qj = q_normalize(np.asarray(q_j, dtype=float).reshape(4))
    return float(np.min(np.linalg.norm(curve - qj, axis=1)))


def unit_name(u: np.ndarray) -> str:
    u = np.asarray(u, dtype=float).reshape(4)
    key = tuple(round(float(c), 6) for c in u)
    if key in AXIS_NAMES:
        return AXIS_NAMES[key]
    if np.allclose(np.abs(u), 0.5, atol=1e-8):
        signs = "".join("+" if c > 0 else "-" for c in u)
        return f"half_{signs}"
    return "u(" + ",".join(f"{c:.3f}" for c in u) + ")"


def iter_hurwitz_units_i_first() -> list[np.ndarray]:
    out = [I_UNIT.copy()]
    for u in HURWITZ_UNITS:
        if not np.allclose(u, I_UNIT):
            out.append(np.asarray(u, dtype=float).copy())
    if len(out) != 24:
        raise RuntimeError(f"expected 24 units after i-first, got {len(out)}")
    return out


def build_l0(_preset: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    pts = np.asarray(HURWITZ_UNITS, dtype=float)
    return pts, {"n": int(len(pts)), "constructed_along": []}


def build_lang(preset: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    pts = sample_angle_lattice(
        n_eta=int(preset["n_eta"]),
        n_xi1=int(preset["n_xi1"]),
        n_xi2=int(preset["n_xi2"]),
        eta_range=tuple(preset["eta_range"]),
    )
    return pts, {"n": int(len(pts)), "constructed_along": []}


def build_lsg(preset: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    n_points = int(preset["lsg_n_points"])
    seeds = [np.asarray(s, dtype=float) for s in preset["lsg_seeds"]]
    blocks: list[np.ndarray] = []
    constructed: list[tuple[int, int]] = []
    bases: list[list[float]] = []
    fiber_scatter: list[float] = []
    offset = 0
    for q in seeds:
        fib = sample_structure_group_fiber(q, n_points=n_points)
        pts = np.asarray(fib["points"], dtype=float)
        blocks.append(pts)
        bases.append(
            [float(fib["base_y1"]), float(fib["base_y2"]), float(fib["base_y3"])]
        )
        fiber_base = hopf_project_points(pts)
        scatter = float(np.max(np.linalg.norm(fiber_base - fiber_base[0], axis=1)))
        fiber_scatter.append(scatter)
        for k in range(n_points):
            i = offset + k
            j = offset + ((k + 1) % n_points)
            constructed.append((i, j) if i < j else (j, i))
        offset += n_points
    stacked = np.vstack(blocks)
    return stacked, {
        "n": int(len(stacked)),
        "n_fibers": len(seeds),
        "n_points_per_fiber": n_points,
        "seed_bases": bases,
        "fiber_base_scatter": fiber_scatter,
        "fiber_base_scatter_max": max(fiber_scatter) if fiber_scatter else None,
        "constructed_along": constructed,
    }


BUILDERS = {"L0": build_l0, "Lang": build_lang, "Lsg": build_lsg}


def fiber_tol(set_name: str, preset: dict[str, Any]) -> float:
    if set_name == "Lang":
        return float(preset["along_fiber_tol_lang"])
    return float(preset["along_fiber_tol_l0_lsg"])


def _edge_metrics(
    points: np.ndarray,
    edges: list[tuple[int, int]],
    *,
    base: np.ndarray,
    eta: np.ndarray,
    xi1: np.ndarray,
    xi2: np.ndarray,
    preset: dict[str, Any],
    set_name: str,
) -> dict[str, Any]:
    n = len(edges)
    base_tol = float(preset["along_base_tol"])
    f_tol = fiber_tol(set_name, preset)
    eta_tol = float(preset["same_fiber_eta_tol"])
    xi1_tol = float(preset["same_fiber_xi1_tol"])
    n_curve = int(preset["sg_curve_n_points"])
    if n == 0:
        return {
            "n": 0,
            "along_base_near_0": None,
            "along_on_true_fiber": None,
            "along_chart_only": None,
            "mean_d_S": None,
            "mean_sg_circle_dist": None,
            "mean_sg_sample_min": None,
        }
    near0 = on_fib = chart_only = 0
    dS_sum = sg_sum = samp_sum = 0.0
    for i, j in edges:
        d_s = base_angle(base[i], base[j])
        sg = distance_to_structure_group_fiber(points[i], points[j])
        samp = sample_min_distance_to_fiber(points[i], points[j], n_curve)
        d_eta = abs(float(eta[i] - eta[j]))
        d_xi1 = wrapped_delta(float(xi1[i]), float(xi1[j]))
        dS_sum += d_s
        sg_sum += sg
        samp_sum += samp
        if d_s < base_tol:
            near0 += 1
        if sg < f_tol:
            on_fib += 1
        if d_eta <= eta_tol and d_xi1 <= xi1_tol and d_s >= base_tol:
            chart_only += 1
    return {
        "n": n,
        "along_base_near_0": near0 / n,
        "along_on_true_fiber": on_fib / n,
        "along_chart_only": chart_only / n,
        "mean_d_S": dS_sum / n,
        "mean_sg_circle_dist": sg_sum / n,
        "mean_sg_sample_min": samp_sum / n,
    }


def fiber_census(
    points: np.ndarray,
    along: list[tuple[int, int]],
    *,
    set_name: str,
    rule: str,
    same_fiber_base_tol: float,
) -> dict[str, Any]:
    """Describe h(Λ) as a discrete fiber bundle. Not a Farey diagram."""
    clusters = hopf_fiber_clusters(points, same_fiber_base_tol=same_fiber_base_tol)
    sizes = sorted(len(c) for c in clusters)
    occupied = [s for s in sizes if s >= 2]
    hist = {str(k): int(v) for k, v in sorted(Counter(sizes).items())}
    consecutive = consecutive_structure_group_along(points, clusters)
    cons_set = set(consecutive)
    along_set = set(tuple(sorted(e)) for e in along)
    n_match = len(along_set & cons_set)
    n_along = len(along_set)
    n_cons = len(cons_set)
    equal = along_set == cons_set
    n_bases = len(clusters)
    unique_occ = sorted(set(occupied))

    if n_along == 0:
        kind = "no_along_edges"
        note = (
            "No along-edges. On Λ0 at book_default this is chart sparsity "
            "(not a Farey graph). Use U(1) occupancy, not a looser η-tol."
        )
    elif equal and set_name == "Lang" and unique_occ == [8] and n_bases == 32:
        kind = "consecutive_u1_steps_on_product_sample"
        note = (
            "8 phases × 32 bases: discrete fiber bundle with a Delaunay base. "
            "Not a Farey diagram and not occupancy-necklace 256."
        )
    elif equal and set_name == "L0":
        kind = "u1_occupancy_through_lambda0"
        note = (
            f"{n_along} along-edges are occupancy of left-U(1) through Λ0 "
            "(cycles on occupied fibers), not 24 Farey neighbors. "
            "Software fact of Model 2; the 6×4 image is the Theorem."
        )
    elif equal and set_name == "Lsg":
        kind = "consecutive_u1_on_sampled_fibers"
        note = (
            "Along-edges are consecutive U(1) steps on sampled structure-group "
            "fibers (true by construction). Only Lsg has along = structure group "
            "by construction. Not a Farey diagram."
        )
    elif equal:
        kind = "consecutive_u1_matching"
        note = (
            "Along-set equals consecutive U(1) steps on Hopf-base clusters. "
            "Not a Farey diagram."
        )
    elif rule == "candidate":
        kind = "chart_xi2_circle_not_u1"
        note = (
            "Along-set is the angle-chart ξ2-circle, not consecutive U(1) "
            "on h(Λ) fibers."
        )
    else:
        kind = "not_exact_consecutive_u1"
        note = (
            f"Along-set matches {n_match}/{n_cons} consecutive U(1) edges "
            f"(rule n_along={n_along})."
        )

    out: dict[str, Any] = {
        "n_points": int(len(points)),
        "n_distinct_bases": n_bases,
        "multiplicity_histogram": hist,
        "n_occupied_fibers": len(occupied),
        "phases_per_occupied_fiber": unique_occ,
        "n_consecutive_u1_along": n_cons,
        "n_rule_along": n_along,
        "n_rule_along_equal_consecutive_u1": n_match,
        "along_equals_consecutive_u1": equal,
        "along_kind": kind,
        "note": note,
        "not_a_farey_diagram": True,
        "same_fiber_base_tol": same_fiber_base_tol,
    }
    base = hopf_project_points(points)
    if set_name == "L0" and n_bases == 6 and hist.get("4") == 6:
        out["image"] = {
            "object": "octahedron_poles",
            "n_points": 6,
            "multiplicity_per_fiber": 4,
            "claim": "Theorem",
            "note": (
                "Classical Hopf map sends the 24 Hurwitz units (24-cell vertices) "
                "to the 6 octahedron poles on S^2, four units per fiber."
            ),
            "realized_by_this_sample": bool(bases_are_octahedron_poles(base)),
        }
        out["along_edges_claim"] = "Software fact"
        out["parked_farey_slice_A"] = (
            "Unstarted. Natural slice: these 6 octahedron poles, spherical "
            "edges of length pi/2; ask which are P1(C) and whether any "
            "Delaunay edge is |ad-bc|=1."
        )
    elif set_name == "Lang":
        out["image"] = {
            "object": "angle_product_sample",
            "n_points": n_bases,
            "claim": "Software fact",
            "note": (
                "Product sample, not a theorem of the 24-cell. Same integer 256 "
                "as the occupancy necklace, different graph."
            ),
        }
        out["along_edges_claim"] = "Software fact"
    elif set_name == "Lsg":
        out["image"] = {
            "object": "sampled_structure_group_fibers",
            "n_points": n_bases,
            "claim": "Software fact",
            "note": (
                "Controlled true fibers. Only this set has along = structure group "
                "by construction."
            ),
        }
        out["along_equals_structure_group_by_construction"] = equal and kind == (
            "consecutive_u1_on_sampled_fibers"
        )
        out["along_edges_claim"] = "Software fact"
    return out


def _true_fiber_how(f_tol: float) -> str:
    return (
        "min Euclidean R^4 from q_j to the left-U(1) orbit {e^{iφ} q_i} "
        "(same circle as sample_structure_group_fiber / common_phase); "
        f"along_on_true_fiber iff that distance < {f_tol:g}"
    )


def experiment1(
    points: np.ndarray,
    *,
    set_name: str,
    preset: dict[str, Any],
    constructed_along: list[tuple[int, int]] | None = None,
    adj_fn=candidate_adjacency,
    kwargs: dict[str, Any] | None = None,
    rule: str = "candidate",
    sample_meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    kwargs = dict(kwargs) if kwargs is not None else adj_kwargs(preset)
    along, inter = adj_fn(points, **kwargs)
    base = hopf_project_points(points)
    eta, xi1, xi2 = chart_angles(points)
    along_m = _edge_metrics(
        points,
        along,
        base=base,
        eta=eta,
        xi1=xi1,
        xi2=xi2,
        preset=preset,
        set_name=set_name,
    )
    base_tol = float(preset["along_base_tol"])
    f_tol = fiber_tol(set_name, preset)
    n_inter = len(inter)
    leaks = 0
    dS_inter: list[float] = []
    if n_inter:
        for i, j in inter:
            d_s = base_angle(base[i], base[j])
            dS_inter.append(d_s)
            if d_s < base_tol:
                leaks += 1
                continue
            if distance_to_structure_group_fiber(points[i], points[j]) < f_tol:
                leaks += 1
    how = _true_fiber_how(f_tol)
    out: dict[str, Any] = {
        "n_points": int(len(points)),
        "n_along": int(len(along)),
        "n_inter": int(n_inter),
        "along_base_near_0": along_m["along_base_near_0"],
        "along_on_true_fiber": along_m["along_on_true_fiber"],
        "along_on_true_fiber_how": how,
        "along_on_true_fiber_denominator": (
            f"n_along={len(along)} from {rule} E_parallel; "
            "not constructed consecutive"
        ),
        "along_chart_only": along_m["along_chart_only"],
        "inter_leaks_into_along": (leaks / n_inter) if n_inter else None,
        "mean_d_S_along": along_m["mean_d_S"],
        "mean_sg_circle_dist_along": along_m["mean_sg_circle_dist"],
        "source": (
            "candidate_adjacency"
            if adj_fn is candidate_adjacency
            else "structure_group_adjacency"
        ),
        "rule": rule,
        "fiber_census": fiber_census(
            points,
            along,
            set_name=set_name,
            rule=rule,
            same_fiber_base_tol=float(preset.get("sg_same_fiber_base_tol", 1e-3)),
        ),
    }
    census = out["fiber_census"]
    if census["along_kind"] == "u1_occupancy_through_lambda0":
        out["l0_along_are_u1_occupancy_not_farey_neighbors"] = True
    if dS_inter:
        arr = np.asarray(dS_inter, dtype=float)
        n_exact = int(np.sum(arr <= 1e-15))
        inter_block: dict[str, Any] = {
            "n": n_inter,
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "mean": float(np.mean(arr)),
            "n_exact_zero": n_exact,
            "n_below_along_base_tol": int(np.sum(arr < base_tol)),
            "leak_is_exact": bool(np.max(arr) <= 1e-15),
        }
        if n_inter <= 64:
            inter_block["values"] = [float(x) for x in arr]
            inter_block["pairs"] = [list(e) for e in inter]
        out["inter_base_distances"] = inter_block
    if constructed_along:
        cons = _edge_metrics(
            points,
            constructed_along,
            base=base,
            eta=eta,
            xi1=xi1,
            xi2=xi2,
            preset=preset,
            set_name=set_name,
        )
        out["constructed_consecutive"] = {
            "n_along": cons["n"],
            "along_base_near_0": cons["along_base_near_0"],
            "along_on_true_fiber": cons["along_on_true_fiber"],
            "along_on_true_fiber_how": how,
            "along_on_true_fiber_denominator": (
                f"n_along={cons['n']} consecutive samples on "
                "sample_structure_group_fiber (wrap included); "
                f"not {rule} E_parallel"
            ),
            "along_chart_only": cons["along_chart_only"],
            "mean_d_S": cons["mean_d_S"],
            "mean_sg_circle_dist": cons["mean_sg_circle_dist"],
            "source": "consecutive samples on sample_structure_group_fiber",
        }
        out["denominators_are_distinct"] = True
        out["do_not_collapse_candidate_n_along_with_constructed_n_along"] = True
    if sample_meta and sample_meta.get("fiber_base_scatter") is not None:
        out["lsg_fiber_base_scatter"] = sample_meta["fiber_base_scatter"]
        out["lsg_fiber_base_scatter_max"] = sample_meta.get("fiber_base_scatter_max")
    return out


def _undirected_set(edges: Iterable[tuple[int, int]]) -> set[tuple[int, int]]:
    s: set[tuple[int, int]] = set()
    for a, b in edges:
        s.add((a, b))
        s.add((b, a))
    return s


def _frac(count: int, n: int) -> float | None:
    if n == 0:
        return None
    return count / n


def classify_image(
    along: list[tuple[int, int]],
    inter: list[tuple[int, int]],
    along_img: list[tuple[int, int]],
    inter_img: list[tuple[int, int]],
) -> dict[str, Any]:
    """Type-flip / lost on a list of image edges (same-index or remapped)."""
    along_m = _undirected_set(along_img)
    inter_m = _undirected_set(inter_img)

    def one(
        edges: list[tuple[int, int]], keep: set[tuple[int, int]], flip: set[tuple[int, int]]
    ) -> tuple[int, int, int]:
        k = f = lost = 0
        for e in edges:
            if e in keep:
                k += 1
            elif e in flip:
                f += 1
            else:
                lost += 1
        return k, f, lost

    ak, af, al = one(along, along_m, inter_m)
    ik, iff, il = one(inter, inter_m, along_m)
    n_a, n_i = len(along), len(inter)
    return {
        "along_kept": _frac(ak, n_a),
        "inter_kept": _frac(ik, n_i),
        "along_to_inter": _frac(af, n_a),
        "inter_to_along": _frac(iff, n_i),
        "lost": _frac(al, n_a),
        "along_lost": _frac(al, n_a),
        "inter_lost": _frac(il, n_i),
        "n_along": n_a,
        "n_inter": n_i,
    }


def classify_nearest(
    along: list[tuple[int, int]],
    inter: list[tuple[int, int]],
    imap: dict[int, int],
) -> dict[str, Any]:
    """Snap each endpoint to the nearest remaining site; type the image pair
    on the original graph."""
    along_set = _undirected_set(along)
    inter_set = _undirected_set(inter)

    def one(
        edges: list[tuple[int, int]],
        keep: set[tuple[int, int]],
        flip: set[tuple[int, int]],
    ) -> tuple[int, int, int, int]:
        k = f = lost = coll = 0
        for a, b in edges:
            ia, ib = imap[a], imap[b]
            if ia == ib:
                lost += 1
                coll += 1
                continue
            e = (ia, ib)
            if e in keep:
                k += 1
            elif e in flip:
                f += 1
            else:
                lost += 1
        return k, f, lost, coll

    ak, af, al, ac = one(along, along_set, inter_set)
    ik, iff, il, ic = one(inter, inter_set, along_set)
    n_a, n_i = len(along), len(inter)
    return {
        "along_kept": _frac(ak, n_a),
        "inter_kept": _frac(ik, n_i),
        "along_to_inter": _frac(af, n_a),
        "inter_to_along": _frac(iff, n_i),
        "lost": _frac(al, n_a),
        "along_lost": _frac(al, n_a),
        "inter_lost": _frac(il, n_i),
        "n_along": n_a,
        "n_inter": n_i,
        "n_collapsed_along": ac,
        "n_collapsed_inter": ic,
    }


def gauge_row(
    points: np.ndarray,
    unit: np.ndarray,
    *,
    side: str,
    resnap: str,
    kwargs: dict[str, Any],
    adj_fn=candidate_adjacency,
    rule: str = "candidate",
) -> dict[str, Any]:
    along, inter = adj_fn(points, **kwargs)
    moved = apply_gauge_step(points, side, unit)

    if resnap in ("exact", "none"):
        along_m, inter_m = adj_fn(moved, **kwargs)
        classified = classify_image(along, inter, along_m, inter_m)
    elif resnap == "nearest":
        imap = nearest_index_map(moved, points)
        classified = classify_nearest(along, inter, imap)
    else:
        raise ValueError(f"unknown resnap {resnap!r}")

    row = {
        "unit": [float(c) for c in np.asarray(unit, dtype=float).reshape(4)],
        "unit_name": unit_name(unit),
        "side": side,
        "resnap": resnap,
        "along_kept": classified["along_kept"],
        "inter_kept": classified["inter_kept"],
        "along_to_inter": classified["along_to_inter"],
        "lost": classified["lost"],
        "along_lost": classified["along_lost"],
        "inter_lost": classified["inter_lost"],
        "inter_to_along": classified["inter_to_along"],
        "n_along": classified["n_along"],
        "n_inter": classified["n_inter"],
        "rule": rule,
    }
    if adj_fn is candidate_adjacency:
        lib_score = adjacency_equivariance_score(points, unit, side=side, **kwargs)
        row["lib_score"] = {
            "along_preserved": float(lib_score["along_preserved"]),
            "inter_preserved": float(lib_score["inter_preserved"]),
            "n_along": float(lib_score["n_along"]),
            "n_inter": float(lib_score["n_inter"]),
        }
    if "n_collapsed_along" in classified:
        row["n_collapsed_along"] = classified["n_collapsed_along"]
        row["n_collapsed_inter"] = classified["n_collapsed_inter"]
    return row


def experiment2(
    points: np.ndarray,
    *,
    resnap: str,
    kwargs: dict[str, Any],
    sides: tuple[str, ...] = ("L", "R"),
    units: list[np.ndarray] | None = None,
    adj_fn=candidate_adjacency,
    rule: str = "candidate",
) -> list[dict[str, Any]]:
    rows = []
    for u in units if units is not None else iter_hurwitz_units_i_first():
        for side in sides:
            rows.append(
                gauge_row(
                    points,
                    u,
                    side=side,
                    resnap=resnap,
                    kwargs=kwargs,
                    adj_fn=adj_fn,
                    rule=rule,
                )
            )
    return rows


def default_resnap(set_name: str, explicit: str | None) -> str:
    if explicit:
        return explicit
    return "exact" if set_name == "L0" else "none"


def validate_resnap(set_name: str, resnap: str) -> None:
    if resnap == "exact" and set_name != "L0":
        raise SystemExit("resnap=exact is only valid on L0 (permutation, no snap)")
    if resnap not in ("exact", "none", "nearest"):
        raise SystemExit(f"unknown resnap {resnap!r}")


def _json_ready(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _json_ready(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_ready(v) for v in obj]
    if isinstance(obj, tuple):
        return [_json_ready(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def fmt_frac(x: float | None) -> str:
    if x is None:
        return "n/a (0 edges)"
    return f"{x:.6f}"


def render_markdown(payload: dict[str, Any]) -> str:
    e1 = payload["experiment1"]
    lines = [
        f"# OP1 adjacency harness — {payload['set']} / {payload['preset']} "
        f"(rule={payload.get('rule', 'candidate')}, resnap={payload['resnap']})",
        "",
        "Claim type: **Software fact**. OP1 status: **Open**. Not a theorem of Chapter 3.",
        "",
        f"- flux-hopf-lib `{payload['flux_hopf_lib']}`",
        f"- `hopf_map((0,0,1,0)) = {payload['hopf_map_0010']}`",
        f"- n_points = {e1['n_points']}",
        f"- rule = `{payload.get('rule', e1.get('rule', 'candidate'))}`",
        "",
        "## Experiment 1 — is E_parallel a Hopf fiber?",
        "",
        "Top-level `along_on_true_fiber` uses the **rule's** E_parallel as denominator.",
        "Constructed consecutive (Lsg) is a **different list** and must not be collapsed.",
        "",
        "| field | value |",
        "|---|---|",
        f"| n_along (rule E_parallel) | {e1['n_along']} |",
        f"| n_inter | {e1['n_inter']} |",
        f"| along_on_true_fiber | {fmt_frac(e1['along_on_true_fiber'])} |",
        f"| denominator | {e1.get('along_on_true_fiber_denominator', '')} |",
        f"| how | {e1.get('along_on_true_fiber_how', '')} |",
        f"| along_base_near_0 | {fmt_frac(e1['along_base_near_0'])} |",
        f"| along_chart_only | {fmt_frac(e1['along_chart_only'])} |",
        f"| inter_leaks_into_along | {fmt_frac(e1['inter_leaks_into_along'])} |",
        f"| source | `{e1['source']}` |",
        "",
    ]
    census = e1.get("fiber_census")
    if census:
        lines += [
            "### Fiber census (h(Λ), not a Farey diagram)",
            "",
            f"- n_distinct_bases = {census['n_distinct_bases']}",
            f"- multiplicity histogram (phases per base) = {census['multiplicity_histogram']}",
            f"- along_kind = `{census['along_kind']}`",
            f"- along_equals_consecutive_U(1) = {census['along_equals_consecutive_u1']}",
            f"- {census['note']}",
            "",
        ]
        img = census.get("image")
        if img:
            lines.append(
                f"- image: `{img.get('object')}` — **{img.get('claim')}**. {img.get('note')}"
            )
            if census.get("along_edges_claim"):
                lines.append(
                    f"- along-edges claim: **{census['along_edges_claim']}** "
                    "(not Farey neighbors)."
                )
            lines.append("")
    ibd = e1.get("inter_base_distances")
    if ibd:
        lines += [
            f"Inter-edge base distances: n={ibd['n']}, min={ibd['min']:.3e}, "
            f"max={ibd['max']:.3e}, n_exact_zero={ibd['n_exact_zero']}, "
            f"leak_is_exact={ibd['leak_is_exact']}.",
            "",
        ]
    cons = e1.get("constructed_consecutive")
    if cons:
        lines += [
            "### Lsg consecutive samples (by construction, true fiber)",
            "",
            "Denominator is **64 constructed consecutive samples**, not the rule's n_along.",
            "",
            "| field | value |",
            "|---|---|",
            f"| n_along | {cons['n_along']} |",
            f"| along_on_true_fiber | {fmt_frac(cons['along_on_true_fiber'])} |",
            f"| denominator | {cons.get('along_on_true_fiber_denominator', '')} |",
            f"| along_base_near_0 | {fmt_frac(cons['along_base_near_0'])} |",
            f"| along_chart_only | {fmt_frac(cons['along_chart_only'])} |",
            "",
        ]
    if e1.get("lsg_fiber_base_scatter") is not None:
        lines += [
            f"Lsg hopf_map scatter per fiber: {e1['lsg_fiber_base_scatter']} "
            f"(max {e1.get('lsg_fiber_base_scatter_max')}; pin requires < 1e-8).",
            "",
        ]
    rows = payload["experiment2"]
    highlight = [r for r in rows if r["unit_name"] in ("i", "j")]
    if highlight:
        lines += [
            "## Experiment 2 — units i and j (not an L/R average)",
            "",
            "| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for r in highlight:
            lines.append(
                f"| {r['unit_name']} | {r['side']} | {fmt_frac(r['along_kept'])} | "
                f"{fmt_frac(r['inter_kept'])} | {fmt_frac(r['along_to_inter'])} | "
                f"{fmt_frac(r['lost'])} | {r['n_along']} | {r['n_inter']} |"
            )
        lines.append("")
    lines += [
        "## Experiment 2 — 24 × 2",
        "",
        "| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['unit_name']} | {r['side']} | {fmt_frac(r['along_kept'])} | "
            f"{fmt_frac(r['inter_kept'])} | {fmt_frac(r['along_to_inter'])} | "
            f"{fmt_frac(r['lost'])} | {r['n_along']} | {r['n_inter']} |"
        )
    lines.append("")
    return "\n".join(lines)


def dump_edges_payload(
    points: np.ndarray,
    along: list[tuple[int, int]],
    inter: list[tuple[int, int]],
) -> dict[str, Any]:
    xyz = np.stack([stereographic(q) for q in points], axis=0)
    return {
        "claim": "Software fact",
        "along_color": "red fiber-claim (rule E_parallel, Model, not a theorem)",
        "inter_color": "blue base-claim",
        "along": [list(e) for e in along],
        "inter": [list(e) for e in inter],
        "xyz": xyz.tolist(),
    }


GRAPH_KIND = "qga_adjacency_graph_v1"


def dump_graph_payload(
    points: np.ndarray,
    along: list[tuple[int, int]],
    inter: list[tuple[int, int]],
    *,
    set_name: str,
    rule: str,
    census: dict[str, Any],
) -> dict[str, Any]:
    """Witness sidecar: indices + coordinates. Not export_fiber_curves.

    ``op1_row`` is filled in ``write_run`` once the stem is known.
    Fractions stay on the attached OP1 row.
    """
    points = np.asarray(points, dtype=float)
    base = hopf_project_points(points)
    xyz = np.stack([stereographic(q) for q in points], axis=0)
    phases = census.get("phases_per_occupied_fiber") or []
    if phases and len(set(int(x) for x in phases)) == 1:
        multiplicity: Any = int(phases[0])
    else:
        multiplicity = [int(x) for x in phases]
    return {
        "kind": GRAPH_KIND,
        "rule": rule,
        "set": set_name,
        "op1_row": None,
        "projection": "stereographic",
        "map": "hopf_map_classical",
        "points": [
            {
                "q": [float(c) for c in q],
                "xyz": [float(c) for c in xyz[i]],
                "base": [float(c) for c in base[i]],
            }
            for i, q in enumerate(points)
        ],
        "along": [list(e) for e in along],
        "inter": [list(e) for e in inter],
        "census": {
            "distinct_bases": int(census["n_distinct_bases"]),
            "multiplicity": multiplicity,
            "along_kind": census["along_kind"],
        },
    }


def run_one(
    set_name: str,
    preset: dict[str, Any],
    *,
    resnap: str,
    dump_edges: bool = True,
    dump_graph: bool = False,
    sides: tuple[str, ...] = ("L", "R"),
    units: list[np.ndarray] | None = None,
    rule: str = "candidate",
) -> dict[str, Any]:
    validate_resnap(set_name, resnap)
    if rule not in RULES:
        raise SystemExit(f"unknown rule {rule!r}")
    if dump_graph and rule != "structure_group":
        raise SystemExit(
            "--dump-graph is a structure_group witness; refused for "
            f"rule={rule!r} (no candidate edges in analysis dumps)"
        )
    header = pin_header()
    points, meta = BUILDERS[set_name](preset)
    if set_name == "Lsg":
        sc = meta.get("fiber_base_scatter_max")
        if sc is None or sc >= 1e-8:
            raise SystemExit(
                f"Lsg hopf_map scatter {sc} is not < 1e-8 (flux-hopf-lib pin)"
            )
    kwargs = rule_kwargs(rule, preset)
    adj_fn = RULES[rule]
    e1 = experiment1(
        points,
        set_name=set_name,
        preset=preset,
        constructed_along=meta.get("constructed_along") or None,
        adj_fn=adj_fn,
        kwargs=kwargs,
        rule=rule,
        sample_meta=meta,
    )
    e2 = experiment2(
        points,
        resnap=resnap,
        kwargs=kwargs,
        sides=sides,
        units=units,
        adj_fn=adj_fn,
        rule=rule,
    )
    payload: dict[str, Any] = {
        **header,
        "set": set_name,
        "preset": preset["_name"],
        "rule": rule,
        "thresholds": kwargs,
        "sample": {
            k: v
            for k, v in meta.items()
            if k != "constructed_along"
        },
        "resnap": resnap,
        "experiment1": e1,
        "experiment2": e2,
    }
    along = inter = None
    if dump_edges or dump_graph:
        along, inter = adj_fn(points, **kwargs)
    if dump_edges:
        payload["edges_sidecar"] = dump_edges_payload(points, along, inter)
    if dump_graph:
        payload["graph_sidecar"] = dump_graph_payload(
            points,
            along,
            inter,
            set_name=set_name,
            rule=rule,
            census=e1["fiber_census"],
        )
    return _json_ready(payload)


def write_run(
    payload: dict[str, Any],
    out_dir: Path,
    *,
    stem: str | None = None,
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    if stem is None:
        day = date.today().strftime("%Y%m%d")
        rule = payload.get("rule", "candidate")
        stem = f"{day}_{payload['set']}_{payload['preset']}_{payload['resnap']}"
        if rule != "candidate":
            stem = f"{stem}_{rule}"
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    sidecar = payload.pop("edges_sidecar", None)
    graph = payload.pop("graph_sidecar", None)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    md = render_markdown(payload)
    md_path.write_text(md, encoding="utf-8")
    if sidecar is not None:
        edge_path = out_dir / f"{stem}_edges.json"
        edge_path.write_text(json.dumps(sidecar, indent=2) + "\n", encoding="utf-8")
    if graph is not None:
        try:
            graph["op1_row"] = str(json_path.relative_to(ROOT))
        except ValueError:
            graph["op1_row"] = json_path.name
        graph_path = out_dir / f"{stem}_graph.json"
        graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    return json_path, md_path


def sweep_heatmap(
    set_name: str,
    preset: dict[str, Any],
    out_dir: Path,
) -> Path:
    import matplotlib.pyplot as plt

    grid = preset.get("_sweep") or {}
    bases = [float(x) for x in grid["base_angle_thresh"]]
    etas = [float(x) for x in grid["same_fiber_eta_tol"]]
    points, meta = BUILDERS[set_name](preset)
    z = np.zeros((len(etas), len(bases)))
    n_along = np.zeros_like(z)
    for iy, eta_tol in enumerate(etas):
        for ix, base_t in enumerate(bases):
            p = dict(preset)
            p["base_angle_thresh"] = base_t
            p["same_fiber_eta_tol"] = eta_tol
            e1 = experiment1(
                points,
                set_name=set_name,
                preset=p,
                constructed_along=None,
            )
            val = e1["along_on_true_fiber"]
            z[iy, ix] = float("nan") if val is None else float(val)
            n_along[iy, ix] = e1["n_along"]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))
    im0 = axes[0].imshow(
        z, origin="lower", aspect="auto", vmin=0.0, vmax=1.0, cmap="viridis"
    )
    axes[0].set_xticks(range(len(bases)), [f"{b:g}" for b in bases])
    axes[0].set_yticks(range(len(etas)), [f"{e:g}" for e in etas])
    axes[0].set_xlabel("base_angle_thresh")
    axes[0].set_ylabel("same_fiber_eta_tol")
    axes[0].set_title(r"along_on_true_fiber (Model)")
    fig.colorbar(im0, ax=axes[0], fraction=0.046)
    im1 = axes[1].imshow(n_along, origin="lower", aspect="auto", cmap="magma")
    axes[1].set_xticks(range(len(bases)), [f"{b:g}" for b in bases])
    axes[1].set_yticks(range(len(etas)), [f"{e:g}" for e in etas])
    axes[1].set_xlabel("base_angle_thresh")
    axes[1].set_ylabel("same_fiber_eta_tol")
    axes[1].set_title(r"$n$ along-edges (Model)")
    fig.colorbar(im1, ax=axes[1], fraction=0.046)
    fig.suptitle(
        f"OP1 candidate_adjacency sweep on {set_name} — Model, not a theorem",
        fontsize=11,
        fontweight="bold",
    )
    fig.tight_layout()
    out_dir.mkdir(parents=True, exist_ok=True)
    day = date.today().strftime("%Y%m%d")
    path = out_dir / f"{day}_sweep_base_x_eta_{set_name}.png"
    fig.savefig(path, dpi=140, facecolor="white")
    plt.close(fig)
    # numeric companion
    npz = out_dir / f"{day}_sweep_base_x_eta_{set_name}.json"
    npz.write_text(
        json.dumps(
            {
                "claim": "Software fact / Model sweep",
                "op1_status": "Open",
                "set": set_name,
                "base_angle_thresh": bases,
                "same_fiber_eta_tol": etas,
                "along_on_true_fiber": z.tolist(),
                "n_along": n_along.tolist(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--set", dest="set_name", default="Lang", help="L0, Lang, Lsg, or all")
    p.add_argument("--preset", default="book_default")
    p.add_argument("--resnap", default=None, choices=["exact", "none", "nearest"])
    p.add_argument("--out-dir", type=Path, default=ROOT / "notes" / "op1_runs")
    p.add_argument("--stem", default=None, help="output filename stem (tests)")
    p.add_argument("--sweep", action="store_true")
    p.add_argument("--no-edges", action="store_true")
    p.add_argument(
        "--dump-graph",
        action="store_true",
        help=(
            "Write <stem>_graph.json (kind=qga_adjacency_graph_v1). "
            "structure_group witness only; refused for candidate."
        ),
    )
    p.add_argument("--unit", default=None, help="restrict Experiment 2 to this unit name (e.g. i)")
    p.add_argument("--side", default=None, choices=["L", "R"])
    p.add_argument(
        "--rule",
        default="candidate",
        choices=["candidate", "structure_group", "all"],
        help=(
            "candidate: frozen book default (figures, golden). "
            "structure_group: Model 2 for analysis/OP2/flywheels after the JSON row "
            "is attached. Do not mix edge sets."
        ),
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    preset = load_preset(args.preset)
    sets = ["L0", "Lang", "Lsg"] if args.set_name == "all" else [args.set_name]
    for s in sets:
        if s not in BUILDERS:
            raise SystemExit(f"unknown set {s!r}")
    if args.sweep:
        for s in sets:
            path = sweep_heatmap(s, preset, args.out_dir)
            print(path)
        return 0
    units = None
    if args.unit:
        wanted = args.unit
        units = [u for u in iter_hurwitz_units_i_first() if unit_name(u) == wanted]
        if not units:
            raise SystemExit(f"no Hurwitz unit named {wanted!r}")
    sides: tuple[str, ...]
    if args.side:
        sides = (args.side,)
    else:
        sides = ("L", "R")
    if args.dump_graph and args.rule != "structure_group":
        raise SystemExit(
            "--dump-graph is a structure_group witness; refused for "
            f"rule={args.rule!r} (no candidate edges in analysis dumps)"
        )
    rules = ["candidate", "structure_group"] if args.rule == "all" else [args.rule]
    for s in sets:
        resnap = default_resnap(s, args.resnap)
        for rule in rules:
            payload = run_one(
                s,
                preset,
                resnap=resnap,
                dump_edges=not args.no_edges,
                dump_graph=args.dump_graph,
                sides=sides,
                units=units,
                rule=rule,
            )
            json_path, md_path = write_run(payload, args.out_dir, stem=args.stem)
            print(json_path)
            print(md_path)
            graph_path = json_path.with_name(json_path.stem + "_graph.json")
            if args.dump_graph:
                print(graph_path)
            print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
