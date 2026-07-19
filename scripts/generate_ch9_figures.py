#!/usr/bin/env python3
"""Generate Chapter 9 figures: quaternion algebras and ideal theory."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "book" / "figures"
sys.path.insert(0, str(ROOT))

from lib.hopf_lattice import HURWITZ_UNITS, stereographic  # noqa: E402
from lib.quaternion_algebra import HurwitzOrder, QuaternionAlgebra  # noqa: E402


def fig_9_1() -> None:
    A = QuaternionAlgebra(-1, -1)
    ram = A.ramified_places(prime_bound=30)
    fig, ax = plt.subplots(figsize=(9.5, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")

    ax.add_patch(FancyBboxPatch((0.4, 1.3), 3.2, 1.8, boxstyle="round,pad=0.06",
                                facecolor="#bee3f8", edgecolor="#2c5282", lw=1.5))
    ax.text(2.0, 2.5, r"Quaternion algebra" "\n" r"$(a,b/\mathbb{Q})$",
            ha="center", va="center", fontsize=11, fontweight="bold")

    ax.annotate("", xy=(5.0, 2.2), xytext=(3.7, 2.2),
                arrowprops=dict(arrowstyle="-|>", color="#4a5568", lw=2))

    ax.add_patch(FancyBboxPatch((5.2, 0.6), 3.0, 1.4, boxstyle="round,pad=0.05",
                                facecolor="#fed7d7", edgecolor="#c53030", lw=1.5))
    ax.text(6.7, 1.3, "ramified places\n" + ", ".join(str(p) for p in ram[:6]),
            ha="center", va="center", fontsize=9)

    ax.add_patch(FancyBboxPatch((5.2, 2.4), 3.0, 1.4, boxstyle="round,pad=0.05",
                                facecolor="#c6f6d5", edgecolor="#276749", lw=1.5))
    ax.text(6.7, 3.1, "split places\n(matrix algebra)",
            ha="center", va="center", fontsize=9)

    ax.add_patch(FancyBboxPatch((8.8, 1.3), 2.8, 1.8, boxstyle="round,pad=0.06",
                                facecolor="#feebc8", edgecolor="#c05621", lw=1.5))
    defn = "definite" if A.is_definite() else "indefinite"
    ax.text(10.2, 2.2, f"type:\n{defn}\nover R", ha="center", va="center", fontsize=10)

    ax.set_title(
        r"Figure 9.1 — Ramification of a quaternion algebra (example $(-1,-1/\mathbb{Q})$)",
        fontsize=12,
        fontweight="bold",
    )
    fig.savefig(FIG_DIR / "fig9_1_quaternion_algebra.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_9_2() -> None:
    O = HurwitzOrder()
    pts = O.units
    st = np.stack([stereographic(q) for q in pts], axis=0)
    fig = plt.figure(figsize=(9.5, 4.5))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    colors = []
    for q in pts:
        if np.allclose(np.abs(q), [1, 0, 0, 0]) or np.allclose(sorted(np.abs(q)), [0, 0, 0, 1]):
            colors.append("#2b6cb0")
        else:
            colors.append("#c05621")
    ax.scatter(st[:, 0], st[:, 1], st[:, 2], c=colors, s=55)
    ax.set_title("24 Hurwitz units (stereo $S^3$)")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax = fig.add_subplot(1, 2, 2)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    rows = [
        ("Lipschitz", "Z[i,j,k]", "8 units", "not Euclidean"),
        ("Hurwitz", "all int or all half-int", "24 units", "Euclidean / maximal"),
    ]
    ax.text(5, 9.2, "Orders in Hamilton quaternions", ha="center", fontsize=12, fontweight="bold")
    for i, (name, defn, units, prop) in enumerate(rows):
        y = 7.2 - i * 3.0
        ax.add_patch(FancyBboxPatch((1, y - 1.2), 8, 2.4, boxstyle="round,pad=0.08",
                                    facecolor="#edf2f7", edgecolor="#4a5568", lw=1.5))
        ax.text(5, y + 0.6, name, ha="center", fontsize=12, fontweight="bold", color="#2c5282")
        ax.text(5, y, defn, ha="center", fontsize=10)
        ax.text(5, y - 0.6, f"{units} · {prop}", ha="center", fontsize=10, color="#4a5568")
    ax.set_title("Figure 9.2 — Hurwitz order lattice / units", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig9_2_hurwitz_order.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_9_3() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    # three ideal classes (for general illustration; Hurwitz has only one)
    centers = [(2.5, 3.2), (5.0, 3.2), (7.5, 3.2)]
    labels = ["[I]", "[J]", "[K]"]
    for (x, y), lab in zip(centers, labels):
        ax.add_patch(Circle((x, y), 0.7, facecolor="#bee3f8", edgecolor="#2b6cb0", lw=2))
        ax.text(x, y, lab, ha="center", va="center", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(4.2, 3.2), xytext=(3.3, 3.2),
                arrowprops=dict(arrowstyle="-|>", color="#c05621", lw=2))
    ax.annotate("", xy=(6.7, 3.2), xytext=(5.8, 3.2),
                arrowprops=dict(arrowstyle="-|>", color="#c05621", lw=2))
    ax.annotate("", xy=(2.9, 2.6), xytext=(7.1, 2.6),
                arrowprops=dict(arrowstyle="-|>", color="#2f855a", lw=1.5,
                                connectionstyle="arc3,rad=-0.35"))
    ax.text(5, 5.2, "Ideal multiplication on classes", ha="center", fontsize=12, fontweight="bold")
    ax.text(5, 1.0, "Hurwitz (Hamilton): class number 1  ·  general orders: finite when definite",
            ha="center", fontsize=9, color="#4a5568")
    ax.set_title("Figure 9.3 — Ideal class group schematic", fontsize=12, fontweight="bold")
    fig.savefig(FIG_DIR / "fig9_3_ideal_class_group.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_9_4() -> None:
    fig, ax = plt.subplots(figsize=(9.5, 3.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    boxes = [
        (0.4, 1.2, 2.4, 1.6, "ideal class\n[I]", "#bee3f8"),
        (3.5, 1.2, 2.6, 1.6, "Model\ndictionary", "#e9d8fd"),
        (6.8, 1.2, 2.4, 1.6, "flux topograph\n/ flywheel", "#feebc8"),
        (9.6, 1.2, 2.0, 1.6, "Magic\nIsland", "#fefcbf"),
    ]
    for x, y, w, h, text, fc in boxes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                    facecolor=fc, edgecolor="#2d3748", lw=1.5))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10)
    for x0, x1 in [(2.8, 3.5), (6.1, 6.8), (9.2, 9.6)]:
        ax.annotate("", xy=(x1, 2.0), xytext=(x0, 2.0),
                    arrowprops=dict(arrowstyle="-|>", color="#4a5568", lw=2))
    ax.text(5.5, 0.5, "Model bridge — not a proved functor (OP6)", ha="center",
            fontsize=9, color="#c53030")
    ax.set_title(
        "Figure 9.4 — From ideal class to flux flywheel (Model bridge)",
        fontsize=12,
        fontweight="bold",
    )
    fig.savefig(FIG_DIR / "fig9_4_ideal_to_flywheel.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def aux_9_1() -> None:
    algebras = [
        QuaternionAlgebra(-1, -1),
        QuaternionAlgebra(2, 3),
        QuaternionAlgebra(-1, 3),
        QuaternionAlgebra(5, 13),
    ]
    # collect primes of interest
    primes = [2, 3, 5, 7, 11, 13, "∞"]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.axis("off")
    # table header
    col_w = 1.1
    row_h = 0.55
    x0, y0 = 0.5, 3.2
    ax.text(x0 + 1.5, y0 + 0.7, "Aux A9.1 — Hilbert symbols (a,b)_p  (−1 = ramified)",
            fontsize=12, fontweight="bold")
    # header row
    ax.text(x0, y0, "(a,b)", fontweight="bold", fontsize=9)
    for j, p in enumerate(primes):
        ax.text(x0 + 2.0 + j * col_w, y0, str(p), fontweight="bold", fontsize=9, ha="center")
    for i, A in enumerate(algebras):
        y = y0 - (i + 1) * row_h
        ax.text(x0, y, f"({A.a},{A.b})", fontsize=9)
        for j, p in enumerate(primes):
            s = A.hilbert_at(p)
            color = "#c53030" if s == -1 else "#276749"
            ax.text(x0 + 2.0 + j * col_w, y, str(s), fontsize=9, ha="center", color=color, fontweight="bold")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.2)
    fig.savefig(FIG_DIR / "aux9_1_ramification_table.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_9_1()
    fig_9_2()
    fig_9_3()
    fig_9_4()
    aux_9_1()
    print(f"Wrote Chapter 9 figures to {FIG_DIR}")
    for p in sorted(FIG_DIR.glob("fig9_*")) + sorted(FIG_DIR.glob("aux9_*")):
        print(f"  {p.name}: {p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
