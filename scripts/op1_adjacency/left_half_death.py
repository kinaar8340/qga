#!/usr/bin/env python3
"""Classify the L0 left-half death (Model 2, resnap=exact).

Lipschitz 8 keeps occupancy 4-cycles. Left half-units of 2T permute Λ0
but send each Hopf 4-cycle to two antipodal poles (2+2). along_kept=0
is therefore occupancy failing left-invariance on a 2T-set, not only
min_index section sensitivity.

Uses the dumped L0 graph + the same Model 2 rule on the moved 24.
No third adjacency, no Lang, no second Delaunay. Software fact. OP1 Open.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.hopf_lattice import (  # noqa: E402
    apply_gauge_step,
    hopf_map,
    structure_group_adjacency,
)


def _load_farey():
    path = Path(__file__).resolve().parent / "farey_slice.py"
    spec = importlib.util.spec_from_file_location("op1_farey_slice", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_farey = _load_farey()
GRAPH_KIND = _farey.GRAPH_KIND
LABEL_ORDER = _farey.LABEL_ORDER
load_graph = _farey.load_graph
pair_key = _farey.pair_key
pole_label = _farey.pole_label


def unit_name(u: np.ndarray) -> str:
    u = np.asarray(u, dtype=float).reshape(4)
    axes = {
        (1.0, 0.0, 0.0, 0.0): "1",
        (-1.0, 0.0, 0.0, 0.0): "-1",
        (0.0, 1.0, 0.0, 0.0): "i",
        (0.0, -1.0, 0.0, 0.0): "-i",
        (0.0, 0.0, 1.0, 0.0): "j",
        (0.0, 0.0, -1.0, 0.0): "-j",
        (0.0, 0.0, 0.0, 1.0): "k",
        (0.0, 0.0, 0.0, -1.0): "-k",
    }
    key = tuple(round(float(c), 6) for c in u)
    if key in axes:
        return axes[key]
    if np.allclose(np.abs(u), 0.5, atol=1e-8):
        signs = "".join("+" if c > 0 else "-" for c in u)
        return f"half_{signs}"
    return "u(" + ",".join(f"{c:.3f}" for c in u) + ")"

SCHEMA = "op1_left_half_death_v1"
DEFAULT_GRAPH = (
    ROOT
    / "notes"
    / "op1_runs"
    / "20260911_L0_book_default_exact_structure_group_graph.json"
)


def _undirected(edges: list) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for e in edges:
        a, b = int(e[0]), int(e[1])
        out.add((a, b) if a < b else (b, a))
    return out


def occupancy_cycles(n: int, along: set[tuple[int, int]]) -> list[list[int]]:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for a, b in along:
        adj[a].append(b)
        adj[b].append(a)
    seen: set[int] = set()
    cycles: list[list[int]] = []
    for start in range(n):
        if start in seen or not adj[start]:
            continue
        cur, prev, seq = start, None, []
        while cur not in seen:
            seen.add(cur)
            seq.append(cur)
            nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
            prev, cur = cur, nxt
        cycles.append(seq)
    return cycles


def is_half_unit(q: np.ndarray) -> bool:
    return bool(np.allclose(np.abs(q), 0.5, atol=1e-8))


def is_lipschitz(q: np.ndarray) -> bool:
    a = np.abs(np.asarray(q, dtype=float).reshape(4))
    return bool(np.count_nonzero(a > 0.5) == 1 and abs(float(a.max()) - 1.0) < 1e-8)


def classify_unit(
    points: np.ndarray,
    along: set[tuple[int, int]],
    inter: set[tuple[int, int]],
    cycles: list[list[int]],
    unit: np.ndarray,
    *,
    side: str = "L",
) -> dict[str, Any]:
    moved = apply_gauge_step(points, side, unit)
    along_m, inter_m = structure_group_adjacency(moved)
    along_m_s = _undirected(along_m)
    inter_m_s = _undirected(inter_m)
    cycle_rows = []
    all_single = True
    all_split = True
    for seq in cycles:
        src = pole_label(hopf_map(points[seq[0]]))
        labs = [pole_label(hopf_map(moved[i])) for i in seq]
        counts = {k: int(v) for k, v in Counter(labs).items()}
        uniq = sorted(counts, key=lambda x: LABEL_ORDER[x])
        cyc_edges = set()
        for a, b in zip(seq, seq[1:] + seq[:1]):
            cyc_edges.add((a, b) if a < b else (b, a))
        rec = len(cyc_edges & along_m_s)
        if len(uniq) != 1:
            all_single = False
        if not (len(uniq) == 2 and all(counts[k] == 2 for k in uniq)):
            all_split = False
        cycle_rows.append(
            {
                "src_fiber": src,
                "indices": seq,
                "image_fibers": uniq,
                "image_counts": counts,
                "along_recovered": rec,
                "n_along": 4,
            }
        )
    surv = []
    for a, b in sorted(inter):
        if (a, b) not in inter_m_s:
            continue
        la = pole_label(hopf_map(points[a]))
        lb = pole_label(hopf_map(points[b]))
        surv.append(list(pair_key(la, lb)))
    n_along = len(along)
    n_inter = len(inter)
    return {
        "unit": [float(c) for c in np.asarray(unit, dtype=float).reshape(4)],
        "unit_name": unit_name(unit),
        "side": side,
        "along_kept": len(along & along_m_s) / n_along,
        "inter_kept": len(inter & inter_m_s) / n_inter,
        "n_along_kept": len(along & along_m_s),
        "n_inter_kept": len(inter & inter_m_s),
        "cycles_map_to_single_fiber": all_single,
        "cycles_split_2_plus_2_antipodes": all_split,
        "cycles": cycle_rows,
        "surviving_octahedron_edges": surv,
    }


def run_table(graph: dict[str, Any]) -> dict[str, Any]:
    if graph.get("set") != "L0" or graph.get("rule") != "structure_group":
        raise SystemExit("left-half death table is L0 Model 2 only")
    points = np.asarray([p["q"] for p in graph["points"]], dtype=float)
    if len(points) != 24:
        raise SystemExit(f"L0 graph must have 24 points, got {len(points)}")
    along = _undirected(graph["along"])
    inter = _undirected(graph["inter"])
    if len(along) != 24 or len(inter) != 12:
        raise SystemExit(f"want 24 along / 12 inter, got {len(along)} / {len(inter)}")
    cycles = occupancy_cycles(24, along)
    if len(cycles) != 6 or any(len(c) != 4 for c in cycles):
        raise SystemExit(f"want six 4-cycles, got {[len(c) for c in cycles]}")

    lipschitz = []
    half = []
    for q in points:
        if is_lipschitz(q):
            lipschitz.append(classify_unit(points, along, inter, cycles, q))
        elif is_half_unit(q):
            half.append(classify_unit(points, along, inter, cycles, q))
    if len(lipschitz) != 8 or len(half) != 16:
        raise SystemExit(f"want 8 Lipschitz + 16 half, got {len(lipschitz)}+{len(half)}")

    verdict = (
        "Left half-units do not map occupancy 4-cycles to 4-cycles: each "
        "cycle splits 2+2 onto an antipodal pair of poles. along_kept=0 is "
        "occupancy failing left-invariance on a 2T-set, not only min_index "
        "section sensitivity. Lipschitz 8 maps each 4-cycle to one fiber "
        "and keeps all 24 along-edges. Software fact. OP1 stays Open."
    )
    return {
        "schema": SCHEMA,
        "claim": "Software fact",
        "op1_status": "Open",
        "slice_status": (
            "C-miniature: occupancy not left-invariant on 2T. "
            "Full C (other sections) still parked."
        ),
        "set": "L0",
        "rule": "structure_group",
        "resnap": "exact",
        "side": "L",
        "verdict": verdict,
        "n_lipschitz": 8,
        "n_half": 16,
        "lipschitz_all_cycles_single_fiber": all(
            r["cycles_map_to_single_fiber"] for r in lipschitz
        ),
        "lipschitz_along_kept": [r["along_kept"] for r in lipschitz],
        "half_all_cycles_split_2_plus_2": all(
            r["cycles_split_2_plus_2_antipodes"] for r in half
        ),
        "half_along_kept": [r["along_kept"] for r in half],
        "half_inter_kept": [r["inter_kept"] for r in half],
        "lipschitz": lipschitz,
        "half": half,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--set", dest="set_name", default="L0")
    p.add_argument("--rule", default="structure_group", choices=["structure_group", "candidate"])
    p.add_argument("--attach", type=Path, default=DEFAULT_GRAPH)
    p.add_argument("--out-dir", type=Path, default=ROOT / "notes" / "op1_runs")
    p.add_argument("--stem", default=None)
    return p.parse_args(argv)


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# L0 left-half death (Model 2, resnap=exact)",
        "",
        f"Claim: **{payload['claim']}**. `slice_status`: **{payload['slice_status']}**. "
        "OP1 stays **Open**.",
        "",
        payload["verdict"],
        "",
        "## Lipschitz 8 (contrast)",
        "",
        "| unit | along_kept | inter_kept | each 4-cycle lands on |",
        "|---|---|---|---|",
    ]
    for r in payload["lipschitz"]:
        lands = ", ".join(
            f"{c['src_fiber']}→{c['image_fibers'][0]}" for c in r["cycles"]
        )
        lines.append(
            f"| {r['unit_name']} | {r['along_kept']:.0f} | {r['inter_kept']:.0f} | {lands} |"
        )
    lines += [
        "",
        "## Left half-units (16)",
        "",
        "| left half-unit | image of each 4-cycle | along recovered | 5 surviving octahedron edges |",
        "|---|---|---|---|",
    ]
    for r in payload["half"]:
        imgs = "; ".join(
            f"{c['src_fiber']}→{{{', '.join(c['image_fibers'])}}} 2+2"
            for c in r["cycles"]
        )
        surv = ", ".join(f"{a}–{b}" for a, b in r["surviving_octahedron_edges"])
        lines.append(
            f"| {r['unit_name']} | {imgs} | {r['n_along_kept']}/24 | {surv} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.rule != "structure_group":
        raise SystemExit("refused: candidate is not the analysis channel")
    if args.set_name != "L0":
        raise SystemExit("left-half death table is L0 only")
    graph = load_graph(args.attach)
    if graph.get("kind") != GRAPH_KIND:
        raise SystemExit("attach must be qga_adjacency_graph_v1")
    payload = run_table(graph)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.stem or (
        f"{date.today().strftime('%Y%m%d')}_L0_left_half_death"
    )
    json_path = args.out_dir / f"{stem}.json"
    md_path = args.out_dir / f"{stem}.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(json_path)
    print(md_path)
    print(payload["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
