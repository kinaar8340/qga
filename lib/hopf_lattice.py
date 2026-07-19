"""Pedagogical gauged Hopf lattice helpers for Kingdom Come / QGA Chapters 3–4.

This module is part of the *book* project (``~/Projects/qga``). It is **not**
yet merged into ``kingdom.core.lattice`` (which currently holds only
``LatticeConfig``; dynamical demos live in ``kingdom.simulations.lattice``).

All adjacency / mediant rules here are **Model candidates** for Open Problem 1.
Symmetry helpers (gauge sequences, orbits, equivariance scores) support Chapter 4.
"""

from __future__ import annotations

from itertools import product
from typing import Iterable

import numpy as np

Array = np.ndarray

# ---------------------------------------------------------------------------
# Algebra (minimal, self-contained)
# ---------------------------------------------------------------------------


def q_mult(a: Array, b: Array) -> Array:
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return np.array(
        [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ],
        dtype=float,
    )


def q_norm2(q: Array) -> float:
    return float(np.dot(q, q))


def q_normalize(q: Array, eps: float = 1e-12) -> Array:
    n = np.linalg.norm(q)
    if n < eps:
        return np.array([1.0, 0.0, 0.0, 0.0])
    return q / n


def hopf_map_classical(q: Array) -> Array:
    r"""Classical complex Hopf map (preferred for lattice pedagogy).

    Identify \(z_1 = w + ix\), \(z_2 = y + iz\). Returns a unit vector in \(\mathbb{R}^3\).
    See Chapter 2 convention note for comparison with the portal real form.
    """
    w, x, y, z = [float(c) for c in q]
    z1 = complex(w, x)
    z2 = complex(y, z)
    y1 = abs(z1) ** 2 - abs(z2) ** 2
    cross = 2.0 * (z1.conjugate() * z2)
    y2 = cross.real
    y3 = cross.imag
    vec = np.array([y1, y2, y3], dtype=float)
    n = np.linalg.norm(vec)
    if n < 1e-14:
        return np.array([1.0, 0.0, 0.0])
    return vec / n


def hopf_map_kc(q: Array) -> Array:
    """Kingdom Come real-form Hopf map (portal continuity; see Ch. 2)."""
    x1, x2, x3, x4 = q
    y1 = x1**2 - x2**2
    y2 = 2.0 * x1 * x2
    y3 = 2.0 * (x3 * x4 + x1 * x2)
    y = np.array([y1, y2, y3], dtype=float)
    n = np.linalg.norm(y)
    if n < 1e-14:
        return np.array([1.0, 0.0, 0.0])
    return y / n


def stereographic(q: Array, scale: float = 2.0) -> Array:
    x1, x2, x3, x4 = q
    denom = 1.0 - x4 + 1e-12
    return scale * np.array([x2 / denom, x3 / denom, x1 / denom])


# ---------------------------------------------------------------------------
# Hurwitz units (24 points on S³)
# ---------------------------------------------------------------------------


def _hurwitz_units() -> Array:
    units: list[list[float]] = []
    # ±1, ±i, ±j, ±k
    for i in range(4):
        for sgn in (-1.0, 1.0):
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = sgn
            units.append(v)
    # (±1 ± i ± j ± k)/2
    for signs in product([-0.5, 0.5], repeat=4):
        units.append(list(signs))
    arr = np.array(units, dtype=float)
    rounded = np.round(arr, 8)
    _, idx = np.unique(rounded, axis=0, return_index=True)
    return arr[np.sort(idx)]


HURWITZ_UNITS: Array = _hurwitz_units()
assert len(HURWITZ_UNITS) == 24, len(HURWITZ_UNITS)


def hopf_project_points(points: Array, *, convention: str = "classical") -> Array:
    """Map (N,4) unit quaternions to (N,3) base points on S².

    ``convention='classical'`` (default) uses the complex Hopf map.
    ``convention='kc'`` uses the Kingdom Come real form from Ch. 2.
    """
    points = np.asarray(points, dtype=float)
    fn = hopf_map_classical if convention == "classical" else hopf_map_kc
    return np.stack([fn(q) for q in points], axis=0)


def left_multiply(points: Array, u: Array) -> Array:
    u = q_normalize(np.asarray(u, dtype=float))
    return np.stack([q_normalize(q_mult(u, q)) for q in points], axis=0)


def right_multiply(points: Array, u: Array) -> Array:
    u = q_normalize(np.asarray(u, dtype=float))
    return np.stack([q_normalize(q_mult(q, u)) for q in points], axis=0)


# ---------------------------------------------------------------------------
# Denser sampling via Hopf angles (portal-compatible)
# ---------------------------------------------------------------------------


