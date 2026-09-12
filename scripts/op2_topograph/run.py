#!/usr/bin/env python3
"""OP2 flux-topograph harness on Model 2 only.

Software facts. OP2 stays Open. Does not close OP1. Does not use
candidate_adjacency as the analysis skeleton.
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
    p.add_argument("--out-dir", type=Path, default=ROOT / "notes" / "op2_runs")
    p.add_argument("--stem", default=None)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.rule != "structure_group":
        raise SystemExit("OP2 harness only accepts --rule structure_group")
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
