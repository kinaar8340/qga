#!/usr/bin/env python3
"""Generate Chapter 2 Hopf fibration figures for Kingdom Come / QGA book."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "book" / "figures"


def _try_import_hopf():
    """Import fiber sampling from flux_hopf_lib or kingdom."""
    candidates = [
        Path.home() / "Projects" / "flux_hopf_lib" / "src",
        Path.home() / "Projects" / "kingdom" / "src",
    ]
    for p in candidates:
        if p.is_dir() and str(p) not in sys.path:
            sys.path.insert(0, str(p))
    try:
        from flux_hopf_lib.hopf import sample_fiber, sample_fiber_family  # type: ignore

        return sample_fiber, sample_fiber_family
    except Exception:
        try:
            from kingdom.core.hopf import sample_fiber, sample_fiber_family  # type: ignore

            return sample_fiber, sample_fiber_family
        except Exception as e:
            raise ImportError(
                "Need flux_hopf_lib or kingdom on PYTHONPATH to sample real fibers"
            ) from e


def fig_2_1() -> None:
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    # Total space S3
    ax.add_patch(
        FancyBboxPatch(
            (0.4, 1.2),
            2.8,
            2.6,
            boxstyle="round,pad=0.08,rounding_size=0.2",
            facecolor="#bee3f8",
            edgecolor="#2c5282",
            lw=2,
        )
    )
    ax.text(1.8, 3.3, r"Total space $S^3$", ha="center", fontsize=12, fontweight="bold")
    ax.text(1.8, 2.6, r"unit quaternions", ha="center", fontsize=10)
    ax.text(1.8, 2.1, r"$(z_1,z_2)$ or $(x_1..x_4)$", ha="center", fontsize=9, color="#2d3748")
    ax.text(1.8, 1.55, r"$|z_1|^2+|z_2|^2=1$", ha="center", fontsize=9, color="#4a5568")

    # Arrow
    ax.annotate(
        "",
        xy=(5.0, 2.5),
        xytext=(3.5, 2.5),
        arrowprops=dict(arrowstyle="-|>", color="#c05621", lw=2.5, mutation_scale=16),
    )
    ax.text(4.25, 3.05, r"Hopf map $h$", ha="center", fontsize=11, color="#c05621", fontweight="bold")
    ax.text(4.25, 1.85, r"fiber $=S^1$", ha="center", fontsize=9, color="#4a5568")

    # Base S2
    ax.add_patch(
        FancyBboxPatch(
            (5.3, 1.2),
            2.8,
            2.6,
            boxstyle="round,pad=0.08,rounding_size=0.2",
            facecolor="#c6f6d5",
            edgecolor="#276749",
            lw=2,
        )
    )
    ax.text(6.7, 3.3, r"Base $S^2$", ha="center", fontsize=12, fontweight="bold")
    ax.text(6.7, 2.55, r"$h(z_1,z_2)$ or", ha="center", fontsize=10)
    ax.text(6.7, 2.1, r"$(y_1,y_2,y_3)$", ha="center", fontsize=10)
    ax.text(6.7, 1.55, r"$\mathbb{CP}^1\cong S^2$", ha="center", fontsize=9, color="#4a5568")

    # Formula strip
    ax.add_patch(
        FancyBboxPatch(
            (0.4, 0.25),
            9.0,
            0.75,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            facecolor="#f7fafc",
            edgecolor="#a0aec0",
            lw=1,
        )
    )
    ax.text(
        4.9,
        0.62,
        r"KC real form:  $y_1=x_1^2-x_2^2,\; y_2=2x_1x_2,\; y_3=2(x_3x_4+x_1x_2)$  (then normalize)",
        ha="center",
        fontsize=9,
    )

    ax.set_title(
        "Figure 2.1 — Hopf map: total space $S^3$ to base $S^2$",
        fontsize=12,
        fontweight="bold",
        pad=8,
    )
    fig.savefig(FIG_DIR / "fig2_1_hopf_definition.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_2_2(sample_fiber_family) -> None:
    fibers = sample_fiber_family(n_fibers=8, n_points=180, scale=2.0)
    fig = plt.figure(figsize=(7.5, 6.2))
    ax = fig.add_subplot(111, projection="3d")
    cmap = plt.cm.turbo
    for i, f in enumerate(fibers):
        color = cmap(i / max(len(fibers) - 1, 1))
        ax.plot(f["px"], f["py"], f["pz"], color=color, lw=1.8, alpha=0.9)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(
        "Figure 2.2 — Linked Hopf fibers (stereographic $\\mathbb{R}^3$)\n"
        "rebuild of Fig. 0.1 from sample_fiber_family",
        fontsize=11,
        fontweight="bold",
    )
    # equal-ish aspect
    pts = np.concatenate(
        [np.stack([f["px"], f["py"], f["pz"]], axis=1) for f in fibers], axis=0
    )
    c = pts.mean(axis=0)
    r = np.percentile(np.linalg.norm(pts - c, axis=1), 95)
    ax.set_xlim(c[0] - r, c[0] + r)
    ax.set_ylim(c[1] - r, c[1] + r)
    ax.set_zlim(c[2] - r, c[2] + r)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.02)
    fig.savefig(FIG_DIR / "fig2_2_linked_fibers.png", dpi=160, facecolor="white")
    plt.close()


def fig_2_3(sample_fiber, sample_fiber_family) -> None:
    """Multi-panel stereographic preview (rebuild of Fig. 0.2 spirit)."""
    fibers = sample_fiber_family(n_fibers=10, n_points=160, scale=2.0)
    highlight = sample_fiber(eta=0.55, xi1=0.4, n_points=200, scale=2.0)

    fig = plt.figure(figsize=(10, 8))
    # 3D composed view
    ax3 = fig.add_subplot(2, 2, 1, projection="3d")
    for f in fibers:
        ax3.plot(f["px"], f["py"], f["pz"], color="#63b3ed", lw=1.0, alpha=0.55)
    ax3.plot(highlight["px"], highlight["py"], highlight["pz"], color="#c05621", lw=2.5)
    ax3.set_title("Stereographic fibers (highlight one)")
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_zticks([])

    # xy projection
    ax = fig.add_subplot(2, 2, 2)
    for f in fibers:
        ax.plot(f["px"], f["py"], color="#90cdf4", lw=0.9, alpha=0.7)
    ax.plot(highlight["px"], highlight["py"], color="#c05621", lw=2)
    ax.set_aspect("equal")
    ax.set_title("xy projection")
    ax.grid(True, alpha=0.25)

    # xz projection
    ax = fig.add_subplot(2, 2, 3)
    for f in fibers:
        ax.plot(f["px"], f["pz"], color="#9ae6b4", lw=0.9, alpha=0.7)
    ax.plot(highlight["px"], highlight["pz"], color="#c05621", lw=2)
    ax.set_aspect("equal")
    ax.set_title("xz projection")
    ax.grid(True, alpha=0.25)

    # base S2 markers
    ax = fig.add_subplot(2, 2, 4, projection="3d")
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(xs, ys, zs, alpha=0.12, color="#2b6cb0", edgecolor="none")
    by1 = np.array([f["base_y1"] for f in fibers])
    by2 = np.array([f["base_y2"] for f in fibers])
    by3 = np.array([f["base_y3"] for f in fibers])
    ax.scatter(by1, by2, by3, c=np.linspace(0, 1, len(fibers)), cmap="turbo", s=35)
    ax.scatter(
        [highlight["base_y1"]],
        [highlight["base_y2"]],
        [highlight["base_y3"]],
        color="#c05621",
        s=80,
        depthshade=False,
    )
    ax.set_title(r"Base points on $S^2$")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    fig.suptitle(
        "Figure 2.3 — Stereographic preview of the fibration (rebuild of Fig. 0.2)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig2_3_stereographic_preview.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_2_4() -> None:
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Base circle (S2 schematic as disk)
    base = Circle((5, 1.6), 1.35, facecolor="#c6f6d5", edgecolor="#276749", lw=2)
    ax.add_patch(base)
    ax.text(5, 1.6, r"$S^2$\nbase", ha="center", va="center", fontsize=11, fontweight="bold")

    # Fibers as vertical-ish loops above base points
    fiber_xs = [3.2, 5.0, 6.8]
    colors = ["#2b6cb0", "#c05621", "#2f855a"]
    for x, col in zip(fiber_xs, colors):
        t = np.linspace(0, 2 * np.pi, 120)
        # ellipse representing circle fiber
        fx = x + 0.45 * np.cos(t)
        fy = 3.9 + 0.55 * np.sin(t)
        ax.plot(fx, fy, color=col, lw=2.5)
        ax.plot([x, x], [1.6 + 1.2, 3.9 - 0.55], color=col, lw=1.2, ls="--", alpha=0.7)
        ax.plot(x, 1.6 + np.sqrt(max(1.35**2 - (x - 5) ** 2, 0)) * 0.15 + 0.9, "o", color=col, ms=6)

    ax.text(5, 5.4, r"Total space $S^3$ (fibers $S^1$ over each base point)", ha="center", fontsize=12, fontweight="bold")
    ax.text(
        5,
        0.35,
        r"$S^1 \hookrightarrow S^3 \twoheadrightarrow S^2$  — nontrivial principal $U(1)$-bundle",
        ha="center",
        fontsize=11,
    )
    ax.annotate(
        "",
        xy=(5, 2.95),
        xytext=(5, 3.25),
        arrowprops=dict(arrowstyle="-|>", color="#4a5568", lw=1.5),
    )
    ax.text(5.35, 3.05, r"$h$", fontsize=11, color="#4a5568")

    ax.set_title(
        "Figure 2.4 — Bundle structure (rebuild of Fig. 0.3)",
        fontsize=12,
        fontweight="bold",
        pad=6,
    )
    fig.savefig(FIG_DIR / "fig2_4_bundle_structure.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def aux_2_1(sample_fiber) -> None:
    f = sample_fiber(eta=0.6, xi1=0.5, n_points=200, scale=2.0)
    fig = plt.figure(figsize=(10, 4.2))

    ax = fig.add_subplot(1, 2, 1, projection="3d")
    # color by phase
    c = f["xi2"] / (2 * np.pi)
    for i in range(len(f["px"]) - 1):
        ax.plot(
            f["px"][i : i + 2],
            f["py"][i : i + 2],
            f["pz"][i : i + 2],
            color=plt.cm.hsv(c[i]),
            lw=2.5,
        )
    ax.set_title(r"Single fiber colored by phase $\xi_2$")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax2 = fig.add_subplot(1, 2, 2)
    # phase vs arc index
    ax2.scatter(f["xi2"], np.arange(len(f["xi2"])), c=c, cmap="hsv", s=18)
    ax2.set_xlabel(r"fiber phase $\xi_2$")
    ax2.set_ylabel("sample index")
    ax2.set_title(r"Phase sweep $\xi_2 \in [0, 2\pi)$ (closed circle)")
    ax2.grid(True, alpha=0.3)

    fig.suptitle(
        "Auxiliary Figure A2.1 — Single fiber phase sweep",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "aux2_1_fiber_phase_sweep.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def aux_2_2() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.3))
    for ax, title, pole in zip(
        axes,
        [r"Chart $U_N$: stereographic from north", r"Chart $U_S$: stereographic from south"],
        ["N", "S"],
    ):
        ax.set_aspect("equal")
        th = np.linspace(0, 2 * np.pi, 200)
        ax.fill(np.cos(th), np.sin(th), color="#ebf8ff", edgecolor="#2b6cb0", lw=2)
        # grid meridians/parallels projected schematically
        for r in (0.25, 0.5, 0.75):
            ax.plot(r * np.cos(th), r * np.sin(th), color="#90cdf4", lw=1, alpha=0.8)
        for ang in np.linspace(0, np.pi, 6, endpoint=False):
            ax.plot([0, np.cos(ang)], [0, np.sin(ang)], color="#a0aec0", lw=0.8)
            ax.plot([0, np.cos(ang + np.pi)], [0, np.sin(ang + np.pi)], color="#a0aec0", lw=0.8)
        ax.set_xlim(-1.25, 1.25)
        ax.set_ylim(-1.25, 1.25)
        ax.set_title(title, fontsize=10)
        ax.text(0, 0, r"$\mathbb{R}^2$", ha="center", va="center", fontsize=11, color="#2c5282")
        ax.text(0, -1.12, rf"trivialization $h^{{-1}}(U_{pole})\cong U_{pole}\times S^1$", ha="center", fontsize=8, color="#4a5568")
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle(
        r"Auxiliary Figure A2.2 — Local charts on base $S^2$ (phase unwrapping / gauge fixing)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "aux2_2_hopf_charts.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    sample_fiber, sample_fiber_family = _try_import_hopf()

    fig_2_1()
    fig_2_2(sample_fiber_family)
    fig_2_3(sample_fiber, sample_fiber_family)
    fig_2_4()
    aux_2_1(sample_fiber)
    aux_2_2()
    print(f"Wrote Chapter 2 figures to {FIG_DIR}")
    for name in [
        "fig2_1_hopf_definition.png",
        "fig2_2_linked_fibers.png",
        "fig2_3_stereographic_preview.png",
        "fig2_4_bundle_structure.png",
        "aux2_1_fiber_phase_sweep.png",
        "aux2_2_hopf_charts.png",
    ]:
        p = FIG_DIR / name
        print(f"  {name}: {p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
