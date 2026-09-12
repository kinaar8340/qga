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


def test_strict_sign_does_not_count_zero_zero():
    pts = HURWITZ_UNITS[:4]
    values = np.zeros(4)
    from lib.flux_topograph import FluxTopograph

    topo = FluxTopograph(points=pts, values=values, edges=[(0, 1)])
    assert detect_separators(topo, mode="strict_sign") == []
    # book default still treats zeros as separators
    assert detect_separators(topo, mode="sign")
