"""Classifier tree matches Conway–Hatcher: elliptic = no river."""

from __future__ import annotations

import numpy as np

from lib.flux_topograph import FluxTopograph, classify_topograph_type
from lib.hopf_lattice import HURWITZ_UNITS


def test_no_river_is_elliptic_not_parabolic():
    values = 2.0 + 0.4 * np.linspace(-1.0, 1.0, len(HURWITZ_UNITS))
    assert float(np.min(values)) > 0.0
    topo = FluxTopograph(points=HURWITZ_UNITS, values=values, edges=[])
    clf = classify_topograph_type(topo, gauge_sequences=[])
    assert clf["type"] == "elliptic"
    assert clf["n_separator_edges"] == 0
    assert clf["heuristic"] is True


def test_near_constant_is_0_hyperbolic():
    values = np.full(len(HURWITZ_UNITS), 1.0)
    topo = FluxTopograph(points=HURWITZ_UNITS, values=values, edges=[])
    clf = classify_topograph_type(topo, gauge_sequences=[])
    assert clf["type"] == "0-hyperbolic"


def test_few_separators_is_not_the_elliptic_rule():
    """A sign-changing river without detected period is not labeled elliptic."""
    n = len(HURWITZ_UNITS)
    values = np.linspace(-2.0, 2.0, n)
    edges = [(i, i + 1) for i in range(n - 1)]
    topo = FluxTopograph(points=HURWITZ_UNITS, values=values, edges=edges)
    clf = classify_topograph_type(topo, gauge_sequences=[])
    assert clf["n_separator_edges"] > 0
    assert clf["type"] != "elliptic"
