"""OP1-A Farey slice on L0. Software fact. Status stays Open."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SLICE_PY = ROOT / "scripts" / "op1_adjacency" / "farey_slice.py"
GRAPH = (
    ROOT
    / "notes"
    / "op1_runs"
    / "20260911_L0_book_default_exact_structure_group_graph.json"
)
LEDGER = (
    ROOT
    / "notes"
    / "op1_runs"
    / "20260911_L0_structure_group_farey_slice_A.json"
)
HARNESS_DIR = ROOT / "scripts" / "op1_adjacency"


def _load():
    spec = importlib.util.spec_from_file_location("op1_farey_slice", SLICE_PY)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def slice_mod():
    return _load()


def test_source_does_not_recompute_adjacency():
    text = SLICE_PY.read_text(encoding="utf-8")
    assert "structure_group_adjacency" not in text
    assert "candidate_adjacency" not in text
    assert "legacy_portal_map" not in text


def test_refuse_candidate(slice_mod):
    with pytest.raises(SystemExit, match="structure_group"):
        slice_mod.main(
            [
                "--set",
                "L0",
                "--rule",
                "candidate",
                "--attach",
                str(GRAPH),
            ]
        )


def test_refuse_lang(slice_mod):
    with pytest.raises(SystemExit, match="L0 only"):
        slice_mod.main(
            [
                "--set",
                "Lang",
                "--rule",
                "structure_group",
                "--attach",
                str(GRAPH),
            ]
        )


def test_l0_slice_schema_and_counts(slice_mod, tmp_path):
    rc = slice_mod.main(
        [
            "--set",
            "L0",
            "--rule",
            "structure_group",
            "--attach",
            str(GRAPH),
            "--out-dir",
            str(tmp_path),
            "--stem",
            "slice_A",
        ]
    )
    assert rc == 0
    payload = json.loads((tmp_path / "slice_A.json").read_text(encoding="utf-8"))
    assert payload["schema"] == "op1_farey_slice_v1"
    assert payload["claim"] == "Software fact"
    assert payload["op1_status"] == "Open"
    assert payload["slice"] == "A"
    assert payload["slice_status"].startswith("Partial result (slice A only)")
    assert "Classical Q Farey still open" in payload["slice_status"]
    assert payload["claims"]["embedding_chart"] == "Theorem"
    assert payload["claims"]["overlap_counts"] == "Software fact"
    assert "quaternionic Farey reduces" not in payload["statement"]
    assert "not Q" in payload["statement"]
    assert payload["embedding"]["name"] == "stereographic_from_north"
    assert payload["embedding"]["p1_set"] == ["0", "inf", "1", "-1", "i", "-i"]
    assert payload["n_model2_inter"] == 12
    assert payload["n_overlap"] + payload["n_miss"] == 12
    assert payload["n_overlap"] == 8
    assert payload["n_miss"] == 4
    assert payload["farey_not_in_model2"] == [["0", "inf"]]
    miss = {tuple(p) for p in payload["miss"]}
    assert miss == {("1", "i"), ("1", "-i"), ("-1", "i"), ("-1", "-i")}
    assert "Q" in payload["embedding"]["note"] or "Q∪" in payload["statement"] or "Q" in payload["statement"]


def test_poles_are_named_p1(slice_mod):
    assert slice_mod.pole_label([0.0, 0.0, 1.0]) == "inf"
    assert slice_mod.pole_label([0.0, 0.0, -1.0]) == "0"
    assert slice_mod.pole_label([1.0, 0.0, 0.0]) == "1"
    assert slice_mod.pole_label([-1.0, 0.0, 0.0]) == "-1"
    assert slice_mod.pole_label([0.0, 1.0, 0.0]) == "i"
    assert slice_mod.pole_label([0.0, -1.0, 0.0]) == "-i"


def test_zero_inf_is_farey_but_not_model2_inter(slice_mod):
    ok, det = slice_mod.det_unit("0", "inf")
    assert ok
    assert abs(abs(det) - 1.0) < 1e-12


def test_ledger_matches_live(slice_mod, tmp_path):
    assert LEDGER.is_file(), f"missing ledger {LEDGER}"
    slice_mod.main(
        [
            "--set",
            "L0",
            "--rule",
            "structure_group",
            "--attach",
            str(GRAPH),
            "--out-dir",
            str(tmp_path),
            "--stem",
            "slice_A",
        ]
    )
    live = json.loads((tmp_path / "slice_A.json").read_text(encoding="utf-8"))
    gold = json.loads(LEDGER.read_text(encoding="utf-8"))
    for key in (
        "n_overlap",
        "n_miss",
        "n_model2_inter",
        "n_farey_on_set",
        "miss",
        "overlap",
        "farey_not_in_model2",
        "op1_status",
        "slice_status",
        "claim",
        "claims",
    ):
        assert live[key] == gold[key], key
