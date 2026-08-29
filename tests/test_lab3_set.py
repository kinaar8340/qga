"""Lab 3 must compare rounded row-tuples, not np.sort(..., axis=0)."""

import numpy as np

from lib.hopf_lattice import rounded_point_set


def test_rounded_point_set_is_row_set_not_column_sort():
    a = np.array([[1.0, 2.0], [3.0, 0.0]])
    b = np.array([[3.0, 0.0], [1.0, 2.0]])
    # Same set of rows.
    assert rounded_point_set(a, 6) == rounded_point_set(b, 6)
    # np.sort(..., 0) would also pass here; this pair distinguishes:
    c = np.array([[1.0, 0.0], [3.0, 2.0]])
    assert np.array_equal(np.sort(a, 0), np.sort(c, 0))  # column sort confuses a with c
    assert rounded_point_set(a, 6) != rounded_point_set(c, 6)
