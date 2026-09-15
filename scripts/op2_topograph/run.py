#!/usr/bin/env python3
"""OP2 flux-topograph harness on Model 2 only.

Software facts. OP2 stays Open. Does not close OP1. Does not use
candidate_adjacency as the analysis skeleton. --matrix assembles the
equivariance ledger from scored JSON; it is not a new graph and not OP3.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.flux_topograph import (
    build_flux_topograph,
    detect_separators,
    fiber_cycle_flux,
    kirchhoff_report,
    periodicity_score,
    pole_level_sets,
    separator_equivariance_score,
)

I_UNIT = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
J_UNIT = np.array([0.0, 0.0, 1.0, 0.0], dtype=float)
SCHEMA = "op2_topograph_v1"
DEFAULT_FUNCTIONALS = ("hopf_height", "hopf_y1")

OP1_DEFAULTS = {
    "Lsg": ROOT / "notes" / "op1_runs" / "20260911_Lsg_book_default_none_structure_group.json",
    "L0": ROOT / "notes" / "op1_runs" / "20260911_L0_book_default_exact_structure_group.json",
    "Lang": ROOT / "notes" / "op1_runs" / "20260911_Lang_book_default_none_structure_group.json",
}

# Objects already scored. The equivariance matrix reads these; it is not a new graph.
OP2_SCORED = {
    "Lsg": ROOT / "notes" / "op2_runs" / "20260911_Lsg_structure_group.json",
    "L0": ROOT / "notes" / "op2_runs" / "20260911_L0_structure_group.json",
    "Lang": ROOT / "notes" / "op2_runs" / "20260911_Lang_structure_group.json",
}
MATRIX_SCHEMA = "op2_equivariance_matrix_v1"
SETS = ("Lsg", "L0", "Lang")
SIDES = ("left_i", "left_j")
RIGHT_SIDES = ("right_i", "right_j")
SIDE_UNIT = {"left_i": "i", "left_j": "j", "right_i": "i", "right_j": "j"}
UNIT_VEC = {"i": I_UNIT, "j": J_UNIT}
COL_LABEL = {
    "left_i": "left-i",
    "left_j": "left-j",
    "right_i": "right-i",
    "right_j": "right-j",
}
LEFT_LEDGER = "notes/op2_runs/20260913_equivariance_matrix.json"
RIGHT_LEDGER = "notes/op2_runs/20260913_equivariance_matrix_right.json"


def _load_op1_run():
    path = ROOT / "scripts" / "op1_adjacency" / "run.py"
    spec = importlib.util.spec_from_file_location("op1_adjacency_run", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_op1_row(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "op1_adjacency_v1":
        raise SystemExit(f"attach is not op1_adjacency_v1: {path}")
    if data.get("rule") != "structure_group":
        raise SystemExit(
            f"OP2 requires Model 2 attach (rule=structure_group), got {data.get('rule')!r}"
        )
    if data.get("op1_status") != "Open":
        # still allow, but refuse a silent candidate graph
        pass
    return data


def _op1_keep(row: dict[str, Any], unit_name: str, side: str) -> dict[str, Any]:
    for r in row.get("experiment2") or []:
        if r.get("unit_name") == unit_name and r.get("side") == side:
            return {
                "along_kept": r.get("along_kept"),
                "inter_kept": r.get("inter_kept"),
                "n_along": r.get("n_along"),
                "n_inter": r.get("n_inter"),
            }
    return {}


def _delta(before: Any, after: Any) -> int | None:
    if before is None or after is None:
        return None
    return int(after) - int(before)


def _ledger_tag(per: dict[str, Any], eq: dict[str, Any]) -> str:
    """Ledger label for one (set, side, functional). Not an axiom."""
    n0 = per.get("n_components_before")
    if per.get("status") == "undefined_or_vacuous" or n0 == 0:
        return "undefined_or_vacuous"
    if per.get("changed"):
        return "changed"
    if eq.get("n_components_before") != eq.get("n_components_after"):
        return "changed"
    if eq.get("n_sep_edges_before") != eq.get("n_sep_edges_after"):
        return "changed"
    return "unchanged"


def _functional_cell(block: dict[str, Any], side: str) -> dict[str, Any]:
    eq = block["equivariance"][side]
    per = block["periodicity"][side]
    tag = _ledger_tag(per, eq)
    n0 = per.get("n_components_before")
    n1 = per.get("n_components_after")
    e0 = per.get("n_separator_edges_before")
    e1 = per.get("n_separator_edges_after")
    return {
        "ledger": tag,
        "periodicity_status": per.get("status"),
        "kind": per.get("kind"),
        "n_components_before": n0,
        "n_components_after": n1,
        "delta_n_components": _delta(n0, n1),
        "n_separator_edges_before": e0,
        "n_separator_edges_after": e1,
        "delta_n_separator_edges": _delta(e0, e1),
        "changed": bool(per.get("changed")),
        "not_farey_period": True,
        "separator_equivariance": {
            "n_sep_edges_before": eq.get("n_sep_edges_before"),
            "n_sep_edges_after": eq.get("n_sep_edges_after"),
            "n_components_before": eq.get("n_components_before"),
            "n_components_after": eq.get("n_components_after"),
            "edge_count_ratio": eq.get("edge_count_ratio"),
        },
        "empty_cut_not_keep_rate_1": tag == "undefined_or_vacuous",
    }


def assemble_equivariance_matrix(*, root: Path = ROOT) -> dict[str, Any]:
    """3×2 ledger from scored OP2 JSON. Not a new graph. Not OP3. Not an axiom."""
    cells: dict[str, Any] = {}
    sources: dict[str, Any] = {}
    for set_name in SETS:
        path = root / "notes" / "op2_runs" / OP2_SCORED[set_name].name
        if not path.is_file():
            raise SystemExit(f"missing scored OP2 row {path}")
        op2 = json.loads(path.read_text(encoding="utf-8"))
        if op2.get("schema") != SCHEMA:
            raise SystemExit(f"not {SCHEMA}: {path}")
        if op2.get("rule") != "structure_group" or op2.get("adjacency") != "structure_group":
            raise SystemExit(f"OP2 matrix refuses non-structure_group row: {path}")
        if op2.get("set") != set_name:
            raise SystemExit(f"OP2 row set {op2.get('set')!r} != {set_name}")
        attach_rel = op2["attached_op1"]
        attach = root / attach_rel
        op1 = load_op1_row(attach)
        if op1.get("set") != set_name:
            raise SystemExit(f"attach set {op1.get('set')!r} != {set_name}")
        sources[set_name] = {
            "op2": str(path.resolve().relative_to(root.resolve())),
            "op1": attach_rel,
        }
        row: dict[str, Any] = {}
        for side in SIDES:
            keep = _op1_keep(op1, SIDE_UNIT[side], "L")
            cell: dict[str, Any] = {
                "op1": {
                    "unit_name": SIDE_UNIT[side],
                    "side": "L",
                    "along_kept": keep.get("along_kept"),
                    "inter_kept": keep.get("inter_kept"),
                    "n_along": keep.get("n_along"),
                    "n_inter": keep.get("n_inter"),
                    "note": (
                        "OP1 Experiment 2 on this attach, left side only. "
                        "Not averaged. Right is a sibling ledger. "
                        "Empty OP2 cut is not keep-rate 1.0."
                    ),
                }
            }
            for fname, block in op2["functionals"].items():
                cell[fname] = _functional_cell(block, side)
            row[side] = cell
        cells[set_name] = row
    return {
        "schema": MATRIX_SCHEMA,
        "claim": "Software fact",
        "op1_status": "Open",
        "op2_status": "Open",
        "op3_status": "Open",
        "do_not_call_model_2_gauge_equivariant": True,
        "do_not_write_axioms": True,
        "averaged": False,
        "side": "L",
        "right": RIGHT_LEDGER,
        "right_averaged": False,
        "not_a_new_graph": True,
        "not_op3": True,
        "rows": list(SETS),
        "columns": list(SIDES),
        "sources": sources,
        "cells": cells,
        "known": {
            "Lsg_hopf_height_left_j": "4→5",
            "Lang_hopf_y1": "8→9",
            "L0_empty_cut": "undefined_or_vacuous, not keep-rate 1.0",
        },
        "claim_lock": {
            "kind": "ledger_increment",
            "not_an_axiom": True,
            "model_2_gauge_equivariant": False,
            "op3_entered": False,
            "op3_status": "Open",
            "gate": "do not enter OP3 here",
            "not_a_new_graph": True,
            "averaged": False,
            "not_invariance": True,
            "forbids": (
                "Do not write OP2 axioms from these cells. "
                "Lsg height moves under left-j; Lang y1 moves under both left units; "
                "L0 periodicity stays vacuous because zeros are levels, not crossings."
            ),
        },
        "note": (
            "Ledger increment, not an axiom. Assembled from scored OP2 JSON. "
            "Candidate edges refused. A/B/C parked. Do not enter OP3 here. "
            "The research problem OP3 remains Open. This is not invariance. "
            "Right-gauge columns are a sibling ledger, not averaged into this table."
        ),
    }


def _build_model2(set_name: str, attach: Path) -> dict[str, Any]:
    """Same Model 2 graph as the 20260911 OP2 rows. Not a new adjacency."""
    if set_name not in SETS:
        raise SystemExit(f"unknown set {set_name!r}")
    op1 = _load_op1_run()
    row = load_op1_row(attach)
    if row.get("set") != set_name:
        raise SystemExit(f"attach set {row.get('set')!r} != {set_name}")
    preset = op1.load_preset("book_default")
    points, meta = op1.BUILDERS[set_name](preset)
    if set_name == "Lsg":
        sc = meta.get("fiber_base_scatter_max")
        if sc is None or sc >= 1e-8:
            raise SystemExit(f"Lsg hopf_map scatter {sc} is not < 1e-8")
    topo = build_flux_topograph(
        points,
        adjacency="structure_group",
        functional="hopf_height",
        op1_row=row,
    )
    along = list(topo.meta.get("along") or [])
    inter = list(topo.meta.get("inter") or [])
    kirchhoff = kirchhoff_report(
        fiber_cycle_flux(points), len(points), support=along + inter
    )
    if not kirchhoff["kirchhoff"] or not kirchhoff["support_subset_of_skeleton"]:
        raise SystemExit(f"non-Kirchhoff or off-skeleton Φ on {set_name}: {kirchhoff}")
    return {
        "row": row,
        "points": points,
        "along": along,
        "inter": inter,
        "kirchhoff": kirchhoff,
        "census": (row.get("experiment1") or {}).get("fiber_census") or {},
        "attached_op1": str(Path(attach).resolve().relative_to(ROOT)),
    }


def _score_gauge_keys(t: Any, set_name: str, gauge: str) -> tuple[dict[str, Any], dict[str, Any]]:
    kind = cut_kind_for(set_name)
    prefix = "left" if gauge == "L" else "right"
    eq: dict[str, Any] = {}
    per: dict[str, Any] = {}
    for uname in ("i", "j"):
        seq = [(gauge, UNIT_VEC[uname])]
        key = f"{prefix}_{uname}"
        eq[key] = separator_equivariance_score(t, seq, mode="strict_sign")
        per[key] = periodicity_score(t, seq, cut="strict_sign", cut_kind=kind)
    return eq, per


def assemble_equivariance_matrix_right(*, root: Path = ROOT) -> dict[str, Any]:
    """3×2 right-gauge ledger on the same Model 2 graphs. Not averaged with left."""
    cells: dict[str, Any] = {}
    sources: dict[str, Any] = {}
    for set_name in SETS:
        attach = root / "notes" / "op1_runs" / OP1_DEFAULTS[set_name].name
        if not attach.is_file():
            attach = OP1_DEFAULTS[set_name]
        if not attach.is_file():
            raise SystemExit(f"missing OP1 attach {attach}")
        built = _build_model2(set_name, attach)
        row = built["row"]
        points = built["points"]
        sources[set_name] = {
            "op2_left_scored": str(OP2_SCORED[set_name].relative_to(ROOT)),
            "op1": built["attached_op1"],
            "graph": "structure_group (same Model 2 skeleton as 20260911, not a new adjacency)",
            "gauge": "R",
        }
        set_cells: dict[str, Any] = {}
        scored_blocks: dict[str, Any] = {}
        for fname in DEFAULT_FUNCTIONALS:
            t = build_flux_topograph(
                points,
                adjacency="structure_group",
                functional=fname,  # type: ignore[arg-type]
                op1_row=row,
            )
            eq, per = _score_gauge_keys(t, set_name, "R")
            scored_blocks[fname] = {
                "equivariance": eq,
                "periodicity": per,
            }
        for side in RIGHT_SIDES:
            keep = _op1_keep(row, SIDE_UNIT[side], "R")
            cell: dict[str, Any] = {
                "op1": {
                    "unit_name": SIDE_UNIT[side],
                    "side": "R",
                    "along_kept": keep.get("along_kept"),
                    "inter_kept": keep.get("inter_kept"),
                    "n_along": keep.get("n_along"),
                    "n_inter": keep.get("n_inter"),
                    "note": (
                        "OP1 Experiment 2 on this attach, right side only. "
                        "Not averaged with left or with i/j. "
                        "Empty OP2 cut is not keep-rate 1.0."
                    ),
                }
            }
            for fname, block in scored_blocks.items():
                cell[fname] = _functional_cell(block, side)
            set_cells[side] = cell
        cells[set_name] = set_cells
    return {
        "schema": MATRIX_SCHEMA,
        "claim": "Software fact",
        "op1_status": "Open",
        "op2_status": "Open",
        "op3_status": "Open",
        "do_not_call_model_2_gauge_equivariant": True,
        "do_not_write_axioms": True,
        "averaged": False,
        "side": "R",
        "left": LEFT_LEDGER,
        "left_averaged": False,
        "not_a_new_graph": True,
        "not_op3": True,
        "rows": list(SETS),
        "columns": list(RIGHT_SIDES),
        "sources": sources,
        "cells": cells,
        "known": {
            "Lsg_hopf_height_right_j": "4→5",
            "Lang_hopf_y1": "8→9",
            "Lang_inter_kept_right": "i=0.811 j=0.833, not left 0.944/0.811",
            "L0_empty_cut": "undefined_or_vacuous, not keep-rate 1.0",
            "not_averaged_with_left": True,
        },
        "claim_lock": {
            "kind": "ledger_increment",
            "not_an_axiom": True,
            "model_2_gauge_equivariant": False,
            "op3_entered": False,
            "op3_status": "Open",
            "gate": "do not enter OP3 here",
            "not_a_new_graph": True,
            "averaged": False,
            "not_invariance": True,
            "forbids": (
                "Do not write OP2 axioms from these cells. "
                "Do not average with the left ledger. Do not fold the two files. "
                "Matching component integers (Lsg height j 4→5, Lang y1 8→9) and "
                "matching edge moves on those cuts (Lsg j 5→7, Lang y1 j 37→38) "
                "do not identify the ledgers. Lang inter_kept already differs "
                "(left 0.944/0.811 vs right 0.811/0.833). L0 stays vacuous because "
                "zeros are levels, not crossings."
            ),
        },
        "note": (
            "Right-gauge ledger increment, not an axiom. Same Model 2 graphs as "
            "the 20260911 OP2 rows. Not averaged with left-i/left-j. "
            "Candidate edges refused. Do not enter OP3 here. This is not invariance."
        ),
    }


def cut_kind_for(set_name: str) -> str:
    if set_name == "Lang":
        return "delaunay_periodicity"
    if set_name == "Lsg":
        return "separator_component_count"
    return "undefined_or_vacuous_if_empty_cut"


def summarize_seps(components: list[list[tuple[int, int]]]) -> dict[str, Any]:
    n_edges = sum(len(c) for c in components)
    sizes = sorted((len(c) for c in components), reverse=True)
    return {
        "n_components": len(components),
        "n_separator_edges": n_edges,
        "component_sizes": sizes,
    }


def run_one(
    set_name: str,
    *,
    attach: Path,
    functionals: tuple[str, ...] = DEFAULT_FUNCTIONALS,
) -> dict[str, Any]:
    if set_name not in ("Lsg", "L0", "Lang"):
        raise SystemExit(f"unknown set {set_name!r}")
    op1 = _load_op1_run()
    row = load_op1_row(attach)
    if row.get("set") != set_name:
        raise SystemExit(f"attach set {row.get('set')!r} != --set {set_name}")
    preset = op1.load_preset("book_default")
    points, meta = op1.BUILDERS[set_name](preset)
    if set_name == "Lsg":
        sc = meta.get("fiber_base_scatter_max")
        if sc is None or sc >= 1e-8:
            raise SystemExit(f"Lsg hopf_map scatter {sc} is not < 1e-8")

    topo = build_flux_topograph(
        points,
        adjacency="structure_group",
        functional="hopf_height",
        op1_row=row,
    )
    along = list(topo.meta.get("along") or [])
    inter = list(topo.meta.get("inter") or [])
    skeleton = along + inter
    flux = fiber_cycle_flux(points)
    kirchhoff = kirchhoff_report(flux, len(points), support=skeleton)
    if not kirchhoff["kirchhoff"] or not kirchhoff["support_subset_of_skeleton"]:
        raise SystemExit(
            f"non-Kirchhoff or off-skeleton Φ on {set_name}: {kirchhoff}"
        )

    census = (row.get("experiment1") or {}).get("fiber_census") or {}
    functionals_out: dict[str, Any] = {}
    for fname in functionals:
        t = build_flux_topograph(
            points,
            adjacency="structure_group",
            functional=fname,  # type: ignore[arg-type]
            op1_row=row,
        )
        seps = detect_separators(t, mode="strict_sign")
        eq_i = separator_equivariance_score(
            t, [("L", I_UNIT)], mode="strict_sign"
        )
        eq_j = separator_equivariance_score(
            t, [("L", J_UNIT)], mode="strict_sign"
        )
        kind = cut_kind_for(set_name)
        per_i = periodicity_score(
            t, [("L", I_UNIT)], cut="strict_sign", cut_kind=kind
        )
        per_j = periodicity_score(
            t, [("L", J_UNIT)], cut="strict_sign", cut_kind=kind
        )
        block: dict[str, Any] = {
            "separators": summarize_seps(seps),
            "equivariance": {
                "left_i": eq_i,
                "left_j": eq_j,
                "note": "Not averaged. Same split as OP1 along_kept.",
            },
            "periodicity": {
                "left_i": per_i,
                "left_j": per_j,
                "note": (
                    "Empty cut → undefined_or_vacuous (no invented crossings). "
                    "Lang height is Delaunay periodicity, not |ad-bc|=1. "
                    "Not averaged over i/j."
                ),
            },
        }
        if set_name == "L0":
            block["pole_level_sets"] = pole_level_sets(points, fname)  # type: ignore[arg-type]
            block["do_not_count_zero_as_crossing"] = True
        if set_name == "Lang" and fname == "hopf_y1":
            block["op1_inter_kept"] = {
                "left_i": _op1_keep(row, "i", "L"),
                "left_j": _op1_keep(row, "j", "L"),
                "note": (
                    "8→9 component move is OP1 inter_kept<1 visible in OP2. "
                    "Do not smooth it."
                ),
            }
        functionals_out[fname] = block

    return {
        "schema": SCHEMA,
        "claim": "Software fact",
        "op2_status": "Open",
        "op1_status": "Open",
        "set": set_name,
        "rule": "structure_group",
        "adjacency": "structure_group",
        "skeleton": "Model 2 — not a theorem of Ch. 5",
        "n_points": int(len(points)),
        "n_along": int(len(along)),
        "n_inter": int(len(inter)),
        "attached_op1": str(Path(attach).resolve().relative_to(ROOT)),
        "fiber_census": census,
        "support": {
            "phi": "fiber_cycle_flux: +1 on each oriented U(1) occupancy cycle",
            "kirchhoff": kirchhoff,
        },
        "functionals": functionals_out,
        "do_not_mix_with_candidate": True,
        "do_not_promote": ["flux_hopf_lib", "qga_engine"],
    }


def _json_ready(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _json_ready(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_ready(v) for v in obj]
    if isinstance(obj, tuple):
        return [_json_ready(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# OP2 topograph harness — {payload['set']} / structure_group",
        "",
        "Claim type: **Software fact**. OP2 status: **Open**. Skeleton is a Model choice.",
        "OP1 remains Open. Not Ch. 5 axioms.",
        "",
        f"- attached OP1: `{payload['attached_op1']}`",
        f"- n_points = {payload['n_points']}  n_along = {payload['n_along']}  n_inter = {payload['n_inter']}",
        f"- Kirchhoff: {payload['support']['kirchhoff']['kirchhoff']} "
        f"(max |r| = {payload['support']['kirchhoff']['max_abs_residual']})",
        "",
        "### Fiber census (from attached OP1 row)",
        "",
    ]
    c = payload.get("fiber_census") or {}
    if c:
        lines += [
            f"- n_distinct_bases = {c.get('n_distinct_bases')}",
            f"- multiplicity = {c.get('multiplicity_histogram')}",
            f"- along_kind = `{c.get('along_kind')}`",
            "",
        ]
        img = c.get("image") or {}
        if img:
            lines.append(f"- image: `{img.get('object')}` **{img.get('claim')}**")
            lines.append("")
    lines += ["## Separators (strict sign-crossing) and left-i / left-j", "", 
              "| functional | n_components | n_sep_edges | left-i n_comp after | left-j n_comp after | periodicity |",
              "|---|---|---|---|---|---|"]
    for fname, block in payload["functionals"].items():
        s = block["separators"]
        ei = block["equivariance"]["left_i"]
        ej = block["equivariance"]["left_j"]
        pi = block.get("periodicity", {}).get("left_i") or {}
        pj = block.get("periodicity", {}).get("left_j") or {}
        per = f"i:{pi.get('status')} j:{pj.get('status')}"
        if pi.get("status") == "finite":
            per = (
                f"i {pi.get('n_components_before')}→{pi.get('n_components_after')} "
                f"j {pj.get('n_components_before')}→{pj.get('n_components_after')} "
                f"({pi.get('kind')})"
            )
        lines.append(
            f"| {fname} | {s['n_components']} | {s['n_separator_edges']} | "
            f"{int(ei['n_components_after'])} | {int(ej['n_components_after'])} | {per} |"
        )
        poles = block.get("pole_level_sets")
        if poles:
            lines.append("")
            lines.append(f"Pole level sets for `{fname}` (zeros are levels, not crossings):")
            for row in poles:
                b = row["base"]
                lines.append(
                    f"- base {b} ×{row['multiplicity']}: value={row['value']}"
                )
            lines.append("")
        kept = block.get("op1_inter_kept")
        if kept:
            lines.append(
                f"OP1 inter_kept attached for `{fname}`: "
                f"left-i={kept['left_i'].get('inter_kept')} "
                f"left-j={kept['left_j'].get('inter_kept')}. {kept.get('note')}"
            )
            lines.append("")
    lines += ["", "Do not average L/R or i/j. Do not mix candidate edges.", ""]
    return "\n".join(lines)


def _cell_md(cell: dict[str, Any]) -> str:
    tag = cell.get("ledger")
    if tag == "undefined_or_vacuous":
        return "`undefined_or_vacuous`"
    n0 = cell.get("n_components_before")
    n1 = cell.get("n_components_after")
    arrow = f"{n0}→{n1}" if n1 is not None else f"{n0}→∅"
    return f"`{arrow}` `{tag}`"


def render_matrix_markdown(payload: dict[str, Any]) -> str:
    cols = list(payload["columns"])
    lines = [
        "# OP2 equivariance matrix (ledger)",
        "",
        "Recorded as an OP2 **ledger increment**. No axiom, no new graph, OP3 not entered.",
        "",
        "## Claim lock",
        "",
        "- The equivariance matrix is a **ledger**, not an axiom.",
        "- Model 2 is **not** gauge-equivariant.",
        "- This increment does **not** open OP3. The research problem OP3 remains **Open**; "
        "the gate is “do not enter it here.”",
        "- No new graph. Candidate edges stay refused.",
        (
            r"- Right-\(i\) / right-\(j\) are not averaged, and not averaged with the left ledger."
            if payload.get("side") == "R"
            else r"- Left-\(i\) / left-\(j\) are not averaged. Right is a sibling ledger."
        ),
        "",
        "Claim type: **Software fact**. OP2 status: **Open**.",
        "Not Ch. 5 axioms. Do **not** call Model 2 gauge-equivariant.",
        "",
        (
            "Right-gauge columns on the same Model 2 graphs. Not averaged with left."
            if payload.get("side") == "R"
            else "Assembled from scored OP2 JSON (left-gauge). Right is a sibling ledger."
        ),
        "",
    ]
    for set_name in payload["rows"]:
        src = payload["sources"][set_name]
        op2_ref = src.get("op2") or src.get("op2_left_scored")
        lines.append(f"- `{set_name}`: `{op2_ref}` ← `{src['op1']}`")
    lines += [
        "",
        "Empty cut stays `undefined_or_vacuous` under gauge, **not** keep-rate 1.0.",
        "",
        "## hopf_height (n_components before→after)",
        "",
        "| | " + " | ".join(COL_LABEL[c] for c in cols) + " |",
        "|" + "|".join(["---"] * (1 + len(cols))) + "|",
    ]
    for set_name in payload["rows"]:
        bits = " | ".join(_cell_md(payload["cells"][set_name][c]["hopf_height"]) for c in cols)
        lines.append(f"| {set_name} | {bits} |")
    lines += [
        "",
        "## hopf_y1 (n_components before→after)",
        "",
        "| | " + " | ".join(COL_LABEL[c] for c in cols) + " |",
        "|" + "|".join(["---"] * (1 + len(cols))) + "|",
    ]
    for set_name in payload["rows"]:
        bits = " | ".join(_cell_md(payload["cells"][set_name][c]["hopf_y1"]) for c in cols)
        lines.append(f"| {set_name} | {bits} |")
    side_word = "right" if payload.get("side") == "R" else "left"
    lines += [
        "",
        f"## OP1 inter_kept ({side_word}, not averaged)",
        "",
        "| | " + " | ".join(COL_LABEL[c] for c in cols) + " |",
        "|" + "|".join(["---"] * (1 + len(cols))) + "|",
    ]
    for set_name in payload["rows"]:
        bits = " | ".join(str(payload["cells"][set_name][c]["op1"].get("inter_kept")) for c in cols)
        lines.append(f"| {set_name} | {bits} |")
    lines += [
        "",
        r"L0 `inter_kept = 1` on Lipschitz \(i,j\) is a **different object** from the empty "
        "strict-sign cut. That cell is not keep-rate 1.0. "
        + (
            "Lang right `inter_kept` is not averaged with left or with i/j."
            if payload.get("side") == "R"
            else "Lang left `inter_kept` is 0.944 / 0.811, not averaged."
        ),
        "",
        "## What this forbids",
        "",
        str((payload.get("claim_lock") or {}).get("forbids") or "")
        + " That is the content of the ledger. It is not invariance.",
        "",
    ]
    return "\n".join(lines)


def write_matrix(
    payload: dict[str, Any], out_dir: Path, *, stem: str | None = None
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    if stem is None:
        day = date.today().strftime("%Y%m%d")
        suffix = "_right" if payload.get("side") == "R" else ""
        stem = f"{day}_equivariance_matrix{suffix}"
    payload = _json_ready(payload)
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_matrix_markdown(payload), encoding="utf-8")
    return json_path, md_path


def write_run(payload: dict[str, Any], out_dir: Path, *, stem: str | None = None) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    if stem is None:
        day = date.today().strftime("%Y%m%d")
        stem = f"{day}_{payload['set']}_structure_group"
    payload = _json_ready(payload)
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, md_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--set", dest="set_name", default="Lsg", choices=["Lsg", "L0", "Lang", "all"])
    p.add_argument("--rule", default="structure_group", choices=["structure_group"])
    p.add_argument("--attach", type=Path, default=None)
    p.add_argument(
        "--matrix",
        action="store_true",
        help="assemble the 3×2 left-gauge equivariance ledger from scored OP2 JSON (not a new graph)",
    )
    p.add_argument(
        "--matrix-right",
        action="store_true",
        dest="matrix_right",
        help="score right-i/right-j on the same Model 2 graphs; sibling ledger, not averaged with left",
    )
    p.add_argument("--out-dir", type=Path, default=ROOT / "notes" / "op2_runs")
    p.add_argument("--stem", default=None)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.rule != "structure_group":
        raise SystemExit("OP2 harness only accepts --rule structure_group")
    if args.matrix and args.matrix_right:
        raise SystemExit("use --matrix or --matrix-right, not both (tables are not averaged)")
    if args.matrix:
        payload = assemble_equivariance_matrix()
        json_path, md_path = write_matrix(payload, args.out_dir, stem=args.stem)
        print(json_path)
        print(md_path)
        print(render_matrix_markdown(payload))
        return 0
    if args.matrix_right:
        payload = assemble_equivariance_matrix_right()
        json_path, md_path = write_matrix(payload, args.out_dir, stem=args.stem)
        print(json_path)
        print(md_path)
        print(render_matrix_markdown(payload))
        return 0
    sets = ["Lsg", "L0", "Lang"] if args.set_name == "all" else [args.set_name]
    # Lsg first: if it fails Kirchhoff, stop before L0/Lang
    order = [s for s in ["Lsg", "L0", "Lang"] if s in sets]
    for s in order:
        attach = args.attach or OP1_DEFAULTS[s]
        if not attach.is_file():
            raise SystemExit(f"missing OP1 attach {attach}")
        payload = run_one(s, attach=attach)
        json_path, md_path = write_run(payload, args.out_dir, stem=args.stem)
        print(json_path)
        print(md_path)
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
