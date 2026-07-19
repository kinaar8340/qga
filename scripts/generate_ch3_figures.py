#!/usr/bin/env python3
"""Generate Chapter 3 figures: gauged Hopf lattice schematics + simulator still."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "book" / "figures"
sys.path.insert(0, str(ROOT))

from lib.hopf_lattice import (  # noqa: E402
    HURWITZ_UNITS,
    candidate_adjacency,
    hopf_project_points,
    left_multiply,
    right_multiply,
    sample_angle_lattice,
    stereographic,
)


def fig_3_1() -> None:
    pts = HURWITZ_UNITS
    stereo = np.stack([stereographic(q) for q in pts], axis=0)
    fig = plt.figure(figsize=(7.2, 6.0))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(stereo[:, 0], stereo[:, 1], stereo[:, 2], c="#2b6cb0", s=55, depthshade=True)
    # connect a few pairs for visual density
    for i in range(0, len(pts), 3):
        ax.plot(
            [stereo[i, 0], stereo[(i + 1) % len(pts), 0]],
            [stereo[i, 1], stereo[(i + 1) % len(pts), 1]],
            [stereo[i, 2], stereo[(i + 1) % len(pts), 2]],
            color="#90cdf4",
            lw=0.6,
            alpha=0.5,
        )
    ax.set_title(
        "Figure 3.1 — 24 Hurwitz units on $S^3$\n(stereographic view)",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.02)
    fig.savefig(FIG_DIR / "fig3_1_hurwitz_lattice_in_s3.png", dpi=160, facecolor="white")
    plt.close()


def fig_3_2() -> None:
    # denser sample for readable base scatter
    pts = sample_angle_lattice(n_eta=3, n_xi1=10, n_xi2=6)
    base = hopf_project_points(pts)
    # unique-ish base by rounding
    rounded = np.round(base, 4)
    _, idx = np.unique(rounded, axis=0, return_index=True)
    base_u = base[idx]
    fig = plt.figure(figsize=(9.5, 4.5))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    u = np.linspace(0, 2 * np.pi, 28)
    v = np.linspace(0, np.pi, 16)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(xs, ys, zs, alpha=0.1, color="#2b6cb0", edgecolor="none")
    ax.scatter(base_u[:, 0], base_u[:, 1], base_u[:, 2], c="#c05621", s=28)
    ax.set_title(r"Base samples $h(\Lambda)$ on $S^2$")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax2 = fig.add_subplot(1, 2, 2)
    # stereographic of total-space samples
    st = np.stack([stereographic(q) for q in pts[::3]], axis=0)
    ax2.scatter(st[:, 0], st[:, 1], s=8, c="#2b6cb0", alpha=0.7)
    ax2.set_aspect("equal")
    ax2.set_title(r"Total-space samples (stereo $xy$)")
    ax2.grid(True, alpha=0.3)
    fig.suptitle(
        "Figure 3.2 — Angle-sampled lattice projected via Hopf map",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig3_2_hopf_projected_lattice.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_3_3() -> None:
    pts = sample_angle_lattice(n_eta=2, n_xi1=6, n_xi2=8)
    along, inter = candidate_adjacency(pts, base_angle_thresh=0.55, fiber_phase_bins=8)
    st = np.stack([stereographic(q) for q in pts], axis=0)

    fig = plt.figure(figsize=(7.5, 6.2))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(st[:, 0], st[:, 1], st[:, 2], c="#4a5568", s=18, alpha=0.8)
    for i, j in inter[:80]:
        ax.plot(
            [st[i, 0], st[j, 0]],
            [st[i, 1], st[j, 1]],
            [st[i, 2], st[j, 2]],
            color="#3182ce",
            lw=0.8,
            alpha=0.45,
        )
    for i, j in along:
        ax.plot(
            [st[i, 0], st[j, 0]],
            [st[i, 1], st[j, 1]],
            [st[i, 2], st[j, 2]],
            color="#c53030",
            lw=1.6,
            alpha=0.85,
        )
    ax.set_title(
        "Figure 3.3 — Candidate adjacency (Model / OP1)\n"
        "red = along-fiber; blue = inter-fiber",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.02)
    fig.savefig(FIG_DIR / "fig3_3_adjacency_and_fibers.png", dpi=160, facecolor="white")
    plt.close()


def fig_3_4() -> None:
    pts = HURWITZ_UNITS
    u_left = np.array([0.0, 1.0, 0.0, 0.0])  # i
    # small right phase ~ rotation in 1-k plane
    angle = np.pi / 6
    u_right = np.array([np.cos(angle / 2), 0.0, 0.0, np.sin(angle / 2)])
    base0 = hopf_project_points(pts)
    baseL = hopf_project_points(left_multiply(pts, u_left))
    ptsR = right_multiply(pts, u_right)
    baseR = hopf_project_points(ptsR)

    fig = plt.figure(figsize=(10, 4.2))
    for col, base, title in [
        (1, base0, "original base points"),
        (2, baseL, r"after left mult. by $i$"),
        (3, baseR, "after small right mult."),
    ]:
        ax = fig.add_subplot(1, 3, col, projection="3d")
        u = np.linspace(0, 2 * np.pi, 24)
        v = np.linspace(0, np.pi, 14)
        xs = np.outer(np.cos(u), np.sin(v))
        ys = np.outer(np.sin(u), np.sin(v))
        zs = np.outer(np.ones_like(u), np.cos(v))
        ax.plot_surface(xs, ys, zs, alpha=0.08, color="#2b6cb0", edgecolor="none")
        ax.scatter(base[:, 0], base[:, 1], base[:, 2], c="#c05621", s=30)
        ax.set_title(title, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
    fig.suptitle(
        "Figure 3.4 — Left vs right multiplications as gauge actions",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig3_4_gauge_action.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_3_5() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # lattice dots
    xs = np.linspace(1.5, 8.5, 7)
    ys = np.linspace(1.2, 4.5, 5)
    for x in xs:
        for y in ys:
            ax.plot(x, y, "o", color="#a0aec0", ms=5)

    # flywheel loop
    t = np.linspace(0, 2 * np.pi, 200)
    cx, cy, rx, ry = 5.0, 2.9, 2.6, 1.5
    ax.plot(cx + rx * np.cos(t), cy + ry * np.sin(t), color="#c53030", lw=3.5, solid_capstyle="round")
    # arrow on loop
    ax.annotate(
        "",
        xy=(cx + rx * np.cos(0.4), cy + ry * np.sin(0.4)),
        xytext=(cx + rx * np.cos(0.15), cy + ry * np.sin(0.15)),
        arrowprops=dict(arrowstyle="-|>", color="#c53030", lw=2.5, mutation_scale=14),
    )
    # linked fiber hint
    ax.plot(cx + 1.2 * np.cos(t), cy + 0.7 * np.sin(t) + 0.3, color="#2b6cb0", lw=2, ls="--", alpha=0.8)
    ax.text(5, 5.4, "Flux flywheel (closed circulating flux)", ha="center", fontsize=12, fontweight="bold")
    ax.text(5, 0.45, "red = protected cycle; blue dashed = linked fiber support (schematic)", ha="center", fontsize=9, color="#4a5568")
    ax.set_title("Figure 3.5 — Flux flywheel on the gauged Hopf lattice (schematic)", fontsize=12, fontweight="bold")
    fig.savefig(FIG_DIR / "fig3_5_flux_flywheel_schematic.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def aux_3_1() -> None:
    """Still from two-gyro lattice comparison if kingdom available; else synthetic."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        sys.path.insert(0, str(Path.home() / "Projects" / "flux_hopf_lib" / "src"))
        sys.path.insert(0, str(Path.home() / "Projects" / "kingdom" / "src"))
        from kingdom.core.lattice import LatticeConfig
        from kingdom.simulations.lattice import TwoGyroLattice

        stable = TwoGyroLattice(LatticeConfig(n_sites=48, frames=80), mode="stable").run(80)
        chaotic = TwoGyroLattice(LatticeConfig(n_sites=48, frames=80, gauge_strength=0.08), mode="chaotic").run(80)

        fig, axes = plt.subplots(2, 2, figsize=(9.5, 6.2), sharex="col")
        t = np.arange(len(stable.pointer_history))
        axes[0, 0].plot(t, stable.pointer_history, color="#3182ce")
        axes[0, 0].set_title("Gauge pointer — stable")
        axes[0, 1].plot(t, chaotic.pointer_history, color="#e53e3e")
        axes[0, 1].set_title("Gauge pointer — chaotic")
        axes[1, 0].plot(t, stable.mean_twist_history, color="#2b6cb0", label="mean twist")
        axes[1, 0].plot(t, stable.identity_preservation, color="#d69e2e", label="identity")
        axes[1, 0].legend(fontsize=8)
        axes[1, 0].set_title("Twist & identity — stable")
        axes[1, 1].plot(t, chaotic.mean_twist_history, color="#2b6cb0")
        axes[1, 1].plot(t, chaotic.identity_preservation, color="#d69e2e")
        axes[1, 1].set_title("Twist & identity — chaotic")
        for ax in axes.ravel():
            ax.grid(True, alpha=0.3)
        fig.suptitle(
            "Auxiliary Figure A3.1 — Lattice Simulator still\n"
            f"(TwoGyroLattice: stable bursts={stable.total_bursts}, "
            f"chaotic bursts={chaotic.total_bursts})",
            fontsize=12,
            fontweight="bold",
        )
        fig.tight_layout()
        fig.savefig(FIG_DIR / "aux3_1_lattice_simulator_still.png", dpi=160, bbox_inches="tight", facecolor="white")
        plt.close()
        return
    except Exception as e:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis("off")
        ax.text(
            0.5,
            0.5,
            f"Lattice Simulator still unavailable\n({e})\n"
            "Install/import kingdom.simulations.lattice to regenerate.",
            ha="center",
            va="center",
            fontsize=11,
        )
        fig.savefig(FIG_DIR / "aux3_1_lattice_simulator_still.png", dpi=140, bbox_inches="tight", facecolor="white")
        plt.close()


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_3_1()
    fig_3_2()
    fig_3_3()
    fig_3_4()
    fig_3_5()
    aux_3_1()
    print(f"Wrote Chapter 3 figures to {FIG_DIR}")
    for name in sorted(FIG_DIR.glob("fig3_*")) + sorted(FIG_DIR.glob("aux3_*")):
        print(f"  {name.name}: {name.stat().st_size} bytes")


if __name__ == "__main__":
    main()
