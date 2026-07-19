#!/usr/bin/env python3
"""Generate Chapter 1 figures for Kingdom Come / QGA book."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "book" / "figures"


def fig_1_1() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    ax = axes[0]
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(r"Positive cycle: $ij=k$, $jk=i$, $ki=j$", fontsize=11)
    pts = {
        "i": np.array([0.0, 1.0]),
        "j": np.array([-0.866, -0.5]),
        "k": np.array([0.866, -0.5]),
    }
    for name, p in pts.items():
        ax.add_patch(
            Circle(p, 0.28, facecolor="#1a365d", edgecolor="white", lw=2, zorder=3)
        )
        ax.text(
            p[0],
            p[1],
            name,
            color="white",
            ha="center",
            va="center",
            fontsize=16,
            fontweight="bold",
            zorder=4,
        )

    def arrow(a, b, color="#c05621"):
        ax.annotate(
            "",
            xy=b * 0.62,
            xytext=a * 0.62,
            arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2, mutation_scale=14),
        )

    arrow(pts["i"], pts["j"])
    arrow(pts["j"], pts["k"])
    arrow(pts["k"], pts["i"])
    ax.text(0, -1.25, r"$i^2=j^2=k^2=ijk=-1$", ha="center", fontsize=11)

    ax = axes[1]
    ax.axis("off")
    ax.set_title("Multiplication table (row x column)", fontsize=11)
    labels = ["1", "i", "j", "k"]
    table = [
        ["1", "i", "j", "k"],
        ["i", "-1", "k", "-j"],
        ["j", "-k", "-1", "i"],
        ["k", "j", "-i", "-1"],
    ]
    colors = []
    for r in range(4):
        rowc = []
        for c in range(4):
            val = table[r][c]
            if r == 0:
                rowc.append("#e2e8f0")
            elif val.startswith("-"):
                rowc.append("#fed7d7")
            elif val in ("i", "j", "k"):
                rowc.append("#c6f6d5")
            else:
                rowc.append("#bee3f8")
        colors.append(rowc)

    the_table = ax.table(
        cellText=table,
        rowLabels=labels,
        colLabels=labels,
        cellColours=colors,
        loc="center",
        cellLoc="center",
    )
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(12)
    the_table.scale(1.2, 1.8)
    for (r, c), cell in the_table.get_celld().items():
        cell.set_edgecolor("#4a5568")
        if r == 0 or c == -1:
            cell.set_text_props(fontweight="bold")

    fig.suptitle(
        "Figure 1.1 — Quaternion imaginary units and multiplication",
        fontsize=12,
        fontweight="bold",
        y=1.02,
    )
    fig.savefig(FIG_DIR / "fig1_1_ijk_multiplication.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_1_2() -> None:
    fig = plt.figure(figsize=(10, 4.5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_aspect("equal")
    theta = np.linspace(0, 2 * np.pi, 200)
    for r, alpha in [(1.0, 0.15), (0.75, 0.25), (0.5, 0.35), (0.25, 0.5)]:
        ax1.fill(
            r * np.cos(theta),
            r * np.sin(theta),
            alpha=alpha,
            color="#2b6cb0",
            edgecolor="#2c5282",
            lw=1,
        )
    ax1.plot(np.cos(theta), np.sin(theta), color="#1a365d", lw=2)
    ax1.set_xlim(-1.3, 1.3)
    ax1.set_ylim(-1.3, 1.3)
    ax1.set_title(r"Complex view: $(z_1,z_2)\in\mathbb{C}^2$, $|z_1|^2+|z_2|^2=1$")
    ax1.text(0, 0, r"$S^3$", ha="center", va="center", fontsize=14, fontweight="bold", color="#1a365d")
    ax1.text(
        0,
        -1.15,
        r"nested level sets of $|z_1|$ (fiber radii later)",
        ha="center",
        fontsize=8,
        color="#4a5568",
    )
    ax1.set_xlabel(r"Re $z_1$ (schematic)")
    ax1.set_ylabel(r"Im $z_1$ (schematic)")
    ax1.grid(True, alpha=0.25)

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 25)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax2.plot_surface(xs, ys, zs, alpha=0.15, color="#2b6cb0", edgecolor="none")
    t = np.linspace(0, 2 * np.pi, 200)
    R = 1.0
    ax2.plot(R * np.cos(t), R * np.sin(t), np.zeros_like(t), color="#c05621", lw=2.5)
    ax2.plot(R * np.cos(t), 0.15 * np.sin(t), R * np.sin(t), color="#2f855a", lw=2.5)
    ax2.set_title(r"Stereographic idea: fibers in $\mathbb{R}^3$")
    ax2.set_xlim(-1.4, 1.4)
    ax2.set_ylim(-1.4, 1.4)
    ax2.set_zlim(-1.4, 1.4)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_zticks([])
    ax2.text2D(
        0.05,
        0.02,
        "linked circles preview Hopf fibers (Ch. 2)",
        transform=ax2.transAxes,
        fontsize=8,
        color="#4a5568",
    )
    fig.suptitle(r"Figure 1.2 — Unit quaternions as $S^3 \subset \mathbb{R}^4$", fontsize=12, fontweight="bold")
    fig.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.08, wspace=0.25)
    fig.savefig(FIG_DIR / "fig1_2_s3_unit_quaternions.png", dpi=160, facecolor="white")
    plt.close()


def fig_1_3() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    ax = axes[0]
    ax.set_aspect("equal")
    xs = np.arange(-3, 4)
    ys = np.arange(-3, 4)
    for x in xs:
        for y in ys:
            ax.plot(x, y, "o", color="#2b6cb0", ms=8)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_title("Lipschitz order Z[i,j,k]\n(integer coords a,b,c,d)")
    ax.set_xlabel("schematic plane (a,b) slice")
    ax.set_ylabel("(c,d) analogous")
    ax.grid(True, alpha=0.3)
    ax.text(0, -3.2, "lattice spacing 1", ha="center", fontsize=9, color="#4a5568")

    ax = axes[1]
    ax.set_aspect("equal")
    for x in xs:
        for y in ys:
            ax.plot(x, y, "o", color="#2b6cb0", ms=7, zorder=2)
    for x in np.arange(-2.5, 3.0, 1.0):
        for y in np.arange(-2.5, 3.0, 1.0):
            ax.plot(x, y, "s", color="#c05621", ms=6, zorder=2)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_title("Hurwitz order H\nall integer or all half-integer coords")
    ax.set_xlabel("blue = integer; orange = half-integer")
    ax.grid(True, alpha=0.3)
    ax.text(0, -3.2, "extra points enable Euclidean algorithm", ha="center", fontsize=9, color="#4a5568")
    ax.plot([], [], "o", color="#2b6cb0", label="integer coords")
    ax.plot([], [], "s", color="#c05621", label="half-integer coords")
    ax.legend(loc="upper right", fontsize=8)

    fig.suptitle(
        "Figure 1.3 — Lipschitz vs Hurwitz integer quaternions (schematic slices)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig1_3_lipschitz_hurwitz.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_1_4() -> None:
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    def box(x, y, w, h, text, fc):
        p = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.05,rounding_size=0.15",
            facecolor=fc,
            edgecolor="#2d3748",
            lw=1.5,
        )
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10)

    box(0.3, 1.5, 2.2, 1.4, "$q_1$\n$N(q_1)=n_1$", "#bee3f8")
    box(3.0, 1.5, 2.2, 1.4, "$q_2$\n$N(q_2)=n_2$", "#c6f6d5")
    box(6.5, 1.5, 2.8, 1.4, "$q_1 q_2$\n$N=n_1 n_2$", "#feebc8")
    ax.annotate(
        "",
        xy=(3.0, 2.2),
        xytext=(2.5, 2.2),
        arrowprops=dict(arrowstyle="-|>", color="#2d3748", lw=2),
    )
    ax.annotate(
        "",
        xy=(6.5, 2.2),
        xytext=(5.2, 2.2),
        arrowprops=dict(arrowstyle="-|>", color="#2d3748", lw=2),
    )
    ax.text(5.85, 2.55, r"$\times$", fontsize=16, ha="center")
    ax.text(
        5.0,
        0.7,
        r"Theorem: $N(q_1 q_2)=N(q_1)\,N(q_2)$  $\Rightarrow$  products of sums of four squares",
        ha="center",
        fontsize=11,
    )
    ax.text(
        5.0,
        0.25,
        r"Example: $(1^2+1^2+1^2+1^2)(1^2+0+0+0)=4\cdot 1=4$",
        ha="center",
        fontsize=9,
        color="#4a5568",
    )
    ax.set_title(
        "Figure 1.4 — Multiplicativity of the quaternion norm",
        fontsize=12,
        fontweight="bold",
        pad=12,
    )
    fig.savefig(FIG_DIR / "fig1_4_norm_multiplicativity.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def aux_1_1() -> None:
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot([0, 0], [0, 0], [0, 1.3], color="#c05621", lw=3, label="axis u")
    ax.scatter([0], [0], [1.3], color="#c05621", s=40)
    t = np.linspace(0, 2 * np.pi, 120)
    r = 0.9
    v0 = np.array([r, 0, 0.2])
    ax.plot(
        r * np.cos(t),
        r * np.sin(t),
        np.full_like(t, 0.2),
        color="#2b6cb0",
        lw=2,
        label=r"orbit of $v$ under $q v q^{-1}$",
    )
    ax.quiver(0, 0, 0, v0[0], v0[1], v0[2], color="#2f855a", lw=2, arrow_length_ratio=0.12)
    arc_t = np.linspace(0, np.pi / 2, 40)
    ax.plot(0.35 * np.cos(arc_t), 0.35 * np.sin(arc_t), 0.2 * np.ones_like(arc_t), color="#718096", lw=1.5)
    ax.text(0.45, 0.35, 0.25, r"$\theta$", fontsize=12)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-0.2, 1.4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_title(
        "Aux A1.1 — Unit quaternion rotation\n(double cover: q and -q same rotation)",
        fontsize=11,
    )
    fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    fig.savefig(FIG_DIR / "aux1_1_quaternion_rotation.png", dpi=160, facecolor="white")
    plt.close()


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_1_1()
    fig_1_2()
    fig_1_3()
    fig_1_4()
    aux_1_1()
    print(f"Wrote Chapter 1 figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
