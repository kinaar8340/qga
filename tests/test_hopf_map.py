"""Tests for the book's Hopf map — these must be able to fail.

The broken 3-component formula (legacy_portal_map) already lands on S^2
after output-normalization, so a '||y||=1 after normalize' check is not
enough. Fiber constancy and h(0,0,1,0) are the guards.
"""

from __future__ import annotations

import numpy as np
import pytest

from lib.hopf_lattice import (
    common_phase,
    hopf_map,
    hopf_map_classical,
    hopf_project_points,
    legacy_portal_map,
    sample_structure_group_fiber,
)


def _unit(rng=None):
    rng = np.random.default_rng(0 if rng is None else rng)
    q = rng.normal(size=4)
    return q / np.linalg.norm(q)


def test_hopf_map_classical_is_the_same_function():
    q = _unit(1)
    np.testing.assert_allclose(hopf_map(q), hopf_map_classical(q))


def test_unit_input_lands_on_s2_without_output_normalize():
    """On unit 4-vectors the formula already has ||y||=1; no ||y|| kludge."""
    rng = np.random.default_rng(2)
    for _ in range(40):
        q = rng.normal(size=4)
        q = q / np.linalg.norm(q)
        y = hopf_map(q)
        # Reconstruct the raw bilinear image and compare — hopf_map must
        # not have divided by ||y|| to force unit length.
        x1, x2, x3, x4 = q
        raw = np.array(
            [
                2.0 * (x1 * x3 + x2 * x4),
                2.0 * (x1 * x4 - x2 * x3),
                x1**2 + x2**2 - x3**2 - x4**2,
            ]
        )
        np.testing.assert_allclose(y, raw, atol=1e-12)
        np.testing.assert_allclose(np.linalg.norm(y), 1.0, atol=1e-12)


def test_fiber_constancy_under_common_phase():
    q = _unit(3)
    y0 = hopf_map(q)
    for phi in np.linspace(0.0, 2.0 * np.pi, 16, endpoint=False):
        y = hopf_map(common_phase(q, float(phi)))
        np.testing.assert_allclose(y, y0, atol=1e-10)


def test_h_0010_is_defined_not_a_singularity():
    q = np.array([0.0, 0.0, 1.0, 0.0])
    y = hopf_map(q)
    assert np.all(np.isfinite(y))
    np.testing.assert_allclose(y, np.array([0.0, 0.0, -1.0]), atol=1e-12)
    np.testing.assert_allclose(np.linalg.norm(y), 1.0, atol=1e-12)


def test_agrees_with_complex_form_conj_z1_z2():
    q = _unit(4)
    x1, x2, x3, x4 = q
    z1 = complex(x1, x2)
    z2 = complex(x3, x4)
    cross = 2.0 * (z1.conjugate() * z2)
    expected = np.array(
        [cross.real, cross.imag, abs(z1) ** 2 - abs(z2) ** 2],
        dtype=float,
    )
    np.testing.assert_allclose(hopf_map(q), expected, atol=1e-12)


def test_origin_rejected():
    with pytest.raises(ValueError, match="origin"):
        hopf_map(np.zeros(4))


def test_non_unit_guard_scales_by_norm_squared_not_output_norm():
    q = np.array([2.0, 0.0, 0.0, 0.0])  # ||q||^2 = 4
    y = hopf_map(q)
    # Homogeneous of degree 2: hopf(λq) = λ² hopf(q_hat); guard divides by ||q||².
    np.testing.assert_allclose(y, hopf_map(q / 2.0), atol=1e-12)
    np.testing.assert_allclose(np.linalg.norm(y), 1.0, atol=1e-12)


def test_legacy_portal_map_fails_fiber_constancy():
    """The old formula is not Hopf: this test documents that it can fail."""
    q = np.array([0.0, 0.0, 1.0, 0.0])
    y0 = legacy_portal_map(q)
    drifted = False
    for phi in (0.3, 1.1, 2.2):
        y = legacy_portal_map(common_phase(q, phi))
        if np.linalg.norm(y - y0) > 1e-6:
            drifted = True
            break
    assert drifted, "legacy_portal_map unexpectedly constant on a Hopf fiber"


def test_legacy_portal_map_vanishes_at_0010_before_kludge():
    """Raw 3-component formula is the zero vector at (0,0,1,0)."""
    x1, x2, x3, x4 = 0.0, 0.0, 1.0, 0.0
    raw = np.array(
        [x1**2 - x2**2, 2.0 * x1 * x2, 2.0 * (x3 * x4 + x1 * x2)],
        dtype=float,
    )
    assert np.linalg.norm(raw) < 1e-14


def test_structure_group_fiber_base_is_constant():
    q = _unit(5)
    fib = sample_structure_group_fiber(q, n_points=24)
    base = np.stack([fib["y1"], fib["y2"], fib["y3"]], axis=1)
    np.testing.assert_allclose(base, np.broadcast_to(base[0], base.shape), atol=1e-10)


def test_hopf_project_points_rejects_kc_convention():
    pts = np.stack([_unit(6), _unit(7)], axis=0)
    with pytest.raises(ValueError, match="legacy_portal_map"):
        hopf_project_points(pts, convention="kc")
