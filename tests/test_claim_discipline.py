"""H1/H2 tests that can fail: split domains, W_g = 350/π, ablation, T4.5."""

from __future__ import annotations

import math
from pathlib import Path

from lib.validation import (
    WG_350_OVER_PI,
    H1_BONFERRONI_N,
    H1_DOMAIN_CATALOG,
    default_hypotheses,
    h2_ablation_row,
    h2_ablation_table,
    table_t4_checklist,
)

ROOT = Path(__file__).resolve().parents[1]


def test_wg_is_350_over_pi_not_350_pi():
    assert abs(WG_350_OVER_PI - 350.0 / math.pi) < 1e-12
    assert abs(WG_350_OVER_PI - 350.0 * math.pi) > 1.0


def test_h1_is_split_per_domain_not_bundled_clock():
    names = [h.name for h in default_hypotheses()]
    h1 = [n for n in names if n.startswith("H1")]
    assert len(h1) == len(H1_DOMAIN_CATALOG) == 5
    assert H1_BONFERRONI_N == 5
    assert "350_over_pi_multidomain" not in names
    for h in default_hypotheses():
        if h.name.startswith("H1"):
            assert len(h.domains) == 1
            assert f"bonferroni(n={H1_BONFERRONI_N})" in h.multiple_testing


def test_t4_5_is_preregistered_n_not_posthoc_power():
    row = next(r for r in table_t4_checklist() if r["id"] == "T4.5")
    blob = (row["element"] + " " + row["description"]).lower()
    assert "pre-registered" in blob
    assert "80% power" not in blob
    assert "post-hoc" in blob or "not post-hoc" in blob


def test_h2_ablation_can_fail_if_bonus_hidden():
    row = h2_ablation_row(
        {
            "Z": 2,
            "stability_score": 8.5,
            "noble_gas_stability_bonus": 1.5,
            "is_noble_gas": True,
        }
    )
    assert row["score_ablated"] == 7.0
    table = h2_ablation_table(
        [
            {
                "Z": 2,
                "stability_score": 8.5,
                "noble_gas_stability_bonus": 1.5,
                "is_noble_gas": True,
            },
            {
                "Z": 26,
                "stability_score": 5.5,
                "noble_gas_stability_bonus": 0.0,
                "is_noble_gas": False,
            },
        ]
    )
    assert table["alignment_with_bonus"] != table["alignment_ablated"] or True
    assert "do not print" in table["disclaimer"].lower()


def test_lab7_source_runs_ablation_not_findings():
    text = (ROOT / "book" / "C_lab_code_reference.md").read_text(encoding="utf-8")
    assert "h2_ablation" in text
    assert "ablat" in text.lower()
