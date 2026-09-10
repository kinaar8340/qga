"""Book HURWITZ_UNITS is a re-export of flux_hopf_lib. Fixtures win."""

from __future__ import annotations

import json
from importlib.resources import files

import numpy as np

from flux_hopf_lib.hopf import hopf_map as lib_hopf_map
from flux_hopf_lib.quaternion.hurwitz import HURWITZ_UNITS as LIB_UNITS
from lib.hopf_lattice import HURWITZ_UNITS, hopf_map


def test_reexport_is_the_lib_24() -> None:
    np.testing.assert_array_equal(HURWITZ_UNITS, LIB_UNITS)
    assert len(HURWITZ_UNITS) == 24


def test_units_match_checked_in_fixture() -> None:
    raw = files("flux_hopf_lib.fixtures").joinpath("hurwitz_units_v1.json").read_text(
        encoding="utf-8"
    )
    want = np.asarray(json.loads(raw)["units"], dtype=float)
    np.testing.assert_array_equal(HURWITZ_UNITS, want)


def test_hopf_on_units_matches_fixture() -> None:
    raw = files("flux_hopf_lib.fixtures").joinpath("hopf_hurwitz_v1.json").read_text(
        encoding="utf-8"
    )
    points = json.loads(raw)["points"]
    for i, row in enumerate(points):
        q = np.asarray(row["q"], dtype=float)
        y_book = hopf_map(q)
        y1, y2, y3 = lib_hopf_map(*q)
        y_lib = np.array([float(y1), float(y2), float(y3)])
        want = np.asarray(row["y"], dtype=float)
        np.testing.assert_allclose(y_book, want, rtol=0, atol=1e-15)
        np.testing.assert_allclose(y_lib, want, rtol=0, atol=1e-15)
        np.testing.assert_array_equal(q, HURWITZ_UNITS[i])
