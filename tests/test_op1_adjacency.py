"""OP1 harness invariants. Not beauty: do not assert Lang looks like a Hopf fiber."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

from flux_hopf_lib.quaternion.hurwitz import HURWITZ_UNITS as LIB_UNITS
from lib.hopf_lattice import (
    HURWITZ_UNITS,
    OCTAHEDRON_POLES_S2,
    bases_are_octahedron_poles,
    hopf_map,
    hopf_project_points,
    sample_structure_group_fiber,
    stereographic,
    structure_group_adjacency,
)

ROOT = Path(__file__).resolve().parents[1]
RUN_PY = ROOT / "scripts" / "op1_adjacency" / "run.py"
GOLDEN = ROOT / "tests" / "data" / "op1_L0_left_i_book_default.json"
HARNESS_DIR = ROOT / "scripts" / "op1_adjacency"

SCHEMA_E1 = (
    "along_base_near_0",
    "along_on_true_fiber",
    "along_chart_only",
    "inter_leaks_into_along",
    "n_along",
    "n_inter",
)
SCHEMA_E2 = (
    "along_kept",
    "inter_kept",
    "along_to_inter",
    "lost",
    "n_along",
    "n_inter",
)


def _load_run():
    spec = importlib.util.spec_from_file_location("op1_adjacency_run", RUN_PY)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def op1():
    return _load_run()


def test_structure_group_fiber_base_scatter_lt_1e_8():
    rng = np.random.default_rng(11)
    q = rng.normal(size=4)
    q = q / np.linalg.norm(q)
    fib = sample_structure_group_fiber(q, n_points=32)
    base = np.stack([fib["y1"], fib["y2"], fib["y3"]], axis=1)
    scatter = float(np.max(np.linalg.norm(base - base[0], axis=1)))
    assert scatter < 1e-8


def test_legacy_portal_map_not_used_by_harness():
    for path in HARNESS_DIR.glob("*"):
        if path.suffix not in {".py", ".yaml", ".md"}:
            continue
        text = path.read_text(encoding="utf-8")
        assert "legacy_portal_map" not in text, path


def test_hurwitz_units_are_the_lib_24():
    assert len(HURWITZ_UNITS) == 24
    np.testing.assert_array_equal(HURWITZ_UNITS, LIB_UNITS)


def test_hopf_map_0010_is_south_pole():
    y = hopf_map(np.array([0.0, 0.0, 1.0, 0.0]))
    np.testing.assert_allclose(y, [0.0, 0.0, -1.0], atol=1e-12)


def test_lsg_seeds_have_distinct_hopf_images(op1):
    preset = op1.load_preset("book_default")
    bases = []
    for seed in preset["lsg_seeds"]:
        y = hopf_map(np.asarray(seed, dtype=float))
        bases.append(np.round(y, 8))
    uniq = {tuple(b.tolist()) for b in bases}
    assert len(uniq) == len(bases)


def test_json_schema_l0_left_i(op1, tmp_path):
    preset = op1.load_preset("book_default")
    payload = op1.run_one(
        "L0",
        preset,
        resnap="exact",
        dump_edges=False,
        sides=("L",),
        units=[op1.I_UNIT],
    )
    for key in SCHEMA_E1:
        assert key in payload["experiment1"], key
    assert payload["schema"] == "op1_adjacency_v1"
    assert payload["op1_status"] == "Open"
    assert payload["claim"] == "Software fact"
    assert payload["hopf_map_0010"] == [0.0, 0.0, -1.0]
    assert len(payload["experiment2"]) == 1
    row = payload["experiment2"][0]
    for key in SCHEMA_E2:
        assert key in row, key
    assert row["unit_name"] == "i"
    assert row["side"] == "L"
    assert row["resnap"] == "exact"
    assert "lib_score" in row
    assert "along_preserved" in row["lib_score"]
    json_path, _md = op1.write_run(payload, tmp_path, stem="schema_check")
    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded["experiment2"][0]["n_along"] == row["n_along"]


def test_empty_along_is_null_not_perfect_keep(op1):
    """If L0 has zero along-edges, harness must not report 100% kept."""
    preset = op1.load_preset("book_default")
    payload = op1.run_one(
        "L0",
        preset,
        resnap="exact",
        dump_edges=False,
        sides=("L",),
        units=[op1.I_UNIT],
    )
    e1 = payload["experiment1"]
    row = payload["experiment2"][0]
    if e1["n_along"] == 0:
        assert e1["along_on_true_fiber"] is None
        assert row["along_kept"] is None
        assert row["lib_score"]["along_preserved"] == 1.0
    else:
        assert row["along_kept"] is not None
        assert 0.0 <= row["along_kept"] <= 1.0


def test_exact_refused_on_lang(op1):
    preset = op1.load_preset("book_default")
    with pytest.raises(SystemExit, match="exact"):
        op1.run_one("Lang", preset, resnap="exact", dump_edges=False)


def test_i_is_first_unit(op1):
    names = [op1.unit_name(u) for u in op1.iter_hurwitz_units_i_first()]
    assert names[0] == "i"
    assert len(names) == 24
    assert names.count("i") == 1


def test_constructed_lsg_is_on_true_fiber(op1):
    preset = op1.load_preset("book_default")
    points, meta = op1.build_lsg(preset)
    e1 = op1.experiment1(
        points,
        set_name="Lsg",
        preset=preset,
        constructed_along=meta["constructed_along"],
    )
    cons = e1["constructed_consecutive"]
    assert cons["n_along"] == 4 * 16
    assert cons["along_on_true_fiber"] == pytest.approx(1.0)
    assert cons["along_base_near_0"] == pytest.approx(1.0)


def test_golden_l0_left_i(op1):
    preset = op1.load_preset("book_default")
    payload = op1.run_one(
        "L0",
        preset,
        resnap="exact",
        dump_edges=False,
        sides=("L",),
        units=[op1.I_UNIT],
    )
    assert GOLDEN.is_file(), f"missing golden {GOLDEN}"
    want = json.loads(GOLDEN.read_text(encoding="utf-8"))
    got_e1 = payload["experiment1"]
    want_e1 = want["experiment1"]
    assert got_e1["n_along"] == want_e1["n_along"]
    assert got_e1["n_inter"] == want_e1["n_inter"]
    for key in (
        "along_base_near_0",
        "along_on_true_fiber",
        "along_chart_only",
        "inter_leaks_into_along",
    ):
        a, b = got_e1[key], want_e1[key]
        if a is None or b is None:
            assert a is b
        else:
            assert a == pytest.approx(b, abs=1e-12)
    got_row = payload["experiment2"][0]
    want_row = want["experiment2"][0]
    assert got_row["unit_name"] == want_row["unit_name"] == "i"
    assert got_row["side"] == want_row["side"] == "L"
    for key in SCHEMA_E2:
        a, b = got_row[key], want_row[key]
        if a is None or b is None:
            assert a is b, key
        else:
            assert a == pytest.approx(b, abs=1e-12), key


def test_sg_distance_zero_on_common_phase(op1):
    from lib.hopf_lattice import common_phase

    q = np.array([1.0, 0.0, 0.0, 0.0])
    qj = common_phase(q, 0.7)
    d = op1.distance_to_structure_group_fiber(q, qj)
    assert d < 1e-12


def test_hopf_project_points_constant_on_lsg_block(op1):
    preset = op1.load_preset("book_default")
    q = np.asarray(preset["lsg_seeds"][0], dtype=float)
    fib = sample_structure_group_fiber(q, n_points=16)
    base = hopf_project_points(fib["points"])
    scatter = float(np.max(np.linalg.norm(base - base[0], axis=1)))
    assert scatter < 1e-8


def test_each_lsg_fiber_hopf_scatter_lt_1e_8(op1):
    """Protects the flux-hopf-lib >= 0.3.1 classical map pin."""
    preset = op1.load_preset("book_default")
    _pts, meta = op1.build_lsg(preset)
    scatters = meta["fiber_base_scatter"]
    assert len(scatters) == len(preset["lsg_seeds"])
    for i, s in enumerate(scatters):
        assert s < 1e-8, f"fiber {i} hopf_map scatter {s}"
    assert meta["fiber_base_scatter_max"] < 1e-8


def test_lsg_denominators_are_not_collapsed(op1):
    preset = op1.load_preset("book_default")
    points, meta = op1.build_lsg(preset)
    e1 = op1.experiment1(
        points,
        set_name="Lsg",
        preset=preset,
        constructed_along=meta["constructed_along"],
    )
    cons = e1["constructed_consecutive"]
    assert e1["n_along"] != cons["n_along"] or e1["n_along"] == 0
    assert "candidate" in e1["along_on_true_fiber_denominator"] or "E_parallel" in e1["along_on_true_fiber_denominator"]
    assert "consecutive samples" in cons["along_on_true_fiber_denominator"]
    assert "not candidate" in cons["along_on_true_fiber_denominator"] or "not " in cons["along_on_true_fiber_denominator"]
    assert e1["do_not_collapse_candidate_n_along_with_constructed_n_along"] is True
    assert e1["along_on_true_fiber_how"]
    assert cons["along_on_true_fiber_how"]


def test_l0_inter_base_distances_are_logged(op1):
    preset = op1.load_preset("book_default")
    payload = op1.run_one(
        "L0",
        preset,
        resnap="exact",
        dump_edges=False,
        sides=("L",),
        units=[op1.I_UNIT],
    )
    e1 = payload["experiment1"]
    ibd = e1["inter_base_distances"]
    assert ibd["n"] == e1["n_inter"] == 36
    assert ibd["values"] is not None
    assert len(ibd["values"]) == 36
    assert ibd["n_exact_zero"] == 36
    assert ibd["leak_is_exact"] is True
    assert ibd["max"] <= 1e-15


def test_structure_group_adjacency_is_sibling_not_a_patch():
    import inspect
    from lib.hopf_lattice import candidate_adjacency

    src = inspect.getsource(candidate_adjacency)
    assert "xi2" in src
    assert "base_angle_thresh" in src
    assert src.count("def candidate_adjacency") == 1


def test_lang_structure_group_is_8_by_32_product_not_farey(op1):
    preset = op1.load_preset("book_default")
    points, _meta = op1.build_lang(preset)
    e1 = op1.experiment1(
        points,
        set_name="Lang",
        preset=preset,
        adj_fn=structure_group_adjacency,
        kwargs=op1.sg_kwargs(preset),
        rule="structure_group",
    )
    c = e1["fiber_census"]
    assert c["n_distinct_bases"] == 32
    assert c["multiplicity_histogram"] == {"8": 32}
    assert c["along_kind"] == "consecutive_u1_steps_on_product_sample"
    assert c["along_equals_consecutive_u1"] is True
    assert c["not_a_farey_diagram"] is True
    assert e1["n_along"] == 256
    assert "8 phases" in c["note"]
    assert c["image"]["claim"] == "Software fact"
    assert "occupancy necklace" in c["image"]["note"]


def test_lang_candidate_along_is_not_consecutive_u1(op1):
    preset = op1.load_preset("book_default")
    points, _meta = op1.build_lang(preset)
    e1 = op1.experiment1(points, set_name="Lang", preset=preset, rule="candidate")
    c = e1["fiber_census"]
    assert c["n_distinct_bases"] == 32
    assert c["multiplicity_histogram"] == {"8": 32}
    assert c["along_kind"] == "chart_xi2_circle_not_u1"
    assert c["along_equals_consecutive_u1"] is False


def test_l0_candidate_has_no_along_edges_not_a_farey_graph(op1):
    preset = op1.load_preset("book_default")
    points, _meta = op1.build_l0(preset)
    e1 = op1.experiment1(points, set_name="L0", preset=preset, rule="candidate")
    c = e1["fiber_census"]
    assert e1["n_along"] == 0
    assert c["n_distinct_bases"] == 6
    assert c["multiplicity_histogram"] == {"4": 6}
    assert c["along_kind"] == "no_along_edges"
    assert c["image"]["claim"] == "Theorem"
    assert c["image"]["object"] == "octahedron_poles"


def test_hurwitz_hopf_image_is_octahedron_poles():
    """Theorem: h(Λ0) is the 6 octahedron poles, 4 per fiber. Check realizes it."""
    base = hopf_project_points(HURWITZ_UNITS)
    assert bases_are_octahedron_poles(base)
    assert len(OCTAHEDRON_POLES_S2) == 6
    rounded = np.round(base, 8)
    _, counts = np.unique(rounded, axis=0, return_counts=True)
    assert sorted(counts.tolist()) == [4, 4, 4, 4, 4, 4]


def test_l0_structure_group_along_is_u1_occupancy_not_farey(op1):
    preset = op1.load_preset("book_default")
    points, _meta = op1.build_l0(preset)
    e1 = op1.experiment1(
        points,
        set_name="L0",
        preset=preset,
        adj_fn=structure_group_adjacency,
        kwargs=op1.sg_kwargs(preset),
        rule="structure_group",
    )
    c = e1["fiber_census"]
    assert e1["n_along"] == 24
    assert c["along_kind"] == "u1_occupancy_through_lambda0"
    assert e1["l0_along_are_u1_occupancy_not_farey_neighbors"] is True
    assert "Farey" in c["note"]
    assert c["along_equals_consecutive_u1"] is True
    assert c["not_a_farey_diagram"] is True
    assert c["image"]["claim"] == "Theorem"
    assert c["image"]["object"] == "octahedron_poles"
    assert c["image"]["realized_by_this_sample"] is True
    assert c["along_edges_claim"] == "Software fact"
    assert "Unstarted" in c["parked_farey_slice_A"]


def test_structure_group_lsg_covers_constructed_64(op1):
    preset = op1.load_preset("book_default")
    points, meta = op1.build_lsg(preset)
    constructed = set(tuple(sorted(e)) for e in meta["constructed_along"])
    along, inter = structure_group_adjacency(points)
    along_set = set(tuple(sorted(e)) for e in along)
    assert constructed <= along_set
    assert len(along) >= 64
    e1 = op1.experiment1(
        points,
        set_name="Lsg",
        preset=preset,
        constructed_along=meta["constructed_along"],
        adj_fn=structure_group_adjacency,
        kwargs=op1.sg_kwargs(preset),
        rule="structure_group",
        sample_meta=meta,
    )
    assert e1["along_on_true_fiber"] == pytest.approx(1.0)
    assert e1["n_along"] >= 64
    if e1["n_inter"]:
        assert e1["inter_leaks_into_along"] == pytest.approx(0.0)
    c = e1["fiber_census"]
    assert c["along_kind"] == "consecutive_u1_on_sampled_fibers"
    assert c["along_equals_structure_group_by_construction"] is True
    assert c["image"]["claim"] == "Software fact"


def _along_cycle_lengths(n_points: int, along: list[list[int]]) -> list[int]:
    adj: dict[int, list[int]] = {i: [] for i in range(n_points)}
    for a, b in along:
        adj[a].append(b)
        adj[b].append(a)
    occupied = [i for i in range(n_points) if adj[i]]
    for i in occupied:
        assert len(adj[i]) == 2, f"vertex {i} degree {len(adj[i])} (want 2 for a cycle)"
    seen: set[int] = set()
    lengths: list[int] = []
    for start in occupied:
        if start in seen:
            continue
        cur = start
        prev = None
        length = 0
        while cur not in seen:
            seen.add(cur)
            length += 1
            nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
            prev, cur = cur, nxt
        assert cur == start, "along component is a path, not a closed cycle"
        lengths.append(length)
    return sorted(lengths)


def _write_graph(op1, tmp_path, set_name: str, *, resnap: str):
    preset = op1.load_preset("book_default")
    payload = op1.run_one(
        set_name,
        preset,
        resnap=resnap,
        dump_edges=False,
        dump_graph=True,
        sides=("L",),
        units=[op1.I_UNIT],
        rule="structure_group",
    )
    stem = f"graph_{set_name}"
    json_path, _md = op1.write_run(payload, tmp_path, stem=stem)
    graph_path = tmp_path / f"{stem}_graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    row = json.loads(json_path.read_text(encoding="utf-8"))
    return graph, row, graph_path


def test_dump_graph_refuses_candidate(op1):
    preset = op1.load_preset("book_default")
    with pytest.raises(SystemExit, match="dump-graph"):
        op1.run_one(
            "Lsg",
            preset,
            resnap="none",
            dump_edges=False,
            dump_graph=True,
            rule="candidate",
        )


def test_dump_graph_cli_refuses_candidate(op1):
    with pytest.raises(SystemExit, match="dump-graph"):
        op1.main(["--set", "Lsg", "--rule", "candidate", "--dump-graph"])


def test_dump_graph_lsg_schema_and_closed_cycles(op1, tmp_path):
    graph, row, _path = _write_graph(op1, tmp_path, "Lsg", resnap="none")
    e1 = row["experiment1"]
    census = e1["fiber_census"]
    assert graph["kind"] == op1.GRAPH_KIND == "qga_adjacency_graph_v1"
    assert "fibers" not in graph
    assert "version" not in graph
    assert graph["rule"] == "structure_group"
    assert graph["set"] == "Lsg"
    assert graph["projection"] == "stereographic"
    assert graph["map"] == "hopf_map_classical"
    assert graph["op1_row"] == "graph_Lsg.json"
    assert len(graph["points"]) == e1["n_points"] == 64
    assert len(graph["along"]) == e1["n_along"]
    assert len(graph["inter"]) == e1["n_inter"]
    assert graph["census"]["distinct_bases"] == census["n_distinct_bases"] == 4
    assert graph["census"]["along_kind"] == census["along_kind"] == (
        "consecutive_u1_on_sampled_fibers"
    )
    assert graph["census"]["multiplicity"] == 16
    assert _along_cycle_lengths(len(graph["points"]), graph["along"]) == [16, 16, 16, 16]
    seed = np.asarray(op1.load_preset("book_default")["lsg_seeds"][0], dtype=float)
    fib = sample_structure_group_fiber(seed, n_points=16)
    for i in range(16):
        np.testing.assert_allclose(graph["points"][i]["q"], fib["points"][i], atol=1e-12)
        np.testing.assert_allclose(graph["points"][i]["xyz"], fib["curve_xyz"][i], atol=1e-12)
        np.testing.assert_allclose(
            graph["points"][i]["base"],
            [fib["y1"][i], fib["y2"][i], fib["y3"][i]],
            atol=1e-12,
        )


def test_dump_graph_l0_schema_octahedron(op1, tmp_path):
    graph, row, _path = _write_graph(op1, tmp_path, "L0", resnap="exact")
    e1 = row["experiment1"]
    census = e1["fiber_census"]
    assert graph["kind"] == "qga_adjacency_graph_v1"
    assert "fibers" not in graph
    assert graph["set"] == "L0"
    assert graph["rule"] == "structure_group"
    assert len(graph["points"]) == e1["n_points"] == 24
    assert len(graph["along"]) == e1["n_along"] == 24
    assert len(graph["inter"]) == e1["n_inter"] == 12
    assert graph["census"]["distinct_bases"] == 6
    assert graph["census"]["multiplicity"] == 4
    assert graph["census"]["along_kind"] == "u1_occupancy_through_lambda0"
    assert graph["census"]["along_kind"] == census["along_kind"]
    bases = np.array([p["base"] for p in graph["points"]], dtype=float)
    assert bases_are_octahedron_poles(bases)
    assert _along_cycle_lengths(len(graph["points"]), graph["along"]) == [4, 4, 4, 4, 4, 4]
    for p in graph["points"]:
        y = hopf_map(np.asarray(p["q"], dtype=float))
        np.testing.assert_allclose(p["base"], y, atol=1e-12)
        xyz = stereographic(np.asarray(p["q"], dtype=float))
        np.testing.assert_allclose(p["xyz"], xyz, atol=1e-12)


LEDGER_GRAPHS = {
    "Lsg": ROOT
    / "notes"
    / "op1_runs"
    / "20260911_Lsg_book_default_none_structure_group_graph.json",
    "L0": ROOT
    / "notes"
    / "op1_runs"
    / "20260911_L0_book_default_exact_structure_group_graph.json",
}


@pytest.mark.parametrize("set_name", ["Lsg", "L0"])
def test_ledger_graph_kind_is_not_hopf_fibers(set_name):
    """Explorer branch: qga_adjacency_graph_v1, never export_fiber_curves fibers[]."""
    graph = json.loads(LEDGER_GRAPHS[set_name].read_text(encoding="utf-8"))
    assert graph["kind"] == "qga_adjacency_graph_v1"
    assert "fibers" not in graph


@pytest.mark.parametrize(
    "set_name,resnap,n_points,n_along,n_inter,n_bases,along_kind,cycles",
    [
        (
            "Lsg",
            "none",
            64,
            64,
            6,
            4,
            "consecutive_u1_on_sampled_fibers",
            [16, 16, 16, 16],
        ),
        (
            "L0",
            "exact",
            24,
            24,
            12,
            6,
            "u1_occupancy_through_lambda0",
            [4, 4, 4, 4, 4, 4],
        ),
    ],
)
def test_ledger_graph_matches_op1_row(
    op1, tmp_path, set_name, resnap, n_points, n_along, n_inter, n_bases, along_kind, cycles
):
    path = LEDGER_GRAPHS[set_name]
    assert path.is_file(), f"missing ledger graph {path}"
    graph = json.loads(path.read_text(encoding="utf-8"))
    row_path = ROOT / graph["op1_row"]
    row = json.loads(row_path.read_text(encoding="utf-8"))
    e1 = row["experiment1"]
    live, _, _ = _write_graph(op1, tmp_path, set_name, resnap=resnap)
    assert graph["kind"] == "qga_adjacency_graph_v1"
    assert "fibers" not in graph
    assert graph["rule"] == "structure_group"
    assert graph["set"] == set_name
    assert len(graph["points"]) == e1["n_points"] == n_points == len(live["points"])
    assert len(graph["along"]) == e1["n_along"] == n_along
    assert len(graph["inter"]) == e1["n_inter"] == n_inter
    assert graph["census"]["distinct_bases"] == n_bases
    assert graph["census"]["along_kind"] == along_kind
    assert {tuple(sorted(e)) for e in graph["along"]} == {
        tuple(sorted(e)) for e in live["along"]
    }
    assert {tuple(sorted(e)) for e in graph["inter"]} == {
        tuple(sorted(e)) for e in live["inter"]
    }
    assert _along_cycle_lengths(len(graph["points"]), graph["along"]) == cycles
