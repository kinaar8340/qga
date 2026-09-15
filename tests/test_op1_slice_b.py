"""OP1-B is an index, not a new keep-rate experiment."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POINTER = ROOT / "notes" / "op1_runs" / "20260911_slice_B_keep_rate.md"
LSG = ROOT / "notes" / "op1_runs" / "20260911_Lsg_book_default_none_structure_group.json"
L0 = ROOT / "notes" / "op1_runs" / "20260911_L0_book_default_exact_structure_group.json"


def test_b_is_index_not_new_matrix():
    text = POINTER.read_text(encoding="utf-8")
    assert "B indexed, not extended" in text
    assert "Software fact" in text
    assert "Open" in text
    assert "Do not rerun" in text
    assert LSG.name in text
    assert L0.name in text
    assert "Lang dump" in text
    assert "candidate" in text
    assert "parked" in text
    for path, n_along, n_inter in ((LSG, 64, 6), (L0, 24, 12)):
        row = json.loads(path.read_text(encoding="utf-8"))
        assert row["rule"] == "structure_group"
        e2 = row["experiment2"]
        assert len(e2) == 48
        assert e2[0]["n_along"] == n_along
        assert e2[0]["n_inter"] == n_inter
