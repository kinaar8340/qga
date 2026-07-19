"""Flux topograph helpers for Kingdom Come / QGA Chapters 5–6.

Pedagogical **Model** implementations of flux functionals, value landscapes,
separator detection, gauge periodicity scores, and classification / Magic Island
diagnostics on the gauged Hopf lattice.

Not claimed to be the unique Conway/Hatcher lift (Open Problems 2–3).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal

import numpy as np

from .hopf_lattice import (
    HURWITZ_UNITS,
    apply_gauge_sequence,
    chordal_distance_s3,
    hopf_project_points,
    phase_unit,
    q_normalize,
)

Array = np.ndarray
FunctionalName = Literal["norm", "hopf_y1", "hopf_height", "phase", "index_wave"]


@dataclass
class FluxTopograph:
    """Value landscape on a discrete point set in S³."""

    points: Array
    values: Array
    edges: list[tuple[int, int]] = field(default_factory=list)
    functional: str = "norm"
    meta: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.points = np.asarray(self.points, dtype=float)
        self.values = np.asarray(self.values, dtype=float)
        if len(self.points) != len(self.values):
            raise ValueError("points and values length mismatch")


def _functional_values(points: Array, name: FunctionalName) -> Array:
    points = np.asarray(points, dtype=float)
    if name == "norm":
        # already unit; use squared imag part as a simple quadratic form
        return points[:, 1] ** 2 + points[:, 2] ** 2 + points[:, 3] ** 2
    if name == "hopf_y1":
        base = hopf_project_points(points, convention="classical")
        return base[:, 0]
    if name == "hopf_height":
        base = hopf_project_points(points, convention="classical")
        return base[:, 2]
    if name == "phase":
        # fiber phase proxy from (x3, x4)
        return np.arctan2(points[:, 3], points[:, 2])
    if name == "index_wave":
        # smooth combinatorial wave for separator demos
        n = len(points)
        t = np.linspace(0, 4 * np.pi, n, endpoint=False)
        return np.sin(t) + 0.35 * np.cos(2 * t)
    raise ValueError(f"unknown functional: {name}")


def build_flux_topograph(
    points: Array,
    edges: list[tuple[int, int]] | None = None,
    *,
    functional: FunctionalName | Callable[[Array], Array] = "norm",
) -> FluxTopograph:
    """Build a flux topograph on lattice points.

    Parameters
    ----------
    points :
        Array (N, 4) of unit quaternions / S³ samples.
    edges :
        Optional undirected edges for separator graph walk.
    functional :
        Named functional or callable ``points -> values``.
    """
    points = np.asarray(points, dtype=float)
    if callable(functional) and not isinstance(functional, str):
        values = np.asarray(functional(points), dtype=float)
        fname = getattr(functional, "__name__", "custom")
    else:
        values = _functional_values(points, functional)  # type: ignore[arg-type]
        fname = str(functional)
    return FluxTopograph(
        points=points,
        values=values,
        edges=list(edges or []),
        functional=fname,
        meta={"n": len(points)},
    )


def detect_separators(
    topo: FluxTopograph,
    *,
    threshold: float | None = None,
    mode: Literal["sign", "level"] = "sign",
) -> list[list[tuple[int, int]]]:
    """Detect separator edge components where the functional crosses a threshold.

    Returns a list of connected components; each component is a list of edges
    (i, j) with i < j.
    """
    values = topo.values
    if threshold is None:
        threshold = 0.0 if mode == "sign" else float(np.median(values))

    # edges to scan
    if topo.edges:
        candidates = [(min(a, b), max(a, b)) for a, b in topo.edges]
    else:
        # fallback: kNN-lite on first 3 stereo coords would be heavy; use
        # complete graph on small sets only
        n = len(values)
        if n > 80:
            # sparse: connect sequential indices as a demo lattice
            candidates = [(i, i + 1) for i in range(n - 1)] + ([(0, n - 1)] if n > 2 else [])
        else:
            candidates = [(i, j) for i in range(n) for j in range(i + 1, n)]

    sep_edges: list[tuple[int, int]] = []
    for i, j in candidates:
        vi, vj = values[i], values[j]
        if mode == "sign":
            if vi == 0 or vj == 0:
                sep_edges.append((i, j))
            elif (vi - threshold) * (vj - threshold) < 0:
                sep_edges.append((i, j))
        else:
            # level: edge crosses threshold if min < thr < max
            lo, hi = (vi, vj) if vi <= vj else (vj, vi)
            if lo < threshold < hi or abs(vi - threshold) < 1e-12 or abs(vj - threshold) < 1e-12:
                sep_edges.append((i, j))

    # connected components on the separator graph
    if not sep_edges:
        return []

    adj: dict[int, set[int]] = {}
    for i, j in sep_edges:
        adj.setdefault(i, set()).add(j)
        adj.setdefault(j, set()).add(i)

    seen: set[int] = set()
    components: list[list[tuple[int, int]]] = []
    for start in list(adj.keys()):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        nodes: set[int] = set()
        while stack:
            u = stack.pop()
            nodes.add(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        comp_edges = [(i, j) for i, j in sep_edges if i in nodes and j in nodes]
        components.append(comp_edges)
    return components


def arithmetic_progression_residuals(
    topo: FluxTopograph,
) -> dict[str, float]:
    """Check a simple AP-style relation on edges: 2*mid ≈ left+right along paths.

    For each edge (i,j) we only have two values; we report mean |v_i - v_j| and
    variance of differences as a coarse “progression regularity” score.
    """
    if not topo.edges:
        return {"mean_abs_jump": float("nan"), "std_jump": float("nan"), "n_edges": 0.0}
    jumps = []
    for i, j in topo.edges:
        jumps.append(topo.values[j] - topo.values[i])
    jumps_a = np.asarray(jumps, dtype=float)
    return {
        "mean_abs_jump": float(np.mean(np.abs(jumps_a))),
        "std_jump": float(np.std(jumps_a)),
        "n_edges": float(len(jumps_a)),
    }


def apply_gauge_to_topograph(
    topo: FluxTopograph,
    sequence: list[tuple[str, Array]],
    *,
    recompute_functional: bool = True,
) -> FluxTopograph:
    """Push points through a gauge sequence; recompute or transport values.

    If ``recompute_functional`` is True, values are recomputed from the named
    functional (exact equivariance for geometric functionals). If False, values
    are carried along by index (correct when the gauge permutes a fixed list).
    """
    hist = apply_gauge_sequence(topo.points, sequence, record=True)
    new_pts = hist[-1]
    if recompute_functional and topo.functional in (
        "norm",
        "hopf_y1",
        "hopf_height",
        "phase",
        "index_wave",
    ):
        return build_flux_topograph(
            new_pts,
            edges=topo.edges,
            functional=topo.functional,  # type: ignore[arg-type]
        )
    return FluxTopograph(
        points=new_pts,
        values=topo.values.copy(),
        edges=list(topo.edges),
        functional=topo.functional,
        meta=dict(topo.meta),
    )


def _point_cloud_distance(a: Array, b: Array) -> float:
    """Fast symmetric multiset distance via sorted coordinates (O(N log N))."""
    a_s = np.sort(np.round(a, 8), axis=0)
    b_s = np.sort(np.round(b, 8), axis=0)
    if a_s.shape != b_s.shape:
        n = max(len(a_s), len(b_s))
        # pad with last row
        if len(a_s) < n:
            a_s = np.vstack([a_s, np.repeat(a_s[-1:], n - len(a_s), axis=0)])
        if len(b_s) < n:
            b_s = np.vstack([b_s, np.repeat(b_s[-1:], n - len(b_s), axis=0)])
    return float(np.mean(np.linalg.norm(a_s - b_s, axis=1)))


def periodicity_score(
    topo: FluxTopograph,
    sequence: list[tuple[str, Array]],
    *,
    max_periods: int = 8,
    tol: float = 1e-3,
) -> dict[str, float]:
    """Score how nearly a gauge sequence returns the topograph.

    Uses sorted point-cloud distance (fast) plus value multiset L2 distance.
    """
    cur = topo
    best_pt = float("inf")
    best_val = float("inf")
    period_found = -1.0
    for p in range(1, max_periods + 1):
        cur = apply_gauge_to_topograph(cur, sequence, recompute_functional=True)
        mean_pt = _point_cloud_distance(topo.points, cur.points)
        v0 = np.sort(topo.values)
        v1 = np.sort(cur.values)
        val_d = float(np.linalg.norm(v0 - v1) / (np.linalg.norm(v0) + 1e-12))
        best_pt = min(best_pt, mean_pt)
        best_val = min(best_val, val_d)
        if mean_pt <= tol and val_d <= tol:
            period_found = float(p)
            break
    return {
        "best_point_nn_mean": best_pt,
        "best_value_multiset_rel": best_val,
        "period_found": period_found,
        "max_periods": float(max_periods),
    }


def separator_equivariance_score(
    topo: FluxTopograph,
    sequence: list[tuple[str, Array]],
    *,
    threshold: float | None = None,
) -> dict[str, float]:
    """Compare separator edge counts before/after gauge (OP2 diagnostic)."""
    seps0 = detect_separators(topo, threshold=threshold)
    topo1 = apply_gauge_to_topograph(topo, sequence, recompute_functional=True)
    seps1 = detect_separators(topo1, threshold=threshold)
    n0 = sum(len(c) for c in seps0)
    n1 = sum(len(c) for c in seps1)
    return {
        "n_sep_edges_before": float(n0),
        "n_sep_edges_after": float(n1),
        "n_components_before": float(len(seps0)),
        "n_components_after": float(len(seps1)),
        "edge_count_ratio": float(n1 / n0) if n0 else float("nan"),
    }


def stability_landscape_z(
    z_values: list[int] | None = None,
    *,
    z_range: tuple[int, int] | None = None,
    extended: bool = False,
) -> list[dict]:
    """Thin wrapper around kingdom map_z_to_flywheel when available.

    Parameters
    ----------
    z_values :
        Explicit list of atomic numbers.
    z_range :
        Inclusive ``(z_min, z_max)`` alternative to ``z_values``.
    extended :
        If True, call ``map_z_to_flywheel_extended`` and include a few
        chemistry-facing fields.
    """
    try:
        from kingdom.core.flux_flywheel import map_z_to_flywheel, map_z_to_flywheel_extended
    except ImportError as e:  # pragma: no cover
        raise ImportError(
            "kingdom.core.flux_flywheel required; set PYTHONPATH to kingdom/src"
        ) from e
    if z_range is not None:
        z_min, z_max = z_range
        z_values = list(range(int(z_min), int(z_max) + 1))
    if z_values is None:
        z_values = [2, 10, 26, 79, 118]
    out = []
    for z in z_values:
        if extended:
            m = map_z_to_flywheel_extended(int(z))
        else:
            m = map_z_to_flywheel(int(z))
        row = {
            "Z": z,
            "stability_score": m.get("stability_score"),
            "stability_class": m.get("stability_class"),
            "is_noble_gas": m.get("is_noble_gas"),
            "delta_omega": m.get("delta_omega"),
        }
        if extended:
            row["alignment_stability_pts"] = m.get("alignment_stability_pts")
            row["model_vs_reality_alignment"] = m.get("model_vs_reality_alignment")
            row["real_ionization_energy_eV"] = m.get("real_ionization_energy_eV")
        out.append(row)
    return out


# ---------------------------------------------------------------------------
# Classification / Magic Islands (Chapter 6 — Model / OP3)
# ---------------------------------------------------------------------------


def standard_gauge_set() -> list[list[tuple[str, Array]]]:
    """Small dictionary of gauge sequences for reduced-orbit experiments."""
    i = np.array([0.0, 1.0, 0.0, 0.0])
    j = np.array([0.0, 0.0, 1.0, 0.0])
    k = np.array([0.0, 0.0, 0.0, 1.0])
    return [
        [("L", i)],
        [("L", j)],
        [("L", k)],
        [("R", phase_unit(np.pi / 2))],
        [("R", phase_unit(np.pi / 3))],
        [("L", i), ("R", phase_unit(np.pi / 2))],
        [("R", phase_unit(np.pi / 2)), ("L", j)],
        [("L", i), ("L", j)],
    ]


def _value_signature(topo: FluxTopograph) -> tuple[float, float, float, float]:
    v = topo.values
    return (
        float(np.mean(v)),
        float(np.std(v)),
        float(np.min(v)),
        float(np.max(v)),
    )


def classify_topograph_type(
    topo: FluxTopograph,
    *,
    gauge_sequences: list[list[tuple[str, Array]]] | None = None,
    period_tol: float = 1e-2,
) -> dict:
    """Heuristic four-type classification (Model / OP3).

    Uses separator mass, value variance, and best periodicity under a small
    gauge dictionary — *not* a classical discriminant computation.
    """
    seps = detect_separators(topo, mode="sign")
    n_sep = sum(len(c) for c in seps)
    n_comp = len(seps)
    var = float(np.var(topo.values))
    rng = float(np.ptp(topo.values))
    mean_abs = float(np.mean(np.abs(topo.values)))

    seqs = gauge_sequences if gauge_sequences is not None else standard_gauge_set()[:5]
    best_period = -1.0
    best_pt = float("inf")
    for seq in seqs:
        sc = periodicity_score(topo, seq, max_periods=4, tol=period_tol)
        if sc["period_found"] > 0:
            best_period = sc["period_found"] if best_period < 0 else min(best_period, sc["period_found"])
        best_pt = min(best_pt, sc["best_point_nn_mean"])

    # Decision tree (explicitly heuristic)
    if rng < 1e-9 or var < 1e-12:
        typ = "0-hyperbolic"
        reason = "nearly constant values"
    elif n_sep == 0 and var < 0.05:
        typ = "parabolic"
        reason = "no sign separators, low variation"
    elif best_period > 0 and n_sep > 0:
        typ = "hyperbolic"
        reason = "periodic under gauge + nonempty separators"
    elif n_comp <= 2 and n_sep < max(4, len(topo.points) // 20):
        typ = "elliptic"
        reason = "few separator components / bounded separator mass"
    elif best_period > 0:
        typ = "hyperbolic"
        reason = "periodic under gauge"
    else:
        typ = "parabolic"
        reason = "default transitional / non-periodic"

    return {
        "type": typ,
        "reason": reason,
        "n_separator_edges": n_sep,
        "n_separator_components": n_comp,
        "value_variance": var,
        "value_range": rng,
        "mean_abs_value": mean_abs,
        "best_period_found": best_period,
        "best_point_nn_mean": best_pt,
        "signature": _value_signature(topo),
    }


def equivalence_distance(
    topo_a: FluxTopograph,
    topo_b: FluxTopograph,
) -> dict[str, float]:
    """Coarse distance between two topographs (Model).

    Compares sorted value multisets and sorted point-cloud distance.
    """
    va = np.sort(topo_a.values)
    vb = np.sort(topo_b.values)
    n = max(len(va), len(vb))
    if len(va) < n:
        va = np.pad(va, (0, n - len(va)), constant_values=va[-1] if len(va) else 0.0)
    if len(vb) < n:
        vb = np.pad(vb, (0, n - len(vb)), constant_values=vb[-1] if len(vb) else 0.0)
    val_d = float(np.linalg.norm(va - vb) / (np.linalg.norm(va) + 1e-12))
    pt_d = _point_cloud_distance(topo_a.points, topo_b.points)
    return {
        "value_multiset_rel": val_d,
        "point_nn_mean": pt_d,
        "combined": val_d + pt_d,
    }


def reduced_representative(
    topo: FluxTopograph,
    gauge_sequences: list[list[tuple[str, Array]]] | None = None,
) -> tuple[FluxTopograph, dict]:
    """Pick a reduced rep: minimize value variance among gauge orbit (Model)."""
    seqs = gauge_sequences if gauge_sequences is not None else standard_gauge_set()
    best = topo
    best_var = float(np.var(topo.values))
    best_meta = {"source": "original", "variance": best_var, "sequence": ()}
    # also try applying each sequence once and compositions of length 1 only
    for seq in seqs:
        cand = apply_gauge_to_topograph(topo, seq, recompute_functional=True)
        var = float(np.var(cand.values))
        # secondary: fewer separator edges preferred when variance ties
        if var < best_var - 1e-15:
            best = cand
            best_var = var
            best_meta = {"source": "gauge", "variance": best_var, "sequence": seq}
    return best, best_meta


def enumerate_reduced(
    topo: FluxTopograph,
    gauge_sequences: list[list[tuple[str, Array]]] | None = None,
    *,
    dedup_tol: float = 1e-3,
    max_two_step: int = 3,
) -> list[dict]:
    """Enumerate approximate reduced orbit representatives (Model / OP3).

    Generates a bounded gauge orbit under ``standard_gauge_set`` (and identity),
    reduces each by variance, and deduplicates by ``equivalence_distance``.
    """
    seqs = gauge_sequences if gauge_sequences is not None else standard_gauge_set()[:6]
    # identity + each generator + limited two-step products
    orbit_seeds: list[tuple[FluxTopograph, str]] = [(topo, "id")]
    for seq in seqs:
        orbit_seeds.append(
            (apply_gauge_to_topograph(topo, seq, recompute_functional=True), f"1:{seq[0][0]}")
        )
    for seq in seqs[:max_two_step]:
        for seq2 in seqs[:max_two_step]:
            composed = seq + seq2
            orbit_seeds.append(
                (
                    apply_gauge_to_topograph(topo, composed, recompute_functional=True),
                    f"2:{seq[0][0]}+{seq2[0][0]}",
                )
            )

    # cheap classification sequences (subset)
    clf_seqs = seqs[:4]
    reduced_list: list[dict] = []
    for cand, tag in orbit_seeds:
        rep, meta = reduced_representative(cand, gauge_sequences=seqs)
        is_new = True
        for existing in reduced_list:
            d = equivalence_distance(rep, existing["topograph"])
            if d["combined"] <= dedup_tol:
                is_new = False
                break
        if is_new:
            clf = classify_topograph_type(rep, gauge_sequences=clf_seqs)
            reduced_list.append(
                {
                    "topograph": rep,
                    "classification": clf,
                    "reduction_meta": meta,
                    "seed_tag": tag,
                    "magic_island_score": magic_island_score(rep, gauge_sequences=clf_seqs),
                }
            )
    return reduced_list


def magic_island_score(
    topo: FluxTopograph,
    gauge_sequences: list[list[tuple[str, Array]]] | None = None,
) -> dict[str, float]:
    """Heuristic island score from periodicity + low variation + separator order.

    Higher is more “Magic Island–like” in the pedagogical Model.
    """
    clf = classify_topograph_type(topo, gauge_sequences=gauge_sequences)
    # normalize ingredients to [0,1]-ish
    period_term = 1.0 if clf["best_period_found"] > 0 else max(0.0, 1.0 - min(clf["best_point_nn_mean"], 1.0))
    # low variance preferred for compact islands; mild variance ok for hyperbolic
    var = clf["value_variance"]
    var_term = float(np.exp(-3.0 * var))
    # separator structure present but not explosive
    n_sep = clf["n_separator_edges"]
    n = max(len(topo.points), 1)
    sep_frac = n_sep / n
    sep_term = float(np.exp(-((sep_frac - 0.15) ** 2) / (2 * 0.12**2)))
    type_bonus = {
        "elliptic": 0.25,
        "hyperbolic": 0.2,
        "0-hyperbolic": 0.35,
        "parabolic": 0.05,
    }.get(clf["type"], 0.0)
    score = 0.4 * period_term + 0.3 * var_term + 0.2 * sep_term + type_bonus
    return {
        "score": float(score),
        "period_term": float(period_term),
        "variance_term": float(var_term),
        "separator_term": float(sep_term),
        "type_bonus": float(type_bonus),
        "type": clf["type"],  # type: ignore[dict-item]
    }


def class_number_analogue(
    topo: FluxTopograph,
    gauge_sequences: list[list[tuple[str, Array]]] | None = None,
    *,
    dedup_tol: float = 1e-3,
) -> dict:
    """Count inequivalent reduced reps — class-number-like integer (Model)."""
    reduced = enumerate_reduced(topo, gauge_sequences=gauge_sequences, dedup_tol=dedup_tol)
    by_type: dict[str, int] = {}
    for r in reduced:
        t = r["classification"]["type"]
        by_type[t] = by_type.get(t, 0) + 1
    return {
        "class_number_analogue": len(reduced),
        "by_type": by_type,
        "reduced": reduced,
    }
