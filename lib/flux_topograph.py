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
    discrete_flux_cycle,
    hopf_fiber_clusters,
    hopf_project_points,
    phase_unit,
    q_normalize,
    structure_group_adjacency,
    structure_group_phase,
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
    adjacency: str | None = None,
    op1_row: dict | None = None,
) -> FluxTopograph:
    """Build a flux topograph on lattice points.

    OP2 analysis: ``adjacency="structure_group"`` only. Do not pass
    ``adjacency="candidate"``. Book figures may still pass explicit edges
    from the frozen candidate without this flag.

    Parameters
    ----------
    points :
        Array (N, 4) of unit quaternions / S³ samples.
    edges :
        Optional undirected edges. Incompatible with ``adjacency=``.
    functional :
        Named functional or callable ``points -> values``.
    adjacency :
        ``"structure_group"`` (Model 2) or None (explicit ``edges``).
    op1_row :
        Optional attached OP1 JSON (census / rule). Stored in ``meta``.
    """
    points = np.asarray(points, dtype=float)
    if adjacency == "candidate":
        raise ValueError(
            "OP2 analysis cannot use candidate_adjacency (ξ2-circle on Lang). "
            "Use adjacency='structure_group' and attach that sample's OP1 JSON."
        )
    if adjacency is not None and adjacency != "structure_group":
        raise ValueError(f"unknown adjacency {adjacency!r}")
    if adjacency == "structure_group" and edges is not None:
        raise ValueError(
            "Do not mix Model 2 along-edges with an explicit edge list "
            "(including candidate inter-edges). Pass adjacency='structure_group' "
            "XOR edges=..."
        )
    along: list[tuple[int, int]] = []
    inter: list[tuple[int, int]] = []
    if adjacency == "structure_group":
        along, inter = structure_group_adjacency(points)
        edges = along + inter
    if callable(functional) and not isinstance(functional, str):
        values = np.asarray(functional(points), dtype=float)
        fname = getattr(functional, "__name__", "custom")
    else:
        values = _functional_values(points, functional)  # type: ignore[arg-type]
        fname = str(functional)
    meta: dict = {"n": len(points), "adjacency": adjacency or "explicit_edges"}
    if along or inter:
        meta["n_along"] = len(along)
        meta["n_inter"] = len(inter)
        meta["along"] = along
        meta["inter"] = inter
    if op1_row is not None:
        meta["op1_row"] = {
            "schema": op1_row.get("schema"),
            "set": op1_row.get("set"),
            "rule": op1_row.get("rule"),
            "op1_status": op1_row.get("op1_status"),
            "fiber_census": (op1_row.get("experiment1") or {}).get("fiber_census"),
        }
    return FluxTopograph(
        points=points,
        values=values,
        edges=list(edges or []),
        functional=fname,
        meta=meta,
    )


def kirchhoff_report(
    flux: dict[tuple[int, int], int],
    n_vertices: int,
    *,
    support: list[tuple[int, int]] | None = None,
) -> dict:
    """Outgoing-sum residual of an oriented integer flux. Kirchhoff ⇔ max |r|=0."""
    outg = np.zeros(n_vertices, dtype=float)
    for (a, b), val in flux.items():
        if a < 0 or a >= n_vertices:
            continue
        outg[a] += float(val)
    max_abs = float(np.max(np.abs(outg))) if n_vertices else 0.0
    support_ok = True
    extra = 0
    if support is not None:
        allowed = set()
        for i, j in support:
            allowed.add((i, j))
            allowed.add((j, i))
        extra = sum(1 for e in flux if e not in allowed)
        support_ok = extra == 0
    return {
        "max_abs_residual": max_abs,
        "n_vertices_nonzero": int(np.sum(np.abs(outg) > 1e-12)),
        "kirchhoff": bool(max_abs < 1e-12),
        "n_oriented_keys": len(flux),
        "support_subset_of_skeleton": support_ok,
        "n_keys_outside_skeleton": extra,
    }


