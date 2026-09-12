#!/usr/bin/env python3
"""OP1-A: Farey slice on L0's six octahedron poles.

Reads a dumped ``qga_adjacency_graph_v1`` (Model 2 inter-edges). Does not
recompute adjacency. Does not dump Lang. Does not port Model 2.

Embedding: stereographic-from-north sends the poles to
``{0, inf, ±1, ±i} ⊂ P¹(C)``. Farey means ``|ad−bc|=1`` over ``Z[i]``
(determinant is a unit). Software fact. OP1 stays Open.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCHEMA = "op1_farey_slice_v1"
GRAPH_KIND = "qga_adjacency_graph_v1"
DEFAULT_GRAPH = (
    ROOT
    / "notes"
    / "op1_runs"
    / "20260911_L0_book_default_exact_structure_group_graph.json"
)

# P¹(C) labels in a stable order.
P1_SET = ("0", "inf", "1", "-1", "i", "-i")
LABEL_ORDER = {lab: i for i, lab in enumerate(P1_SET)}

# Homogeneous [z:w] as Gaussian integers (z, w) ∈ Z[i]².
HOMOGENEOUS: dict[str, tuple[complex, complex]] = {
    "0": (0 + 0j, 1 + 0j),
    "inf": (1 + 0j, 0 + 0j),
    "1": (1 + 0j, 1 + 0j),
    "-1": (-1 + 0j, 1 + 0j),
    "i": (0 + 1j, 1 + 0j),
    "-i": (0 - 1j, 1 + 0j),
}

UNITS_ZI = frozenset({1 + 0j, -1 + 0j, 1j, -1j})

POLE_TO_LABEL = {
    (0.0, 0.0, 1.0): "inf",
    (0.0, 0.0, -1.0): "0",
    (1.0, 0.0, 0.0): "1",
    (-1.0, 0.0, 0.0): "-1",
    (0.0, 1.0, 0.0): "i",
    (0.0, -1.0, 0.0): "-i",
}


def _c_json(z: complex) -> list[float]:
    return [float(z.real), float(z.imag)]


def pair_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b), key=lambda x: LABEL_ORDER[x]))  # type: ignore[return-value]


def load_graph(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("kind") != GRAPH_KIND:
        raise SystemExit(
            f"attach is not {GRAPH_KIND} (got {data.get('kind')!r}); "
            "not export_fiber_curves and not a third adjacency"
        )
    if "fibers" in data:
        raise SystemExit("graph payload must not carry fibers[]")
    return data


def pole_label(base: list[float], *, tol: float = 1e-8) -> str:
    """Stereographic-from-north: z = (y1 + i y2) / (1 − y3). North → inf."""
    y1, y2, y3 = (float(c) for c in base)
    key = (round(y1, 8), round(y2, 8), round(y3, 8))
    # Collapse -0.0
    key = tuple(0.0 if abs(c) < tol else float(c) for c in key)
    if key in POLE_TO_LABEL:
        return POLE_TO_LABEL[key]
    if abs(1.0 - y3) < tol:
        raise SystemExit(f"base {base} is north but not the octahedron pole")
    z = (y1 + 1j * y2) / (1.0 - y3)
    for lab, (num, den) in HOMOGENEOUS.items():
        if den == 0:
            continue
        if abs(z - num / den) < 1e-6:
            return lab
    raise SystemExit(f"base {base} is not in {{0,inf,±1,±i}} under stereographic-from-north")


def det_unit(p: str, q: str) -> tuple[bool, complex]:
    a, c = HOMOGENEOUS[p]
    b, d = HOMOGENEOUS[q]
    det = a * d - c * b
    return det in UNITS_ZI, det


def farey_pairs_on_set() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for i, p in enumerate(P1_SET):
        for q in P1_SET[i + 1 :]:
            ok, _det = det_unit(p, q)
            if ok:
                out.append(pair_key(p, q))
    return out


def model2_inter_labels(graph: dict[str, Any]) -> list[tuple[str, str]]:
    points = graph["points"]
    edges = graph["inter"]
    out: list[tuple[str, str]] = []
    for e in edges:
        i, j = int(e[0]), int(e[1])
        a = pole_label(points[i]["base"])
        b = pole_label(points[j]["base"])
        if a == b:
            raise SystemExit(f"inter-edge {e} is same-fiber ({a}); not a base edge")
        out.append(pair_key(a, b))
    return out


def run_slice(graph: dict[str, Any], *, graph_path: Path) -> dict[str, Any]:
    if graph.get("set") != "L0":
        raise SystemExit("OP1-A is L0 only in this increment (Lang waits)")
    if graph.get("rule") != "structure_group":
        raise SystemExit(
            f"OP1-A attaches Model 2 only; refused rule={graph.get('rule')!r}"
        )
    inter = graph.get("inter") or []
    if len(inter) != 12:
        raise SystemExit(f"L0 Model 2 inter must be 12, got {len(inter)}")

    model = model2_inter_labels(graph)
    farey = farey_pairs_on_set()
    model_set = set(model)
    farey_set = set(farey)
    overlap = sorted(model_set & farey_set, key=lambda p: (LABEL_ORDER[p[0]], LABEL_ORDER[p[1]]))
    miss = sorted(model_set - farey_set, key=lambda p: (LABEL_ORDER[p[0]], LABEL_ORDER[p[1]]))
    farey_not_model = sorted(
        farey_set - model_set, key=lambda p: (LABEL_ORDER[p[0]], LABEL_ORDER[p[1]])
    )
    dets = {
        f"{p}--{q}": _c_json(det_unit(p, q)[1])
        for i, p in enumerate(P1_SET)
        for q in P1_SET[i + 1 :]
    }
    try:
        rel = str(graph_path.resolve().relative_to(ROOT))
    except ValueError:
        rel = str(graph_path)

    n_overlap = len(overlap)
    n_miss = len(miss)
    statement = (
        "slice A on L0: 8/12 Gaussian-Farey overlap; equatorial square missed; "
        "antipode extra; not Q. "
        f"{n_overlap} of 12 Model 2 inter-edges are Z[i] neighbors "
        "(|ad-bc|=1, units ±1, ±i) under stereographic-from-north "
        "(polar stars 0–equator and inf–equator). "
        "The 4 misses are the equatorial square {±1, ±i} (dets 1±i, −1±i, "
        "norm 2). Farey-not-Model-2 is only {0, inf} (det −1, d_S=π). "
        "Model 2 on h(Λ0) is the octahedron 1-skeleton, not the Gaussian "
        "Farey graph on the same six points. They share the two polar stars "
        "and differ on the equator and the axis. "
        "This is P¹(C) with Z[i], not Hatcher's Q∪{∞}. OP1 stays Open."
    )
    return {
        "schema": SCHEMA,
        "claim": "Software fact",
        "op1_status": "Open",
        "slice": "A",
        "slice_status": (
            "Partial result (slice A only): Z[i] neighbors on h(Λ0). "
            "Classical Q Farey still open."
        ),
        "claims": {
            "embedding_chart": "Theorem",
            "embedding_dump": "Software fact",
            "overlap_counts": "Software fact",
            "not": "not Q∪{∞}↪S²; not a bump of OP1",
        },
        "set": "L0",
        "rule": "structure_group",
        "graph": rel,
        "embedding": {
            "name": "stereographic_from_north",
            "formula": "z = (y1 + i y2) / (1 - y3)",
            "north_pole_s2": [0.0, 0.0, 1.0],
            "image": {
                "(0,0,1)": "inf",
                "(0,0,-1)": "0",
                "(1,0,0)": "1",
                "(-1,0,0)": "-1",
                "(0,1,0)": "i",
                "(0,-1,0)": "-i",
            },
            "p1_set": list(P1_SET),
            "chart_claim": "Theorem",
            "dump_claim": "Software fact",
            "note": (
                "Named slice on h(Λ0), the 6 octahedron poles as "
                "{0, inf, ±1, ±i} ⊂ P¹(C). Chart is a Theorem; this dump "
                "is a Software fact. Not Q∪{∞}↪S² (veto 1 still holds for "
                "classical Farey over Q)."
            ),
        },
        "homogeneous": {
            lab: {"z": _c_json(zw[0]), "w": _c_json(zw[1])}
            for lab, zw in HOMOGENEOUS.items()
        },
        "farey_condition": "|ad-bc|=1 over Z[i] (det is a unit ±1, ±i)",
        "n_model2_inter": 12,
        "n_farey_on_set": len(farey),
        "n_overlap": n_overlap,
        "n_miss": n_miss,
        "model2_inter_labels": [list(p) for p in model],
        "farey_pairs": [list(p) for p in farey],
        "overlap": [list(p) for p in overlap],
        "miss": [list(p) for p in miss],
        "farey_not_in_model2": [list(p) for p in farey_not_model],
        "determinants": dets,
        "statement": statement,
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
            "OP1-A is a structure_group witness; refused for "
            f"rule={args.rule!r} (no candidate edges)"
        )
    if args.set_name != "L0":
        raise SystemExit("OP1-A is L0 only in this increment (Lang waits)")
    graph = load_graph(args.attach)
    if graph.get("set") != args.set_name:
        raise SystemExit(
            f"attach set {graph.get('set')!r} != --set {args.set_name!r}"
        )
    payload = run_slice(graph, graph_path=args.attach)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.stem or (
        f"{date.today().strftime('%Y%m%d')}_{args.set_name}_"
        f"{args.rule}_farey_slice_A"
    )
    path = args.out_dir / f"{stem}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(path)
    print(payload["statement"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
