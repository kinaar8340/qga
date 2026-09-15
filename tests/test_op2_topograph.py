"""OP2 harness invariants. Skeleton is Model 2. Status stays Open."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

from lib.flux_topograph import (
    build_flux_topograph,
    detect_separators,
    fiber_cycle_flux,
    kirchhoff_report,
    periodicity_score,
    pole_level_sets,
)
from lib.hopf_lattice import HURWITZ_UNITS, hopf_map

ROOT = Path(__file__).resolve().parents[1]
OP2_PY = ROOT / "scripts" / "op2_topograph" / "run.py"
OP1_LSG = ROOT / "notes" / "op1_runs" / "20260911_Lsg_book_default_none_structure_group.json"
OP1_L0 = ROOT / "notes" / "op1_runs" / "20260911_L0_book_default_exact_structure_group.json"
OP1_LANG = ROOT / "notes" / "op1_runs" / "20260911_Lang_book_default_none_structure_group.json"
HARNESS_DIR = ROOT / "scripts" / "op2_topograph"
I_UNIT = np.array([0.0, 1.0, 0.0, 0.0])
J_UNIT = np.array([0.0, 0.0, 1.0, 0.0])


def _load_op2():
    spec = importlib.util.spec_from_file_location("op2_topograph_run", OP2_PY)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def op2():
    return _load_op2()


def test_refuse_candidate_adjacency():
    with pytest.raises(ValueError, match="candidate_adjacency"):
        build_flux_topograph(HURWITZ_UNITS, adjacency="candidate")


def test_refuse_mixed_edges():
    with pytest.raises(ValueError, match="mix"):
        build_flux_topograph(
            HURWITZ_UNITS,
            edges=[(0, 1)],
            adjacency="structure_group",
        )


def test_harness_does_not_use_legacy_portal_map():
    text = (HARNESS_DIR / "run.py").read_text(encoding="utf-8")
    assert "legacy_portal_map" not in text


def test_hopf_map_pin():
    y = hopf_map(np.array([0.0, 0.0, 1.0, 0.0]))
    np.testing.assert_allclose(y, [0.0, 0.0, -1.0], atol=1e-12)


def test_lsg_fiber_flux_is_kirchhoff(op2):
    op1 = op2._load_op1_run()
    preset = op1.load_preset("book_default")
    points, _meta = op1.build_lsg(preset)
    topo = build_flux_topograph(points, adjacency="structure_group", functional="hopf_height")
    flux = fiber_cycle_flux(points)
    report = kirchhoff_report(
        flux, len(points), support=topo.meta["along"] + topo.meta["inter"]
    )
    assert report["kirchhoff"] is True
    assert report["support_subset_of_skeleton"] is True
    assert report["max_abs_residual"] == 0.0
    assert topo.meta["adjacency"] == "structure_group"


def test_lsg_run_attaches_op1_census(op2, tmp_path):
    pytest.importorskip("yaml")
    if not OP1_LSG.is_file():
        pytest.skip("OP1 Lsg structure_group JSON missing")
    payload = op2.run_one("Lsg", attach=OP1_LSG)
    assert payload["op2_status"] == "Open"
    assert payload["op1_status"] == "Open"
    assert payload["rule"] == "structure_group"
    assert payload["support"]["kirchhoff"]["kirchhoff"] is True
    census = payload["fiber_census"]
    assert census["along_kind"] == "consecutive_u1_on_sampled_fibers"
    assert census.get("along_equals_structure_group_by_construction") is True
    assert "hopf_height" in payload["functionals"]
    assert "hopf_y1" in payload["functionals"]
    eq = payload["functionals"]["hopf_height"]["equivariance"]
    assert "left_i" in eq and "left_j" in eq
    json_path, _md = op2.write_run(payload, tmp_path, stem="op2_lsg")
    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded["n_along"] == payload["n_along"]


def test_attach_rejects_candidate_row(op2, tmp_path):
    fake = {
        "schema": "op1_adjacency_v1",
        "rule": "candidate",
        "set": "Lsg",
        "op1_status": "Open",
    }
    path = tmp_path / "cand.json"
    path.write_text(json.dumps(fake), encoding="utf-8")
    with pytest.raises(SystemExit, match="structure_group"):
        op2.load_op1_row(path)


def test_lsg_hopf_height_golden(op2):
    if not OP1_LSG.is_file():
        pytest.skip("OP1 Lsg JSON missing")
    payload = op2.run_one("Lsg", attach=OP1_LSG)
    gold = json.loads(
        (ROOT / "tests" / "data" / "op2_Lsg_hopf_height.json").read_text(encoding="utf-8")
    )
    s = payload["functionals"]["hopf_height"]["separators"]
    assert s["n_components"] == gold["n_components"]
    assert s["n_separator_edges"] == gold["n_separator_edges"]
    assert payload["support"]["kirchhoff"]["kirchhoff"] is gold["kirchhoff"]


def test_l0_periodicity_is_vacuous_empty_cut(op2):
    if not OP1_L0.is_file():
        pytest.skip("OP1 L0 JSON missing")
    payload = op2.run_one("L0", attach=OP1_L0)
    for fname in ("hopf_height", "hopf_y1"):
        per = payload["functionals"][fname]["periodicity"]
        assert per["left_i"]["status"] == "undefined_or_vacuous"
        assert per["left_j"]["status"] == "undefined_or_vacuous"
        assert per["left_i"]["n_components_after"] is None
        poles = payload["functionals"][fname]["pole_level_sets"]
        assert len(poles) == 6
        vals = sorted(set(round(p["value"], 8) for p in poles))
        assert 0.0 in vals
        assert payload["functionals"][fname]["do_not_count_zero_as_crossing"] is True


def test_lsg_height_periodicity_changes_under_left_j(op2):
    if not OP1_LSG.is_file():
        pytest.skip("OP1 Lsg JSON missing")
    payload = op2.run_one("Lsg", attach=OP1_LSG)
    per = payload["functionals"]["hopf_height"]["periodicity"]
    assert per["left_i"]["status"] == "finite"
    assert per["left_j"]["status"] == "finite"
    assert per["left_i"]["n_components_before"] == 4
    assert per["left_i"]["n_components_after"] == 4
    assert per["left_j"]["n_components_before"] == 4
    assert per["left_j"]["n_components_after"] == 5
    assert per["left_j"]["changed"] is True
    assert per["left_j"]["not_farey_period"] is True


def test_lang_height_is_delaunay_periodicity_not_farey(op2):
    if not OP1_LANG.is_file():
        pytest.skip("OP1 Lang JSON missing")
    payload = op2.run_one("Lang", attach=OP1_LANG)
    per = payload["functionals"]["hopf_height"]["periodicity"]
    assert per["left_i"]["kind"] == "delaunay_periodicity"
    assert per["left_i"]["not_farey_period"] is True
    assert per["left_i"]["status"] == "finite"
    y1 = payload["functionals"]["hopf_y1"]
    assert y1["separators"]["n_components"] == 8
    assert y1["equivariance"]["left_i"]["n_components_after"] == 9
    assert y1["equivariance"]["left_j"]["n_components_after"] == 9
    assert "inter_kept" in y1["op1_inter_kept"]["left_i"]
    assert "inter_kept<1" in y1["op1_inter_kept"]["note"]


def test_book_periodicity_score_without_cut_still_returns_period_found():
    topo = build_flux_topograph(
        HURWITZ_UNITS, adjacency="structure_group", functional="hopf_height"
    )
    sc = periodicity_score(topo, [("L", I_UNIT)], max_periods=4)
    assert "period_found" in sc
    assert "status" not in sc


def test_equivariance_matrix_is_ledger_not_axiom(op2):
    for path in (OP1_LSG, OP1_L0, OP1_LANG):
        if not path.is_file():
            pytest.skip(f"missing {path.name}")
    payload = op2.assemble_equivariance_matrix()
    assert payload["schema"] == "op2_equivariance_matrix_v1"
    assert payload["claim"] == "Software fact"
    assert payload["op1_status"] == "Open"
    assert payload["op2_status"] == "Open"
    assert payload["op3_status"] == "Open"
    assert payload["do_not_call_model_2_gauge_equivariant"] is True
    assert payload["do_not_write_axioms"] is True
    assert payload["averaged"] is False
    lock = payload["claim_lock"]
    assert lock["kind"] == "ledger_increment"
    assert lock["not_an_axiom"] is True
    assert lock["model_2_gauge_equivariant"] is False
    assert lock["op3_entered"] is False
    assert lock["op3_status"] == "Open"
    assert lock["not_invariance"] is True
    assert "zeros are levels" in lock["forbids"]
    assert payload["side"] == "L"
    assert payload["right"].endswith("equivariance_matrix_right.json")
    assert payload["right_averaged"] is False
    assert payload["not_a_new_graph"] is True
    assert payload["not_op3"] is True
    assert payload["rows"] == ["Lsg", "L0", "Lang"]
    assert payload["columns"] == ["left_i", "left_j"]
    assert "candidate" not in json.dumps(payload["sources"])


def test_equivariance_matrix_l0_empty_cut_is_not_keep_rate(op2):
    if not OP1_L0.is_file():
        pytest.skip("OP1 L0 JSON missing")
    payload = op2.assemble_equivariance_matrix()
    for side in ("left_i", "left_j"):
        cell = payload["cells"]["L0"][side]
        assert cell["op1"]["inter_kept"] == 1.0
        assert cell["op1"]["along_kept"] == 1.0
        for fname in ("hopf_height", "hopf_y1"):
            fn = cell[fname]
            assert fn["ledger"] == "undefined_or_vacuous"
            assert fn["periodicity_status"] == "undefined_or_vacuous"
            assert fn["n_components_after"] is None
            assert fn["empty_cut_not_keep_rate_1"] is True


def test_equivariance_matrix_known_moves_not_averaged(op2):
    if not OP1_LSG.is_file() or not OP1_LANG.is_file():
        pytest.skip("OP1 JSON missing")
    payload = op2.assemble_equivariance_matrix()
    lsg_h = payload["cells"]["Lsg"]
    assert lsg_h["left_i"]["hopf_height"]["n_components_before"] == 4
    assert lsg_h["left_i"]["hopf_height"]["n_components_after"] == 4
    assert lsg_h["left_j"]["hopf_height"]["n_components_before"] == 4
    assert lsg_h["left_j"]["hopf_height"]["n_components_after"] == 5
    assert lsg_h["left_j"]["hopf_height"]["ledger"] == "changed"
    assert (
        lsg_h["left_i"]["hopf_height"]["n_components_after"]
        != lsg_h["left_j"]["hopf_height"]["n_components_after"]
    )
    lang_y = payload["cells"]["Lang"]
    assert lang_y["left_i"]["hopf_y1"]["n_components_before"] == 8
    assert lang_y["left_i"]["hopf_y1"]["n_components_after"] == 9
    assert lang_y["left_j"]["hopf_y1"]["n_components_after"] == 9
    assert lang_y["left_i"]["op1"]["inter_kept"] != lang_y["left_j"]["op1"]["inter_kept"]
    assert lang_y["left_i"]["op1"]["inter_kept"] == pytest.approx(0.9444444444444444)
    assert lang_y["left_j"]["op1"]["inter_kept"] == pytest.approx(0.8111111111111111)
    lsg_y = payload["cells"]["Lsg"]["left_i"]["hopf_y1"]
    assert lsg_y["ledger"] == "undefined_or_vacuous"


def test_equivariance_matrix_ledger_file_exists(op2):
    path = ROOT / "notes" / "op2_runs" / "20260913_equivariance_matrix.json"
    if not path.is_file():
        pytest.skip("matrix ledger not written")
    data = json.loads(path.read_text(encoding="utf-8"))
    live = op2.assemble_equivariance_matrix()
    assert data["schema"] == live["schema"]
    assert data["do_not_call_model_2_gauge_equivariant"] is True
    assert data["op3_status"] == "Open"
    assert data["claim_lock"]["op3_entered"] is False
    assert data["claim_lock"]["not_invariance"] is True
    assert data["cells"]["Lsg"]["left_j"]["hopf_height"]["n_components_after"] == 5
    assert data["cells"]["Lang"]["left_i"]["hopf_y1"]["n_components_after"] == 9
    assert data["cells"]["L0"]["left_i"]["hopf_height"]["ledger"] == "undefined_or_vacuous"


def test_equivariance_matrix_writes_ledger(op2, tmp_path):
    if not OP1_LSG.is_file():
        pytest.skip("OP1 JSON missing")
    payload = op2.assemble_equivariance_matrix()
    json_path, md_path = op2.write_matrix(payload, tmp_path, stem="equivariance_matrix")
    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    md = md_path.read_text(encoding="utf-8")
    assert loaded["do_not_call_model_2_gauge_equivariant"] is True
    assert loaded["op3_status"] == "Open"
    assert loaded["claim_lock"]["op3_entered"] is False
    assert loaded["claim_lock"]["not_invariance"] is True
    assert "Claim lock" in md
    assert "ledger increment" in md
    assert "gauge-equivariant" in md
    assert "not averaged" in md.lower() or "Not averaged" in md or "not averaged" in md
    assert "OP3 not entered" in md
    assert "not invariance" in md
    assert "undefined_or_vacuous" in md
    assert "keep-rate 1.0" in md
    notes = (ROOT / "notes" / "open_problems.md").read_text(encoding="utf-8")
    assert "20260913_equivariance_matrix.json" in notes
    assert "Parked (not started) — equivariance matrix" not in notes
    assert "Do not open OP3" in notes or "do not enter" in notes.lower()


def test_right_matrix_is_sibling_not_averaged(op2):
    pytest.importorskip("yaml")
    for path in (OP1_LSG, OP1_L0, OP1_LANG):
        if not path.is_file():
            pytest.skip(f"missing {path.name}")
    left = op2.assemble_equivariance_matrix()
    right = op2.assemble_equivariance_matrix_right()
    assert right["schema"] == "op2_equivariance_matrix_v1"
    assert right["side"] == "R"
    assert right["columns"] == ["right_i", "right_j"]
    assert right["averaged"] is False
    assert right["left_averaged"] is False
    assert right["not_a_new_graph"] is True
    assert right["op3_status"] == "Open"
    assert right["claim_lock"]["op3_entered"] is False
    assert right["do_not_call_model_2_gauge_equivariant"] is True
    assert right["left"].endswith("equivariance_matrix.json")
    # L0 empty cut stays vacuous; OP1 R keep-rate 1 is a different object.
    for side in ("right_i", "right_j"):
        cell = right["cells"]["L0"][side]
        assert cell["op1"]["side"] == "R"
        assert cell["op1"]["inter_kept"] == 1.0
        for fname in ("hopf_height", "hopf_y1"):
            assert cell[fname]["ledger"] == "undefined_or_vacuous"
            assert cell[fname]["empty_cut_not_keep_rate_1"] is True
    # Lang R inter_kept is not the left pair, and i/j are not averaged.
    lang_r = right["cells"]["Lang"]
    lang_l = left["cells"]["Lang"]
    assert lang_r["right_i"]["op1"]["inter_kept"] == pytest.approx(0.8111111111111111)
    assert lang_r["right_j"]["op1"]["inter_kept"] == pytest.approx(0.8333333333333334)
    assert lang_r["right_i"]["op1"]["inter_kept"] != lang_r["right_j"]["op1"]["inter_kept"]
    assert lang_r["right_i"]["op1"]["inter_kept"] != lang_l["left_i"]["op1"]["inter_kept"]
    # Same skeleton, not mixed into one table.
    assert "left_i" not in right["cells"]["Lsg"]
    assert "right_i" not in left["cells"]["Lsg"]
    # Component moves on this dictionary (Software fact, not an identification with left).
    assert right["cells"]["Lsg"]["right_j"]["hopf_height"]["n_components_after"] == 5
    assert right["cells"]["Lang"]["right_i"]["hopf_y1"]["n_components_after"] == 9
    assert right["cells"]["Lang"]["right_j"]["hopf_y1"]["n_separator_edges_after"] == 38
    assert right["cells"]["Lang"]["right_i"]["hopf_y1"]["n_separator_edges_after"] == 37


def test_right_ledger_file_exists(op2):
    path = ROOT / "notes" / "op2_runs" / "20260913_equivariance_matrix_right.json"
    if not path.is_file():
        pytest.skip("right matrix ledger not written")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["side"] == "R"
    assert data["do_not_call_model_2_gauge_equivariant"] is True
    assert data["claim_lock"]["op3_entered"] is False
    assert data["cells"]["L0"]["right_i"]["hopf_height"]["ledger"] == "undefined_or_vacuous"
    assert data["cells"]["Lang"]["right_i"]["op1"]["inter_kept"] == pytest.approx(0.8111111111111111)
    left = json.loads(
        (ROOT / "notes" / "op2_runs" / "20260913_equivariance_matrix.json").read_text(
            encoding="utf-8"
        )
    )
    # Matching j-cut integers do not identify the files.
    assert left["cells"]["Lsg"]["left_j"]["hopf_height"]["n_separator_edges_after"] == 7
    assert data["cells"]["Lsg"]["right_j"]["hopf_height"]["n_separator_edges_after"] == 7
    assert left["cells"]["Lang"]["left_i"]["op1"]["inter_kept"] != data["cells"]["Lang"]["right_i"]["op1"]["inter_kept"]
    lock = data["claim_lock"]["forbids"]
    assert "Do not fold" in lock or "do not identify" in lock
    assert "0.833" in lock or "0.811" in lock


def test_right_matrix_writes_ledger(op2, tmp_path):
    pytest.importorskip("yaml")
    if not OP1_LSG.is_file():
        pytest.skip("OP1 JSON missing")
    payload = op2.assemble_equivariance_matrix_right()
    json_path, md_path = op2.write_matrix(payload, tmp_path, stem="equivariance_matrix_right")
    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    md = md_path.read_text(encoding="utf-8")
    assert loaded["side"] == "R"
    assert loaded["claim_lock"]["not_invariance"] is True
    assert "not averaged" in md.lower()
    assert "OP3 not entered" in md
    assert "right-i" in md
    assert "not invariance" in md


def test_strict_sign_does_not_count_zero_zero():
    pts = HURWITZ_UNITS[:4]
    values = np.zeros(4)
    from lib.flux_topograph import FluxTopograph

    topo = FluxTopograph(points=pts, values=values, edges=[(0, 1)])
    assert detect_separators(topo, mode="strict_sign") == []
    # book default still treats zeros as separators
    assert detect_separators(topo, mode="sign")