def hopf_coordinates(eta: float, xi1: float, xi2: float) -> Array:
    ce, se = np.cos(eta), np.sin(eta)
    c1, s1 = np.cos(xi1), np.sin(xi1)
    c2, s2 = np.cos(xi2), np.sin(xi2)
    return np.array([ce * c1, ce * s1, se * c2, se * s2], dtype=float)


def sample_angle_lattice(
    n_eta: int = 4,
    n_xi1: int = 8,
    n_xi2: int = 8,
    eta_range: tuple[float, float] = (0.2, 1.2),
) -> Array:
    """Cartesian product sample of Hopf angles → unit quaternions on S³.

    This is a **software sampling lattice**, not the Hurwitz order. Useful for
    visualizing fibers, candidate adjacency, and gauge actions at higher density.
    """
    etas = np.linspace(eta_range[0], eta_range[1], n_eta)
    xi1s = np.linspace(0.0, 2.0 * np.pi, n_xi1, endpoint=False)
    xi2s = np.linspace(0.0, 2.0 * np.pi, n_xi2, endpoint=False)
    pts = [
        hopf_coordinates(float(e), float(a), float(b))
        for e in etas
        for a in xi1s
        for b in xi2s
    ]
    return np.stack(pts, axis=0)


# ---------------------------------------------------------------------------
# Candidate adjacency (Model — Open Problem 1)
# ---------------------------------------------------------------------------


