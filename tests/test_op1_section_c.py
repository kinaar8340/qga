"""OP1-C: other sections on the same L0 graph. Software fact. OP1 Open."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from lib.hopf_lattice import HURWITZ_UNITS, structure_group_adjacency

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "op1_adjacency" / "section_c.py"
GRAPH = (
    ROOT
    / "notes"
    / "op1_runs"
    / "20260911_L0_book_default_exact_structure_group_graph.json"
)
LEDGER = ROOT / "notes" / "op1_runs" / "20260913_L0_section_C.json"


def _load():
    spec = importlib.util.spec_from_file_location("op1_section_c", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def section_c():
    return _load()


def test_refuse_candidate_and_lang(section_c):
    with pytest.raises(SystemExit, match="candidate"):
        section_c.main(["--set", "L0", "--rule", "candidate", "--attach", str(GRAPH)])
    with pytest.raises(SystemExit, match="L0"):
        section_c.main(["--set", "Lang", "--rule", "structure_group", "--attach", str(GRAPH)])


def test_source_no_third_graph():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "candidate_adjacency" not in text
    assert "legacy_portal_map" not in text
    assert "dump-graph" not in text


def test_default_section_still_min_index():
    along, inter = structure_group_adjacency(HURWITZ_UNITS)
    along_m, inter_m = structure_group_adjacency(HURWITZ_UNITS, gauge_section="min_index")
    assert along == along_m
    assert inter == inter_m


def test_c_same_graph_along_invariant_overlap_invariant(section_c, tmp_path):
    rc = section_c.main(
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
            "section_c",
        ]
    )
    assert rc == 0
    payload = json.loads((tmp_path / "section_c.json").read_text(encoding="utf-8"))
    assert payload["schema"] == "op1_section_c_v1"
    assert payload["claim"] == "Software fact"
    assert payload["op1_status"] == "Open"
    assert payload["op3_entered"] is False
    assert payload["not_a_third_graph"] is True
    assert payload["set"] == "L0"
    assert payload["along_section_invariant"] is True
    assert payload["overlap_invariant"] is True
    assert payload["overlap_values"] == [8]
    assert payload["inter_index_sets_distinct"] == 3
    assert payload["rows"]["min_index"]["inter_index_equals_graph"] is True
    assert payload["rows"]["max_index"]["inter_index_equals_graph"] is False
    assert payload["rows"]["max_real"]["inter_index_equals_graph"] is False
    assert payload["rows"]["min_index"]["half_left"]["inter_kept_value"] == pytest.approx(5 / 12)
    assert payload["rows"]["max_index"]["half_left"]["inter_kept_value"] == pytest.approx(5 / 12)
    assert payload["rows"]["max_real"]["half_left"]["inter_kept_constant"] is False
    assert payload["half_inter_kept_invariant"] is False


def test_c_ledger_file(section_c):
    if not LEDGER.is_file():
        pytest.skip("C ledger not written")
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = section_c.run_c(section_c._farey.load_graph(GRAPH))
    assert data["overlap_values"] == live["overlap_values"] == [8]
    assert data["inter_index_sets_distinct"] == 3
    assert data["op3_entered"] is False
    lock = data["claim_lock"]
    assert lock["same_l0_graph"] is True
    assert lock["not_a_third_adjacency"] is True
    assert lock["do_not_fold_into_slice_A"] is True
    assert lock["default_gauge_section"] == "min_index"
    assert lock["overlap_stays_8_of_12"] is True
    assert lock["half_keep_moves_only_under_max_real"] is True
    md = (LEDGER.with_suffix(".md")).read_text(encoding="utf-8")
    assert "Claim lock" in md
    assert "Do not fold C into slice A" in md
    assert "Keep the two dumps separate" in md
    notes = (ROOT / "notes" / "open_problems.md").read_text(encoding="utf-8")
    assert "20260913_L0_section_C.json" in notes
    assert "do not fold c into slice a" in notes.lower()
