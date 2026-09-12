"""L0 left-half death: occupancy 4-cycles are not left-2T invariant."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "op1_adjacency" / "left_half_death.py"
GRAPH = (
    ROOT
    / "notes"
    / "op1_runs"
    / "20260911_L0_book_default_exact_structure_group_graph.json"
)
LEDGER_JSON = ROOT / "notes" / "op1_runs" / "20260912_L0_left_half_death.json"


def _load():
    spec = importlib.util.spec_from_file_location("op1_left_half_death", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def death():
    return _load()


def test_refuse_candidate_and_lang(death):
    with pytest.raises(SystemExit, match="candidate"):
        death.main(["--set", "L0", "--rule", "candidate", "--attach", str(GRAPH)])
    with pytest.raises(SystemExit, match="L0"):
        death.main(["--set", "Lang", "--rule", "structure_group", "--attach", str(GRAPH)])


def test_source_no_third_graph():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "candidate_adjacency" not in text
    assert "legacy_portal_map" not in text


def test_table_split_not_section(death, tmp_path):
    rc = death.main(
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
            "death",
        ]
    )
    assert rc == 0
    payload = json.loads((tmp_path / "death.json").read_text(encoding="utf-8"))
    assert payload["claim"] == "Software fact"
    assert payload["op1_status"] == "Open"
    assert payload["n_lipschitz"] == 8
    assert payload["n_half"] == 16
    assert payload["lipschitz_all_cycles_single_fiber"] is True
    assert payload["lipschitz_along_kept"] == [1.0] * 8
    assert payload["half_all_cycles_split_2_plus_2"] is True
    assert payload["half_along_kept"] == [0.0] * 16
    assert payload["half_inter_kept"] == [5 / 12] * 16
    for row in payload["half"]:
        assert row["n_inter_kept"] == 5
        for c in row["cycles"]:
            assert c["along_recovered"] == 0
            assert len(c["image_fibers"]) == 2
            assert c["image_counts"][c["image_fibers"][0]] == 2
            assert c["image_counts"][c["image_fibers"][1]] == 2


def test_ledger_matches_live(death, tmp_path):
    assert LEDGER_JSON.is_file()
    death.main(
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
            "death",
        ]
    )
    live = json.loads((tmp_path / "death.json").read_text(encoding="utf-8"))
    gold = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))
    for key in (
        "verdict",
        "half_all_cycles_split_2_plus_2",
        "lipschitz_all_cycles_single_fiber",
        "half_along_kept",
        "half_inter_kept",
        "op1_status",
        "claim",
    ):
        assert live[key] == gold[key], key
