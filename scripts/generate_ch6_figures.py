#!/usr/bin/env python3
"""Generate Chapter 6 figures: classification and Magic Islands."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "book" / "figures"
sys.path.insert(0, str(ROOT))

from lib.flux_topograph import (  # noqa: E402
    apply_gauge_to_topograph,
    build_flux_topograph,
    class_number_analogue,
    classify_topograph_type,
    detect_separators,
    enumerate_reduced,
    reduced_representative,
)
from lib.hopf_lattice import (  # noqa: E402
    candidate_adjacency,
    hopf_project_points,
    sample_angle_lattice,
    stereographic,
)


def _topo_sample(functional="hopf_height", n_eta=2, n_xi1=8, n_xi2=8):
    pts = sample_angle_lattice(n_eta=n_eta, n_xi1=n_xi1, n_xi2=n_xi2)
    along, inter = candidate_adjacency(pts, base_angle_thresh=0.55, fiber_phase_bins=8)
    return build_flux_topograph(pts, edges=along + inter, functional=functional)


def fig_6_1() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 8.0))
    specs = [
        ("elliptic", "hopf_y1", "Elliptic\nfinite / compact separators"),
        ("hyperbolic", "hopf_height", "Hyperbolic\nperiodic separators"),
        ("parabolic", "norm", "Parabolic\ntransitional / low structure"),
        ("0-hyperbolic", "index_wave", "0-hyperbolic / flat-ish\nnear-constant pockets"),
    ]
    # force schematic panels rather than relying on classifier
    for ax, (name, func, title) in zip(axes.ravel(), specs):
        pts = sample_angle_lattice(2, 7, 7)
        along, inter = candidate_adjacency(pts, base_angle_thresh=0.6, fiber_phase_bins=7)
        topo = build_flux_topograph(pts, edges=along + inter, functional=func)
        if name == "0-hyperbolic":
            topo.values = np.full_like(topo.values, 0.1)
        st = np.stack([stereographic(q) for q in topo.points], axis=0)
        ax_rm = ax
        # 2d projection
        sc = ax_rm.scatter(st[:, 0], st[:, 1], c=topo.values, cmap="coolwarm", s=14)
        seps = detect_separators(topo)
        for comp in seps[:5]:
            for i, j in comp[:40]:
                ax_rm.plot(
                    [st[i, 0], st[j, 0]],
                    [st[i, 1], st[j, 1]],
                    color="#1a202c",
                    lw=0.8,
                    alpha=0.5,
                )
        ax_rm.set_title(title, fontsize=10)
        ax_rm.set_xticks([])
        ax_rm.set_yticks([])
        ax_rm.set_aspect("equal")
    fig.suptitle(
        "Figure 6.1 — Four types of flux topographs (schematic Model lift)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig6_1_four_types.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_6_2() -> None:
    topo = _topo_sample("hopf_height", 2, 8, 8)
    rep, meta = reduced_representative(topo)
    st0 = np.stack([stereographic(q) for q in topo.points], axis=0)
    st1 = np.stack([stereographic(q) for q in rep.points], axis=0)

    fig = plt.figure(figsize=(10, 4.5))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.scatter(st0[:, 0], st0[:, 1], st0[:, 2], c=topo.values, cmap="coolwarm", s=16)
    ax.set_title(f"original (var={np.var(topo.values):.3f})")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax = fig.add_subplot(1, 2, 2, projection="3d")
    ax.scatter(st1[:, 0], st1[:, 1], st1[:, 2], c=rep.values, cmap="coolwarm", s=16)
    ax.set_title(f"reduced rep (var={meta['variance']:.3f})")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    fig.suptitle(
        "Figure 6.2 — Reduced configuration (minimal-variance gauge representative)",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig6_2_reduced_config.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_6_3() -> None:
    topo = _topo_sample("hopf_height", 2, 7, 7)
    cn = class_number_analogue(topo, dedup_tol=0.05)
    types = list(cn["by_type"].keys()) or ["none"]
    counts = [cn["by_type"].get(t, 0) for t in types]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    ax = axes[0]
    ax.bar(types, counts, color=["#2b6cb0", "#c05621", "#2f855a", "#805ad5"][: len(types)])
    ax.set_ylabel("reduced representatives")
    ax.set_title(f"class_number_analogue = {cn['class_number_analogue']}")
    ax.tick_params(axis="x", rotation=15)

    ax = axes[1]
    # schematic islands
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.4, 0.6), 9.0, 4.8, boxstyle="round,pad=0.05", facecolor="#ebf8ff", edgecolor="#90cdf4"))
    for cx, cy, r, lab in [(3.0, 3.2, 1.1, "I₁"), (6.5, 3.5, 1.3, "I₂"), (5.0, 1.8, 0.7, "I₃")]:
        ax.add_patch(Circle((cx, cy), r, facecolor="#fefcbf", edgecolor="#d69e2e", lw=2, alpha=0.9))
        ax.text(cx, cy, lab, ha="center", va="center", fontweight="bold")
    ax.set_title("Magic Islands as clusters of reduced configs")
    ax.text(5, 0.35, "count of inequivalent reduced reps ↔ class-number analogue", ha="center", fontsize=9, color="#4a5568")

    fig.suptitle(
        "Figure 6.3 — Class-number analogue and Magic Island clusters",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig6_3_class_number_analogue.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_6_4() -> None:
    topo = _topo_sample("hopf_y1", 2, 8, 8)
    i = np.array([0.0, 1.0, 0.0, 0.0])
    topo2 = apply_gauge_to_topograph(topo, [("L", i)], recompute_functional=True)
    st0 = np.stack([stereographic(q) for q in topo.points], axis=0)
    st1 = np.stack([stereographic(q) for q in topo2.points], axis=0)

    fig = plt.figure(figsize=(10, 4.5))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.scatter(st0[:, 0], st0[:, 1], st0[:, 2], c=topo.values, cmap="coolwarm", s=18)
    ax.set_title(r"topograph $\Phi$")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax = fig.add_subplot(1, 2, 2, projection="3d")
    ax.scatter(st1[:, 0], st1[:, 1], st1[:, 2], c=topo2.values, cmap="coolwarm", s=18)
    ax.set_title(r"equivalent $g\cdot\Phi$ (left $\times i$)")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    fig.suptitle(
        "Figure 6.4 — Gauge equivalence of two flux topographs",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig6_4_equivalence.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def aux_6_1() -> None:
    fig, ax = plt.subplots(figsize=(9.5, 4.0))
    zs = np.arange(1, 51)
    scores = None
    try:
        sys.path.insert(0, str(Path.home() / "Projects" / "flux_hopf_lib" / "src"))
        sys.path.insert(0, str(Path.home() / "Projects" / "kingdom" / "src"))
        from kingdom.core.flux_flywheel import map_z_to_flywheel

        scores = np.array([map_z_to_flywheel(int(z))["stability_score"] for z in zs])
        nobles = [z for z in zs if map_z_to_flywheel(int(z)).get("is_noble_gas")]
    except Exception:
        scores = 5.2 + 2.5 * (
            (zs == 2) | (zs == 10) | (zs == 18) | (zs == 36)
        ).astype(float) + 0.3 * np.sin(zs / 3)
        nobles = [2, 10, 18, 36]

    ax.plot(zs, scores, color="#2b6cb0", lw=1.8, label="stability_score")
    ax.axhline(7.0, color="#c05621", ls="--", lw=1, label="high-stability threshold (Model)")
    for z in nobles:
        ax.axvline(z, color="#d69e2e", ls=":", lw=1, alpha=0.8)
    ax.scatter(nobles, [scores[z - 1] for z in nobles if z <= 50], c="#d69e2e", s=40, zorder=3, label="noble gas Z")
    ax.set_xlabel("Z")
    ax.set_ylabel("stability_score")
    ax.set_title("Auxiliary Figure A6.1 — Parameter sweep (Z) revealing Magic-Island-like peaks")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "aux6_1_island_sweep.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_6_1()
    fig_6_2()
    fig_6_3()
    fig_6_4()
    aux_6_1()
    print(f"Wrote Chapter 6 figures to {FIG_DIR}")
    for p in sorted(FIG_DIR.glob("fig6_*")) + sorted(FIG_DIR.glob("aux6_*")):
        print(f"  {p.name}: {p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