def fiber_cycle_flux(points: Array) -> dict[tuple[int, int], int]:
    """Kirchhoff Φ: +1 around each occupied left-U(1) fiber (oriented cycle)."""
    points = np.asarray(points, dtype=float)
    clusters = hopf_fiber_clusters(points)
    flux: dict[tuple[int, int], int] = {}
    for members in clusters:
        if len(members) < 2:
            continue
        ref = members[0]
        ordered = sorted(
            members, key=lambda k: structure_group_phase(points[ref], points[k])
        )
        walk = list(zip(ordered, ordered[1:] + ordered[:1]))
        flux.update(discrete_flux_cycle(walk, value=1))
    return flux


def detect_separators(
    topo: FluxTopograph,
    *,
    threshold: float | None = None,
    mode: Literal["sign", "strict_sign", "level"] = "sign",
) -> list[list[tuple[int, int]]]:
    """Detect separator edge components where the functional crosses a threshold.

    Returns a list of connected components; each component is a list of edges
    (i, j) with i < j.

    ``strict_sign`` is (v_i-thr)(v_j-thr)<0 only — zeros are not separators.
    OP2 harness uses that. Book labs keep ``sign`` (zeros count).
    """
    values = topo.values
    if threshold is None:
        threshold = 0.0 if mode in ("sign", "strict_sign") else float(np.median(values))

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
        if mode == "strict_sign":
            if (vi - threshold) * (vj - threshold) < 0:
                sep_edges.append((i, j))
        elif mode == "sign":
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
        rebuilt = build_flux_topograph(
            new_pts,
            edges=topo.edges,
            functional=topo.functional,  # type: ignore[arg-type]
        )
        rebuilt.meta = dict(topo.meta)
        rebuilt.meta["gauged"] = True
        return rebuilt
    return FluxTopograph(
        points=new_pts,
        values=topo.values.copy(),
        edges=list(topo.edges),
        functional=topo.functional,
        meta=dict(topo.meta),
    )


def _lexsort_rows(arr: Array) -> Array:
    arr = np.round(np.asarray(arr, dtype=float), 8)
    if arr.size == 0:
        return arr.reshape(0, arr.shape[-1] if arr.ndim == 2 else 1)
    keys = tuple(arr[:, k] for k in range(arr.shape[1] - 1, -1, -1))
    return arr[np.lexsort(keys)]


def _point_cloud_distance(a: Array, b: Array) -> float:
    """Symmetric multiset distance via lexicographically sorted *rows* (not axis=0)."""
    a_s = _lexsort_rows(a)
    b_s = _lexsort_rows(b)
    if a_s.shape != b_s.shape:
        n = max(len(a_s), len(b_s))
        if len(a_s) < n:
            a_s = np.vstack([a_s, np.repeat(a_s[-1:], n - len(a_s), axis=0)])
        if len(b_s) < n:
            b_s = np.vstack([b_s, np.repeat(b_s[-1:], n - len(b_s), axis=0)])
    return float(np.mean(np.linalg.norm(a_s - b_s, axis=1)))


def pole_level_sets(
    points: Array,
    functional: FunctionalName,
    *,
    same_fiber_base_tol: float = 1e-3,
) -> list[dict]:
    """One row per Hopf-base cluster: functional value on that fiber.

    On Λ0 these are the six octahedron poles. Values 0 are level sets, not
    sign-crossings — do not count them as separators.
    """
    points = np.asarray(points, dtype=float)
    clusters = hopf_fiber_clusters(points, same_fiber_base_tol=same_fiber_base_tol)
    base = hopf_project_points(points)
    values = _functional_values(points, functional)
    rows: list[dict] = []
    for members in clusters:
        i = members[0]
        v_on = values[np.asarray(members, dtype=int)]
        rows.append(
            {
                "base": [float(x) for x in base[i]],
                "multiplicity": int(len(members)),
                "value": float(values[i]),
                "value_min_on_fiber": float(np.min(v_on)),
                "value_max_on_fiber": float(np.max(v_on)),
            }
        )
    return rows


