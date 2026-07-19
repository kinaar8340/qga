#!/usr/bin/env python3
"""Generate Chapter 4 figures: symmetries of the gauged Hopf lattice."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "book" / "figures"
sys.path.insert(0, str(ROOT))

from lib.hopf_lattice import (  # noqa: E402
    HURWITZ_UNITS,
    hopf_coordinates,
    hopf_project_points,
    left_multiply,
    orbit_of_point,
    phase_unit,
    q_normalize,
    right_multiply,
    stereographic,
)


def _sphere(ax, alpha=0.08):
    u = np.linspace(0, 2 * np.pi, 24)
    v = np.linspace(0, np.pi, 14)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(xs, ys, zs, alpha=alpha, color="#2b6cb0", edgecolor="none")


def fig_4_1() -> None:
    pts = HURWITZ_UNITS
    i = np.array([0.0, 1.0, 0.0, 0.0])
    u_r = phase_unit(np.pi / 5)
    base0 = hopf_project_points(pts)
    baseL = hopf_project_points(left_multiply(pts, i))
    baseR = hopf_project_points(right_multiply(pts, u_r))
    st0 = np.stack([stereographic(q) for q in pts], axis=0)
    stR = np.stack([stereographic(q) for q in right_multiply(pts, u_r)], axis=0)

    fig = plt.figure(figsize=(11, 4.2))
    ax = fig.add_subplot(1, 3, 1, projection="3d")
    _sphere(ax)
    ax.scatter(base0[:, 0], base0[:, 1], base0[:, 2], c="#718096", s=28, label="orig")
    ax.scatter(baseL[:, 0], baseL[:, 1], baseL[:, 2], c="#c05621", s=28, label="left i")
    ax.set_title("Base $S^2$: left mult. by $i$")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax = fig.add_subplot(1, 3, 2, projection="3d")
    _sphere(ax)
    ax.scatter(base0[:, 0], base0[:, 1], base0[:, 2], c="#718096", s=28)
    ax.scatter(baseR[:, 0], baseR[:, 1], baseR[:, 2], c="#2f855a", s=28)
    ax.set_title("Base $S^2$: right phase")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax = fig.add_subplot(1, 3, 3, projection="3d")
    ax.scatter(st0[:, 0], st0[:, 1], st0[:, 2], c="#718096", s=22)
    ax.scatter(stR[:, 0], stR[:, 1], stR[:, 2], c="#2f855a", s=22)
    for a, b in zip(st0, stR):
        ax.plot([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color="#9ae6b4", lw=0.6, alpha=0.6)
    ax.set_title("Stereo $S^3$: right phase displacements")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    fig.suptitle(
        "Figure 4.1 — Left vs right gauge actions on base and total space",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig4_1_left_right_symmetries.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_4_2() -> None:
    i = np.array([0.0, 1.0, 0.0, 0.0])
    j = np.array([0.0, 0.0, 1.0, 0.0])
    seq = [("R", phase_unit(np.pi / 3)), ("L", i), ("R", phase_unit(np.pi / 3)), ("L", j)]
    q0 = HURWITZ_UNITS[5]
    orbit = orbit_of_point(q0, seq, max_periods=24, tol=1e-5)
    st = np.stack([stereographic(q) for q in orbit], axis=0)
    base = hopf_project_points(np.stack(orbit, axis=0))

    fig = plt.figure(figsize=(10, 4.5))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.plot(st[:, 0], st[:, 1], st[:, 2], color="#2b6cb0", lw=1.5, alpha=0.8)
    ax.scatter(st[0, 0], st[0, 1], st[0, 2], c="#c05621", s=60, label="start")
    ax.scatter(st[-1, 0], st[-1, 1], st[-1, 2], c="#2f855a", s=40, label="end")
    ax.set_title(f"Stereo orbit ({len(orbit)} samples)")
    ax.legend(fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax = fig.add_subplot(1, 2, 2, projection="3d")
    _sphere(ax)
    ax.plot(base[:, 0], base[:, 1], base[:, 2], color="#c05621", lw=1.5)
    ax.scatter(base[0, 0], base[0, 1], base[0, 2], c="#2b6cb0", s=50)
    ax.set_title("Base track of the same orbit")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    fig.suptitle(
        "Figure 4.2 — Periodic / long orbit under a combined gauge sequence",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig4_2_periodic_orbit.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_4_3() -> None:
    """Glide-like helical path: right phase + left shift iterated."""
    u_left = q_normalize(np.array([np.cos(0.15), np.sin(0.15), 0.0, 0.0]))
    u_right = phase_unit(0.35)
    seq = [("R", u_right), ("L", u_left)]
    q0 = hopf_coordinates(0.55, 0.2, 0.0)
    orbit = orbit_of_point(q0, seq, max_periods=40, tol=1e-4, identify_antipodes=True)
    st = np.stack([stereographic(q) for q in orbit], axis=0)
    base = hopf_project_points(np.stack(orbit, axis=0))

    fig = plt.figure(figsize=(10, 4.5))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    t = np.linspace(0, 1, len(st))
    for k in range(len(st) - 1):
        ax.plot(
            st[k : k + 2, 0],
            st[k : k + 2, 1],
            st[k : k + 2, 2],
            color=plt.cm.viridis(t[k]),
            lw=2,
        )
    ax.set_title("Helical total-space path (stereo)")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax = fig.add_subplot(1, 2, 2, projection="3d")
    _sphere(ax)
    for k in range(len(base) - 1):
        ax.plot(
            base[k : k + 2, 0],
            base[k : k + 2, 1],
            base[k : k + 2, 2],
            color=plt.cm.plasma(t[k]),
            lw=2,
        )
    ax.set_title("Base drift (glide analogue)")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    fig.suptitle(
        "Figure 4.3 — Glide-like helical symmetry (right phase + left shift)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig4_3_glide_reflection_analogue.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_4_4() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # lattice dots
    for x in np.linspace(1.2, 8.8, 8):
        for y in np.linspace(1.0, 4.8, 5):
            ax.plot(x, y, "o", color="#cbd5e0", ms=4)

    t = np.linspace(0, 2 * np.pi, 200)
    # original flywheel
    cx, cy, rx, ry = 3.5, 2.9, 1.8, 1.2
    ax.plot(cx + rx * np.cos(t), cy + ry * np.sin(t), color="#c53030", lw=3)
    ax.annotate(
        "",
        xy=(cx + rx * np.cos(0.5), cy + ry * np.sin(0.5)),
        xytext=(cx + rx * np.cos(0.2), cy + ry * np.sin(0.2)),
        arrowprops=dict(arrowstyle="-|>", color="#c53030", lw=2, mutation_scale=12),
    )
    # image flywheel
    cx2 = 6.8
    ax.plot(cx2 + rx * np.cos(t), cy + ry * np.sin(t), color="#2b6cb0", lw=3)
    ax.annotate(
        "",
        xy=(cx2 + rx * np.cos(0.5), cy + ry * np.sin(0.5)),
        xytext=(cx2 + rx * np.cos(0.2), cy + ry * np.sin(0.2)),
        arrowprops=dict(arrowstyle="-|>", color="#2b6cb0", lw=2, mutation_scale=12),
    )
    ax.annotate(
        "",
        xy=(5.2, 2.9),
        xytext=(4.6, 2.9),
        arrowprops=dict(arrowstyle="-|>", color="#4a5568", lw=2, mutation_scale=14),
    )
    ax.text(5.0, 3.5, r"gauge $g$", ha="center", fontsize=11, color="#4a5568")
    ax.text(3.5, 5.2, "flywheel $\\Phi$", ha="center", fontsize=11, color="#c53030", fontweight="bold")
    ax.text(6.8, 5.2, r"image $g\cdot\Phi$", ha="center", fontsize=11, color="#2b6cb0", fontweight="bold")
    ax.text(5.0, 0.45, "same topological type (linking / winding preserved)", ha="center", fontsize=9, color="#4a5568")
    ax.set_title(
        "Figure 4.4 — Gauge symmetry mapping a flux flywheel to an equivalent cycle",
        fontsize=12,
        fontweight="bold",
    )
    fig.savefig(FIG_DIR / "fig4_4_symmetry_on_flywheel.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def aux_4_1() -> None:
    pts = HURWITZ_UNITS
    base = hopf_project_points(pts)
    labels = []
    # crude labels
    names = []
    for q in pts:
        w, x, y, z = np.round(q, 5)
        if abs(abs(w) - 1) < 1e-4 and abs(x) + abs(y) + abs(z) < 1e-4:
            names.append(f"{'+' if w > 0 else '-'}1")
        elif abs(abs(x) - 1) < 1e-4:
            names.append(f"{'+' if x > 0 else '-'}i")
        elif abs(abs(y) - 1) < 1e-4:
            names.append(f"{'+' if y > 0 else '-'}j")
        elif abs(abs(z) - 1) < 1e-4:
            names.append(f"{'+' if z > 0 else '-'}k")
        else:
            names.append("½")

    fig = plt.figure(figsize=(9.5, 4.5))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    st = np.stack([stereographic(q) for q in pts], axis=0)
    colors = ["#2b6cb0" if n != "½" else "#c05621" for n in names]
    ax.scatter(st[:, 0], st[:, 1], st[:, 2], c=colors, s=50)
    ax.set_title("Hurwitz units in stereo $S^3$\n(blue = $\\pm1,\\pm i,\\pm j,\\pm k$; orange = half)")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax = fig.add_subplot(1, 2, 2, projection="3d")
    _sphere(ax)
    ax.scatter(base[:, 0], base[:, 1], base[:, 2], c=colors, s=50)
    ax.set_title("Same units projected to base $S^2$")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    fig.suptitle(
        "Auxiliary Figure A4.1 — Discrete gauge group elements (24 Hurwitz units)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "aux4_1_gauge_group_elements.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_4_1()
    fig_4_2()
    fig_4_3()
    fig_4_4()
    aux_4_1()
    print(f"Wrote Chapter 4 figures to {FIG_DIR}")
    for p in sorted(FIG_DIR.glob("fig4_*")) + sorted(FIG_DIR.glob("aux4_*")):
        print(f"  {p.name}: {p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