def candidate_adjacency(
    points: Array,
    *,
    base_angle_thresh: float = 0.45,
    fiber_phase_bins: int = 8,
    same_fiber_eta_tol: float = 0.08,
    same_fiber_xi1_tol: float = 0.08,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """Return (along_fiber_edges, inter_fiber_edges) as index pairs.

    **Model candidate only (OP1).**

    - Along-fiber: points with nearly equal (η, ξ₁) estimates and neighboring ξ₂.
    - Inter-fiber: Hopf images within angular distance ``base_angle_thresh`` on S²,
      excluding along-fiber pairs.
    """
    points = np.asarray(points, dtype=float)
    n = len(points)
    # Recover rough angles from coordinates (portal chart)
    # x1=ce c1, x2=ce s1, x3=se c2, x4=se s2
    x1, x2, x3, x4 = points.T
    eta = np.arctan2(np.sqrt(x3**2 + x4**2), np.sqrt(x1**2 + x2**2))
    xi1 = np.arctan2(x2, x1)
    xi2 = np.arctan2(x4, x3)
    base = hopf_project_points(points)

    along: list[tuple[int, int]] = []
    inter: list[tuple[int, int]] = []

    # along-fiber: same (eta, xi1) bucket, consecutive xi2 on circle
    phase_step = 2.0 * np.pi / max(fiber_phase_bins, 1)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(eta[i] - eta[j]) > same_fiber_eta_tol:
                continue
            dxi1 = abs(((xi1[i] - xi1[j] + np.pi) % (2 * np.pi)) - np.pi)
            if dxi1 > same_fiber_xi1_tol:
                continue
            dxi2 = abs(((xi2[i] - xi2[j] + np.pi) % (2 * np.pi)) - np.pi)
            if dxi2 <= phase_step * 1.25 + 1e-9:
                along.append((i, j))

    along_set = set(along) | {(b, a) for a, b in along}

    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in along_set:
                continue
            # angular distance on S²: arccos of dot product
            c = float(np.clip(np.dot(base[i], base[j]), -1.0, 1.0))
            ang = float(np.arccos(c))
            if ang <= base_angle_thresh:
                inter.append((i, j))

    return along, inter


def discrete_flux_cycle(edge_indices: Iterable[tuple[int, int]], value: int = 1) -> dict[tuple[int, int], int]:
    """Assign constant oriented flux on a list of edges (simple closed walk)."""
    flux: dict[tuple[int, int], int] = {}
    for a, b in edge_indices:
        flux[(a, b)] = value
        flux[(b, a)] = -value
    return flux


# ---------------------------------------------------------------------------
# Symmetries / gauge sequences (Chapter 4)
# ---------------------------------------------------------------------------


def phase_unit(theta: float) -> Array:
    """Unit quaternion for a pure right-phase (rotation in the 1–k plane)."""
    return np.array([np.cos(theta / 2.0), 0.0, 0.0, np.sin(theta / 2.0)], dtype=float)


def chordal_distance_s3(q: Array, r: Array, *, identify_antipodes: bool = False) -> float:
    """Euclidean distance in R⁴; optionally min(|q−r|, |q+r|) for rotation sense."""
    q = np.asarray(q, dtype=float)
    r = np.asarray(r, dtype=float)
    d = float(np.linalg.norm(q - r))
    if identify_antipodes:
        d = min(d, float(np.linalg.norm(q + r)))
    return d


def apply_gauge_step(points: Array, side: str, unit: Array) -> Array:
    """Apply one left (``'L'``) or right (``'R'``) multiplication to all points."""
    side = side.upper()
    if side == "L":
        return left_multiply(points, unit)
    if side == "R":
        return right_multiply(points, unit)
    raise ValueError("side must be 'L' or 'R'")


def apply_gauge_sequence(
    points: Array,
    sequence: list[tuple[str, Array]],
    *,
    record: bool = True,
) -> list[Array] | Array:
    """Apply a sequence of (side, unit) gauge steps.

    Parameters
    ----------
    points :
        Array of shape (N, 4) or a single quaternion (4,).
    sequence :
        List of ``('L'|'R', unit_quaternion)`` steps.
    record :
        If True (default), return the list of configurations after each step
        (including the initial configuration as index 0). If False, return only
        the final configuration.
    """
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        pts = pts.reshape(1, 4)
    history = [pts.copy()]
    cur = pts
    for side, unit in sequence:
        cur = apply_gauge_step(cur, side, unit)
        history.append(cur.copy())
    if record:
        return history
    return cur


def orbit_of_point(
    q: Array,
    sequence: list[tuple[str, Array]],
    *,
    max_periods: int = 48,
    tol: float = 1e-6,
    identify_antipodes: bool = True,
) -> list[Array]:
    """Iterate a gauge sequence on a single point until approximate return.

    Returns the list of positions starting at ``q`` and ending at the first
    approximate return (inclusive), or after ``max_periods`` applications of the
    full sequence if no return is found.
    """
    q0 = q_normalize(np.asarray(q, dtype=float).reshape(4))
    orbit = [q0.copy()]
    cur = q0.copy()
    for _ in range(max_periods):
        for side, unit in sequence:
            cur = apply_gauge_step(cur.reshape(1, 4), side, unit)[0]
            orbit.append(cur.copy())
        if chordal_distance_s3(cur, q0, identify_antipodes=identify_antipodes) <= tol:
            break
    return orbit


def permutes_hurwitz_units(unit: Array, *, side: str = "L", tol: float = 1e-8) -> bool:
    """True if left/right multiplication by ``unit`` permutes the 24 Hurwitz units."""
    moved = apply_gauge_step(HURWITZ_UNITS, side, unit)
    # each image should match some original unit
    for m in moved:
        if not any(chordal_distance_s3(m, u) <= tol for u in HURWITZ_UNITS):
            return False
    return True


def adjacency_equivariance_score(
    points: Array,
    unit: Array,
    *,
    side: str = "L",
    **adj_kwargs,
) -> dict[str, float]:
    """Measure how well candidate_adjacency is preserved by a gauge action.

    **OP1 diagnostic (Model).** Returns fractions of along-fiber and inter-fiber
    edges whose images remain edges of the same type after the gauge map.
    """
    points = np.asarray(points, dtype=float)
    along, inter = candidate_adjacency(points, **adj_kwargs)
    moved = apply_gauge_step(points, side, unit)

    # map each original index to nearest point in the moved cloud... actually
    # gauge maps points[i] -> moved[i] with the same index ordering.
    along_m, inter_m = candidate_adjacency(moved, **adj_kwargs)
    along_set = set(along) | {(b, a) for a, b in along}
    inter_set = set(inter) | {(b, a) for a, b in inter}
    along_m_set = set(along_m) | {(b, a) for a, b in along_m}
    inter_m_set = set(inter_m) | {(b, a) for a, b in inter_m}

    def frac(edges, target):
        if not edges:
            return 1.0
        ok = sum(1 for e in edges if e in target or (e[1], e[0]) in target)
        return ok / len(edges)

    return {
        "along_preserved": frac(along, along_m_set),
        "inter_preserved": frac(inter, inter_m_set),
        "n_along": float(len(along)),
        "n_inter": float(len(inter)),
    }


def transform_flux(
    flux: dict[tuple[int, int], int],
    index_map: dict[int, int],
) -> dict[tuple[int, int], int]:
    """Push flux forward under a vertex index permutation/map."""
    out: dict[tuple[int, int], int] = {}
    for (a, b), val in flux.items():
        if a not in index_map or b not in index_map:
            continue
        out[(index_map[a], index_map[b])] = val
    return out


def nearest_index_map(src: Array, dst: Array) -> dict[int, int]:
    """Map each index i of src to argmin_j |src[i]−dst[j]| (for re-snap diagnostics)."""
    src = np.asarray(src, dtype=float)
    dst = np.asarray(dst, dtype=float)
    mapping: dict[int, int] = {}
    for i, p in enumerate(src):
        d = np.linalg.norm(dst - p, axis=1)
        mapping[i] = int(np.argmin(d))
    return mapping
