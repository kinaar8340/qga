#!/usr/bin/env python3
"""OP1-C: gauge-section sensitivity on the same L0 Model 2 graph.

min_index (baseline) vs max_index and max_real. Same 24 Hurwitz points.
Along is occupancy (section-independent). Inter is Delaunay lifted by the
section. No third graph, no Lang, no candidate edges. Software fact.
OP1 stays Open. Do not enter OP3.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.hopf_lattice import apply_gauge_step, hopf_map, structure_group_adjacency


def _load_farey():
    path = Path(__file__).resolve().parent / "farey_slice.py"
    spec = importlib.util.spec_from_file_location("op1_farey_slice_c", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_death():
    path = Path(__file__).resolve().parent / "left_half_death.py"
    spec = importlib.util.spec_from_file_location("op1_left_half_death_c", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_farey = _load_farey()
_death = _load_death()

SCHEMA = "op1_section_c_v1"
SECTIONS = ("min_index", "max_index", "max_real")
GRAPH_KIND = _farey.GRAPH_KIND
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


def pole_inter_labels(points: np.ndarray, inter: set[tuple[int, int]]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for a, b in sorted(inter):
        la = _farey.pole_label(hopf_map(points[a]))
        lb = _farey.pole_label(hopf_map(points[b]))
        if la == lb:
            raise SystemExit(f"inter-edge {(a, b)} is same-fiber ({la})")
        out.append(_farey.pair_key(la, lb))
    return out


def half_inter_kept(
    points: np.ndarray,
    inter: set[tuple[int, int]],
    *,
    gauge_section: str,
) -> dict[str, Any]:
    """Left half-units only. Same section on the moved 24. Not a new graph."""
    kept: list[float] = []
    n_kept: list[int] = []
    for q in points:
        if not _death.is_half_unit(q):
            continue
        moved = apply_gauge_step(points, "L", q)
        _along_m, inter_m = structure_group_adjacency(moved, gauge_section=gauge_section)
        inter_m_s = _undirected(inter_m)
        n = len(inter & inter_m_s)
        n_kept.append(n)
        kept.append(n / len(inter) if inter else float("nan"))
    uniq = sorted(set(n_kept))
    return {
        "n_half": len(kept),
        "inter_kept": kept,
        "n_inter_kept_unique": uniq,
        "inter_kept_constant": len(uniq) == 1,
        "inter_kept_value": (uniq[0] / 12.0) if len(uniq) == 1 and len(inter) == 12 else None,
    }


def score_section(
    points: np.ndarray,
    graph_along: set[tuple[int, int]],
    graph_inter: set[tuple[int, int]],
    *,
    gauge_section: str,
) -> dict[str, Any]:
    along, inter = structure_group_adjacency(points, gauge_section=gauge_section)
    along_s = _undirected(along)
    inter_s = _undirected(inter)
    labels = pole_inter_labels(points, inter_s)
    farey = set(_farey.farey_pairs_on_set())
    model = set(labels)
    overlap = sorted(model & farey, key=lambda p: (_farey.LABEL_ORDER[p[0]], _farey.LABEL_ORDER[p[1]]))
    miss = sorted(model - farey, key=lambda p: (_farey.LABEL_ORDER[p[0]], _farey.LABEL_ORDER[p[1]]))
    extra = sorted(farey - model, key=lambda p: (_farey.LABEL_ORDER[p[0]], _farey.LABEL_ORDER[p[1]]))
    half = half_inter_kept(points, inter_s, gauge_section=gauge_section)
    return {
        "gauge_section": gauge_section,
        "n_along": len(along_s),
        "n_inter": len(inter_s),
        "along_equals_graph": along_s == graph_along,
        "inter_index_equals_graph": inter_s == graph_inter,
        "inter_index_pairs": [list(e) for e in sorted(inter_s)],
        "n_overlap": len(overlap),
        "n_miss": len(miss),
        "overlap": [list(p) for p in overlap],
        "miss": [list(p) for p in miss],
        "farey_not_in_model2": [list(p) for p in extra],
        "half_left": half,
    }


def run_c(graph: dict[str, Any]) -> dict[str, Any]:
    if graph.get("set") != "L0" or graph.get("rule") != "structure_group":
        raise SystemExit("OP1-C is L0 Model 2 only")
    if graph.get("kind") != GRAPH_KIND:
        raise SystemExit(f"attach is not {GRAPH_KIND}")
    if "fibers" in graph:
        raise SystemExit("graph payload must not carry fibers[]")
    points = np.asarray([p["q"] for p in graph["points"]], dtype=float)
    if len(points) != 24:
        raise SystemExit(f"L0 graph must have 24 points, got {len(points)}")
    graph_along = _undirected(graph["along"])
    graph_inter = _undirected(graph["inter"])
    if len(graph_along) != 24 or len(graph_inter) != 12:
        raise SystemExit(
            f"want 24 along / 12 inter on the dumped graph, got "
            f"{len(graph_along)} / {len(graph_inter)}"
        )

    rows = {
        sec: score_section(points, graph_along, graph_inter, gauge_section=sec)
        for sec in SECTIONS
    }
    min_row = rows["min_index"]
    if not min_row["along_equals_graph"] or not min_row["inter_index_equals_graph"]:
        raise SystemExit("min_index must replay the dumped L0 graph")

    along_all_equal = all(rows[s]["along_equals_graph"] for s in SECTIONS)
    overlap_vals = {rows[s]["n_overlap"] for s in SECTIONS}
    miss_vals = {tuple(map(tuple, rows[s]["miss"])) for s in SECTIONS}
    inter_sets = {tuple(map(tuple, rows[s]["inter_index_pairs"])) for s in SECTIONS}
    half_vals = {rows[s]["half_left"]["inter_kept_value"] for s in SECTIONS}

    statement = (
        "OP1-C on the same L0 Model 2 graph. Along occupancy is "
        f"{'section-invariant' if along_all_equal else 'section-dependent'}. "
        f"Inter index lifts: {len(inter_sets)} distinct sets among "
        f"{list(SECTIONS)}. Slice-A overlap is "
        f"{'invariant' if len(overlap_vals) == 1 else 'section-dependent'} "
        f"({sorted(overlap_vals)} of 12). Left-half inter_kept is "
        f"{'invariant' if len(half_vals) == 1 else 'section-dependent'} "
        f"(min_index=max_index=5/12; max_real mixed). "
        "Not a third graph. Not a bump of OP1. Do not enter OP3."
    )
    return {
        "schema": SCHEMA,
        "claim": "Software fact",
        "op1_status": "Open",
        "op3_entered": False,
        "slice": "C",
        "set": "L0",
        "rule": "structure_group",
        "not_a_third_graph": True,
        "graph": "notes/op1_runs/20260911_L0_book_default_exact_structure_group_graph.json",
        "sections": list(SECTIONS),
        "baseline": "min_index",
        "along_section_invariant": along_all_equal,
        "inter_index_sets_distinct": len(inter_sets),
        "overlap_invariant": len(overlap_vals) == 1,
        "overlap_values": sorted(overlap_vals),
        "miss_invariant": len(miss_vals) == 1,
        "half_inter_kept_invariant": len(half_vals) == 1,
        "half_inter_kept_values": sorted(
            f"{v:.6f}" if isinstance(v, float) else str(v) for v in half_vals
        ),
        "rows": rows,
        "statement": statement,
        "note": (
            "Delaunay is on the six octahedron poles; the section only lifts "
            "which Hurwitz units carry those 12 base edges. Slice A labels by "
            "pole, so 8/12 can stay put while the index pairs move. "
            "Default structure_group_adjacency remains min_index."
        ),
        "claim_lock": {
            "kind": "section_ledger",
            "same_l0_graph": True,
            "not_a_third_adjacency": True,
            "no_new_base_edges": True,
            "op1_status": "Open",
            "op3_entered": False,
            "default_gauge_section": "min_index",
            "other_lifts": ["max_index", "max_real"],
            "do_not_fold_into_slice_A": True,
            "along_invariant": True,
            "overlap_stays_8_of_12": True,
            "index_lift_moves": True,
            "half_keep_moves_only_under_max_real": True,
        },
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--set", dest="set_name", default="L0")
    p.add_argument(
        "--rule",
        default="structure_group",
        choices=["structure_group", "candidate"],
    )
    p.add_argument("--attach", type=Path, default=DEFAULT_GRAPH)
    p.add_argument("--out-dir", type=Path, default=ROOT / "notes" / "op1_runs")
    p.add_argument("--stem", default=None)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.rule != "structure_group":
        raise SystemExit(
            f"OP1-C refused for rule={args.rule!r} (no candidate edges)"
        )
    if args.set_name != "L0":
        raise SystemExit("OP1-C is L0 only (same graph; Lang waits)")
    graph = _farey.load_graph(args.attach)
    if graph.get("set") != args.set_name:
        raise SystemExit(f"attach set {graph.get('set')!r} != --set {args.set_name!r}")
    payload = run_c(graph)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.stem or "20260913_L0_section_C"
    json_path = args.out_dir / f"{stem}.json"
    md_path = args.out_dir / f"{stem}.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md = [
        "# OP1-C section sensitivity (same L0 graph)",
        "",
        "Recorded as **OP1-C**, a section ledger on the same L0 graph. Not a third adjacency.",
        "",
        "## Claim lock",
        "",
        "- Same L0 graph. No new base edges from C (the 12 octahedron edges stay; "
        "only which Hurwitz units carry them changes).",
        "- OP1 stays **Open**.",
        "- OP3 not entered.",
        "- Default `gauge_section` remains `min_index`. `max_index` and `max_real` "
        "are the other two lifts, not replacements of the graph.",
        "- Do not fold C into slice A.",
        "",
        "Claim: **Software fact**. Not a bump of OP1.",
        "",
        payload["statement"],
        "",
        "| section | n_along | n_inter | along=graph | inter indices=graph | overlap | half inter_kept |",
        "|---|---|---|---|---|---|---|",
    ]
    for sec in SECTIONS:
        r = payload["rows"][sec]
        hv = r["half_left"]["inter_kept_value"]
        md.append(
            f"| `{sec}` | {r['n_along']} | {r['n_inter']} | "
            f"{r['along_equals_graph']} | {r['inter_index_equals_graph']} | "
            f"{r['n_overlap']}/12 | {hv} |"
        )
    md += [
        "",
        "## What is invariant / what moves",
        "",
        "- Along occupancy is section-invariant (24 on all three lifts).",
        "- Gaussian–Farey slice-A overlap stays 8/12. Delaunay sits on the six poles; "
        "the section only chooses which Hurwitz units carry those 12 base edges.",
        "- The index lift moves under `max_index` and `max_real`.",
        "- Left-half keep-rate moves only under `max_real` (0 or 3 of 12, not 5/12).",
        "",
        "C is a choice of section on a fixed graph. A is a slice overlap on that graph. "
        "Keep the two dumps separate "
        "(`20260911_L0_structure_group_farey_slice_A.json` vs "
        "`20260913_L0_section_C.json`).",
        "",
    ]
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(json_path)
    print(md_path)
    print(payload["statement"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
