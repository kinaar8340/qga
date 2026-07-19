#!/usr/bin/env python3
"""Generate Chapter 8 figures: composition and class-group analogues."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "book" / "figures"
sys.path.insert(0, str(ROOT))

from lib.composition import (  # noqa: E402
    class_group_analogue,
    compose_flywheels,
    composition_table,
    reduce_composition,
)
from lib.flux_topograph import (  # noqa: E402
    build_flux_topograph,
    class_number_analogue,
)
from lib.hopf_lattice import candidate_adjacency, sample_angle_lattice, stereographic  # noqa: E402


def _two_topos():
    pts = sample_angle_lattice(n_eta=2, n_xi1=6, n_xi2=6)
    along, inter = candidate_adjacency(pts, base_angle_thresh=0.55, fiber_phase_bins=6)
    edges = along + inter
    t1 = build_flux_topograph(pts, edges=edges, functional="hopf_height")
    t2 = build_flux_topograph(pts, edges=edges, functional="hopf_y1")
    return t1, t2


def fig_8_1() -> None:
    """Classical Gauss composition schematic."""
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    for x, label, fc in [
        (0.5, r"$f_1$" "\n" r"(a₁,b₁,c₁)", "#bee3f8"),
        (3.5, r"$f_2$" "\n" r"(a₂,b₂,c₂)", "#c6f6d5"),
        (7.5, r"$f_1 * f_2$" "\n" r"same $\Delta$", "#feebc8"),
        (10.2, "class\ngroup", "#e9d8fd"),
    ]:
        ax.add_patch(
            FancyBboxPatch(
                (x, 1.2), 2.0, 1.6, boxstyle="round,pad=0.05",
                facecolor=fc, edgecolor="#2d3748", lw=1.5,
            )
        )
        ax.text(x + 1.0, 2.0, label, ha="center", va="center", fontsize=10)
    ax.annotate("", xy=(3.5, 2.0), xytext=(2.5, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#4a5568", lw=2))
    ax.annotate("", xy=(7.5, 2.0), xytext=(5.5, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#4a5568", lw=2))
    ax.annotate("", xy=(10.2, 2.0), xytext=(9.5, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#4a5568", lw=2))
    ax.text(6.0, 0.6, r"Gauss composition $\rightarrow$ finite abelian class group (classical Theorem)",
            ha="center", fontsize=10, color="#4a5568")
    ax.set_title("Figure 8.1 — Classical Gauss composition (Hatcher Ch. 7 reminder)",
                 fontsize=12, fontweight="bold")
    fig.savefig(FIG_DIR / "fig8_1_gauss_composition.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_8_2() -> None:
    t1, t2 = _two_topos()
    comp = compose_flywheels(t1, t2, method="value_sum")
    red = reduce_composition(comp)["topograph"]

    fig = plt.figure(figsize=(11, 3.8))
    for idx, (topo, title) in enumerate(
        [(t1, r"$\Phi_1$"), (t2, r"$\Phi_2$"), (red, r"reduce$(\Phi_1 * \Phi_2)$")],
        start=1,
    ):
        ax = fig.add_subplot(1, 3, idx, projection="3d")
        st = np.stack([stereographic(q) for q in topo.points], axis=0)
        ax.scatter(st[:, 0], st[:, 1], st[:, 2], c=topo.values, cmap="coolwarm", s=18)
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
    fig.suptitle(
        "Figure 8.2 — Composition of two flux topographs / flywheels (Model)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig8_2_flywheel_composition.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_8_3() -> None:
    t1, _ = _two_topos()
    cg = class_group_analogue(t1, dedup_tol=0.08, samples=8)
    order = cg["order"]
    table = cg["table"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    ax = axes[0]
    # class nodes in a circle
    th = np.linspace(0, 2 * np.pi, max(order, 1), endpoint=False)
    xs, ys = np.cos(th), np.sin(th)
    ax.set_aspect("equal")
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.axis("off")
    for i, (x, y) in enumerate(zip(xs, ys)):
        ax.add_patch(Circle((x, y), 0.18, facecolor="#bee3f8", edgecolor="#2c5282", lw=1.5))
        ax.text(x, y, f"[{i}]", ha="center", va="center", fontsize=9, fontweight="bold")
    # a few composition arrows from table
    if table is not None and order >= 2:
        for i in range(min(order, 4)):
            j = (i + 1) % order
            k = int(table[i, j]) if table[i, j] >= 0 else (i + j) % order
            ax.annotate(
                "",
                xy=(xs[k] * 0.75, ys[k] * 0.75),
                xytext=(xs[i] * 0.75, ys[i] * 0.75),
                arrowprops=dict(arrowstyle="-|>", color="#c05621", lw=1.2, alpha=0.7),
            )
    ax.set_title(f"classes (order={order})\n{cg['structure']}")

    ax = axes[1]
    if table is not None and order > 0:
        im = ax.imshow(table, cmap="viridis", vmin=-1, vmax=max(order - 1, 0))
        ax.set_xlabel("class j")
        ax.set_ylabel("class i")
        ax.set_title("composition table [i]*[j]")
        fig.colorbar(im, ax=ax, fraction=0.046)
    else:
        ax.text(0.5, 0.5, "empty", ha="center")
        ax.axis("off")

    fig.suptitle(
        "Figure 8.3 — Class-group analogue on the gauged Hopf lattice (Model)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig8_3_class_group_analogue.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_8_4() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.4, 0.6), 9.0, 4.8, boxstyle="round,pad=0.05",
                                facecolor="#ebf8ff", edgecolor="#90cdf4"))
    # class group bar
    ax.add_patch(FancyBboxPatch((1.0, 4.0), 8.0, 0.9, boxstyle="round,pad=0.04",
                                facecolor="#e9d8fd", edgecolor="#6b46c1", lw=1.5))
    ax.text(5.0, 4.45, "class-group analogue  [0] * [1] * …", ha="center", fontsize=11, fontweight="bold")
    # island
    ax.add_patch(Circle((5.0, 2.2), 1.3, facecolor="#fefcbf", edgecolor="#d69e2e", lw=2.5))
    ax.text(5.0, 2.2, "Magic\nIsland", ha="center", va="center", fontsize=12, fontweight="bold", color="#744210")
    ax.annotate("", xy=(5.0, 3.45), xytext=(5.0, 3.95),
                arrowprops=dict(arrowstyle="-|>", color="#4a5568", lw=2))
    ax.text(5.0, 0.9, "distinguished / high-stability classes ↔ island location (Model)",
            ha="center", fontsize=9, color="#4a5568")
    ax.set_title(
        "Figure 8.4 — Magic Island from class-group structure (schematic Model)",
        fontsize=12,
        fontweight="bold",
    )
    fig.savefig(FIG_DIR / "fig8_4_island_from_class.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def aux_8_1() -> None:
    t1, t2 = _two_topos()
    cn = class_number_analogue(t1, dedup_tol=0.1)
    reps = [r["topograph"] for r in cn["reduced"][:4]]
    if len(reps) < 2:
        reps = [t1, t2]
    # ensure at least 2
    while len(reps) < 2:
        reps.append(t2)
    table = composition_table(reps[:3], method="value_sum", dedup_tol=0.1)

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    mat = table["table"]
    im = ax.imshow(mat, cmap="coolwarm", vmin=-1, vmax=max(len(reps) - 1, 1))
    n = mat.shape[0]
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xlabel("j")
    ax.set_ylabel("i")
    for i in range(n):
        for j in range(n):
            ax.text(j, i, str(int(mat[i, j])), ha="center", va="center", color="white", fontweight="bold")
    ax.set_title(
        f"Aux A8.1 — Composition table (n={n}, closure={table['closure_fraction']:.2f})",
        fontsize=11,
        fontweight="bold",
    )
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "aux8_1_composition_table.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_8_1()
    fig_8_2()
    fig_8_3()
    fig_8_4()
    aux_8_1()
    print(f"Wrote Chapter 8 figures to {FIG_DIR}")
    for p in sorted(FIG_DIR.glob("fig8_*")) + sorted(FIG_DIR.glob("aux8_*")):
        print(f"  {p.name}: {p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