def periodicity_score(
    topo: FluxTopograph,
    sequence: list[tuple[str, Array]],
    *,
    max_periods: int = 8,
    tol: float = 1e-3,
    cut: Literal["strict_sign", "sign"] | None = None,
    cut_kind: str | None = None,
) -> dict:
    """Score gauge return, or (OP2) separator-cut periodicity.

    Default (``cut is None``): book lab — point-cloud / value-multiset return.
    ``cut="strict_sign"``: if the strict-sign separator set is empty, return
    ``status="undefined_or_vacuous"`` and do **not** invent crossings. If
    nonempty, report component counts before/after one application of
    ``sequence``. That number is Delaunay / cut periodicity, not Farey.
    """
    if cut is not None:
        seps0 = detect_separators(topo, mode=cut)
        n0 = len(seps0)
        e0 = sum(len(c) for c in seps0)
        kind = cut_kind or "separator_component_count"
        if n0 == 0:
            return {
                "status": "undefined_or_vacuous",
                "reason": "empty strict-sign cut; no river to periodize",
                "n_components_before": 0,
                "n_components_after": None,
                "n_separator_edges_before": 0,
                "n_separator_edges_after": None,
                "changed": False,
                "kind": kind,
                "not_farey_period": True,
            }
        topo1 = apply_gauge_to_topograph(topo, sequence, recompute_functional=True)
        seps1 = detect_separators(topo1, mode=cut)
        n1 = len(seps1)
        e1 = sum(len(c) for c in seps1)
        return {
            "status": "finite",
            "n_components_before": n0,
            "n_components_after": n1,
            "n_separator_edges_before": e0,
            "n_separator_edges_after": e1,
            "changed": bool(n0 != n1 or e0 != e1),
            "kind": kind,
            "not_farey_period": True,
        }

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
    mode: Literal["sign", "strict_sign", "level"] = "sign",
) -> dict[str, float]:
    """Compare separator edge counts before/after gauge (OP2 diagnostic)."""
    seps0 = detect_separators(topo, threshold=threshold, mode=mode)
    topo1 = apply_gauge_to_topograph(topo, sequence, recompute_functional=True)
    seps1 = detect_separators(topo1, threshold=threshold, mode=mode)
    n0 = sum(len(c) for c in seps0)
    n1 = sum(len(c) for c in seps1)
    return {
        "n_sep_edges_before": float(n0),
        "n_sep_edges_after": float(n1),
        "n_components_before": float(len(seps0)),
        "n_components_after": float(len(seps1)),
        "edge_count_ratio": (float(n1 / n0) if n0 else None),
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
            "kingdom.core.flux_flywheel required; "
            "python3 -m pip install -e '.[portal]' "
            "(kingdom-come is pinned to GitHub, not PYTHONPATH)"
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

    Aligned with the Conway–Hatcher table as a *proxy*, not a discriminant:
    elliptic = no river (no sign separators); hyperbolic = periodic river;
    0-hyperbolic = degenerate / nearly constant or unperiodized separators.
    Finite samples can still mislabel; this is a Software fact, not a theorem.
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

    # Decision tree aligned with Conway–Hatcher (still heuristic, not Δ)
    if rng < 1e-9 or var < 1e-12:
        typ = "0-hyperbolic"
        reason = "nearly constant values (degenerate / 0-hyperbolic proxy)"
    elif n_sep == 0:
        typ = "elliptic"
        reason = "no sign separators (no river) — Conway–Hatcher elliptic proxy"
    elif best_period > 0:
        typ = "hyperbolic"
        reason = "periodic under gauge + nonempty separators (river proxy)"
    elif n_sep > 0:
        typ = "0-hyperbolic"
        reason = "separators present but no period found (degenerate-river proxy)"
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
        "heuristic": True,
        "known_limitation": (
            "Not a discriminant computation; finite samples can still mislabel "
            "relative to Conway–Hatcher. Software fact, not a theorem."
        ),
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
