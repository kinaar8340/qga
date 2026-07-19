"""Validation protocols (Table T4) for Kingdom Come / QGA Chapter 10.

Pedagogical helpers for pre-registered hypothesis testing. These do **not**
claim that any hypothesis has been confirmed; they structure tests and
diagnostics.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import numpy as np

# Named constant from Kingdom Come model
WG_350_OVER_PI = 350.0 / math.pi  # ≈ 111.408


@dataclass
class HypothesisSpec:
    """A pre-registered hypothesis for Table T4."""

    name: str
    claim: str
    claim_type: str = "Hypothesis"  # Model | Hypothesis
    null_hypothesis: str = ""
    alpha: float = 0.01
    domains: list[str] = field(default_factory=list)
    data_sources: list[str] = field(default_factory=list)
    test_statistic: str = "combined_p_value"
    multiple_testing: str = "bonferroni"
    falsification: str = ""
    notes: str = ""


def table_t4_checklist() -> list[dict[str, str]]:
    """Return the eight core elements of the Table T4 validation protocol."""
    return [
        {
            "id": "T4.1",
            "element": "Null hypothesis definition",
            "description": "State H0 with significance level α (default 0.01).",
        },
        {
            "id": "T4.2",
            "element": "Data sources and preprocessing",
            "description": "List datasets, windows, and cleaning rules.",
        },
        {
            "id": "T4.3",
            "element": "Test statistic",
            "description": "Define the scalar or vector statistic used for decision.",
        },
        {
            "id": "T4.4",
            "element": "Multiple-testing correction",
            "description": "Bonferroni or FDR control across domains/tests.",
        },
        {
            "id": "T4.5",
            "element": "Power analysis",
            "description": "Minimum detectable effect at 80% power.",
        },
        {
            "id": "T4.6",
            "element": "Falsification criteria",
            "description": "What result counts as strong evidence against H1.",
        },
        {
            "id": "T4.7",
            "element": "Pre-registration",
            "description": "Timestamped commit or external registry before new data.",
        },
        {
            "id": "T4.8",
            "element": "Reproducibility",
            "description": "Full code, seeds, and environment for every figure/table.",
        },
    ]


def default_hypotheses() -> list[HypothesisSpec]:
    """Catalog of major book hypotheses for validation planning."""
    return [
        HypothesisSpec(
            name="350_over_pi_multidomain",
            claim="W_g = 350/π is a shared topological clock across named domains.",
            claim_type="Hypothesis",
            null_hypothesis=(
                "Recurrence of values near 350/π across domains is consistent "
                "with random numerical coincidence at α=0.01."
            ),
            alpha=0.01,
            domains=[
                "pulsar_timing",
                "bitcoin_pi_cycle",
                "tls_trees",
                "cuprate_superconductors",
                "structural_constants",
            ],
            data_sources=[
                "kingdom/observations/pulsars_investigation.md",
                "kingdom/app/assets/bitcoin_pi/",
                "kingdom observations tabs",
            ],
            test_statistic="combined_p_value_or_topological_distance",
            multiple_testing="bonferroni",
            falsification=(
                "Combined test fails to reject H0 after pre-registration and "
                "multiple-testing correction; or independent replication finds "
                "no excess clustering near 350/π."
            ),
        ),
        HypothesisSpec(
            name="z_map_periodic_table_proxy",
            claim=(
                "map_z_to_flywheel stability peaks reflect genuine chemical/nuclear "
                "specialness beyond model tuning."
            ),
            claim_type="Hypothesis",
            null_hypothesis=(
                "High stability_score near noble gases is explained by explicit "
                "model bonuses / detuning map alone (no extra predictive content)."
            ),
            alpha=0.01,
            domains=["periodic_table", "ionization_energy", "nuclear_magic"],
            data_sources=[
                "kingdom.core.flux_flywheel",
                "experimental IE / magic-number tables",
            ],
            test_statistic="out_of_sample_correlation_or_ablation",
            multiple_testing="bonferroni",
            falsification=(
                "Ablating noble-gas bonuses removes all predictive alignment; "
                "held-out properties not predicted above chance."
            ),
        ),
        HypothesisSpec(
            name="magic_island_class_number",
            claim="Magic Island structure is predicted by class-number-like invariants.",
            claim_type="Hypothesis",
            null_hypothesis="Island locations are independent of class_number_analogue.",
            alpha=0.05,
            domains=["model_islands", "reduced_configs"],
            data_sources=["qga/lib/flux_topograph.py", "qga/lib/composition.py"],
            test_statistic="association_or_rank_correlation",
            multiple_testing="fdr",
            falsification="No significant association after pre-registration.",
        ),
    ]


def bonferroni_threshold(alpha: float, n_tests: int) -> float:
    """Per-test α under Bonferroni correction."""
    if n_tests <= 0:
        return float("nan")
    return alpha / n_tests


def combine_p_values_fisher(p_values: list[float]) -> dict[str, float]:
    """Fisher's method for combining independent p-values.

    Returns chi2 statistic, df, and approximate combined p-value.
    Uses survival function of chi2 via incomplete gamma / series fallback.
    """
    ps = [float(p) for p in p_values if 0 < float(p) <= 1]
    if not ps:
        return {"chi2": float("nan"), "df": 0.0, "combined_p": float("nan"), "n": 0.0}
    chi2 = -2.0 * sum(math.log(p) for p in ps)
    df = 2 * len(ps)
    # regularized gamma Q(df/2, chi2/2) ≈ upper incomplete / Gamma
    # scipy-free approximation via survival of chi2
    try:
        from math import gamma

        # series for lower incomplete gamma, then Q = 1 - P
        k = df / 2.0
        x = chi2 / 2.0
        # lower incomplete P(k,x)
        term = 1.0 / k
        s = term
        for n in range(1, 200):
            term *= x / (k + n)
            s += term
            if term < 1e-14:
                break
        lower = s * math.exp(-x + k * math.log(x) - math.lgamma(k))
        combined = max(0.0, min(1.0, 1.0 - lower))
    except Exception:
        combined = float("nan")
    return {"chi2": chi2, "df": float(df), "combined_p": combined, "n": float(len(ps))}


def proximity_to_wg(
    values: list[float],
    *,
    target: float = WG_350_OVER_PI,
    relative: bool = True,
) -> dict[str, Any]:
    """Diagnostic: how close a list of observed numbers is to W_g = 350/π."""
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return {"target": target, "n": 0, "mean_abs_error": float("nan")}
    err = np.abs(arr - target)
    if relative:
        rel = err / (abs(target) + 1e-12)
    else:
        rel = err
    return {
        "target": target,
        "n": int(arr.size),
        "mean_abs_error": float(np.mean(err)),
        "median_abs_error": float(np.median(err)),
        "mean_rel_error": float(np.mean(rel)),
        "min_abs_error": float(np.min(err)),
        "values": arr.tolist(),
    }


def open_problems_status_table() -> list[dict[str, str]]:
    """Snapshot of OP1–OP6 status for Chapter 10 summary."""
    return [
        {
            "id": "OP1",
            "problem": "Canonical quaternionic Farey structure",
            "home": "Ch. 3",
            "status": "Open — candidate_adjacency sandbox",
            "next": "Refine adjacency; prove Farey reduction",
        },
        {
            "id": "OP2",
            "problem": "Flux topograph axioms",
            "home": "Ch. 5",
            "status": "Open — flux_topograph sandbox",
            "next": "Formal axiom system reducing to Hatcher",
        },
        {
            "id": "OP3",
            "problem": "Class number ↔ Magic Island",
            "home": "Ch. 6",
            "status": "Open — class_number_analogue heuristic",
            "next": "Invariant predicting island location/size",
        },
        {
            "id": "OP4",
            "problem": "Z→flywheel uniqueness",
            "home": "Ch. 7 / 10",
            "status": "Open — map implemented",
            "next": "Classify gauge ambiguity",
        },
        {
            "id": "OP5",
            "problem": "350/π first principles or falsification",
            "home": "Ch. 10",
            "status": "Open — hypothesis layer",
            "next": "Execute Table T4 pre-registered tests",
        },
        {
            "id": "OP6",
            "problem": "Composition of flywheels (Gauss lift)",
            "home": "Ch. 8–9",
            "status": "Open — low sandbox closure; algebraic tools ready",
            "next": "Ideal-theoretic associative law",
        },
    ]


def toy_multidomain_pvalues(
    *,
    seed: int = 0,
    n_domains: int = 5,
    null: bool = True,
) -> list[float]:
    """Generate *illustrative* per-domain p-values for lab demos only.

    If ``null=True``, draws under H0 (Uniform[0,1]). If False, mildly biased
    toward small p (for illustration of a signal — **not real data**).
    """
    rng = np.random.default_rng(seed)
    if null:
        return [float(x) for x in rng.uniform(0, 1, size=n_domains)]
    # Beta(0.5, 3) skews small — demo only
    return [float(x) for x in rng.beta(0.5, 3.0, size=n_domains)]


def run_table_t4_demo(
    p_values: list[float] | None = None,
    *,
    alpha: float = 0.01,
    seed: int = 0,
) -> dict[str, Any]:
    """Run a pedagogical Table T4 decision on (possibly toy) p-values.

    **Not** a claim that 350/π has been validated. Lab 10.B style diagnostic.
    """
    if p_values is None:
        p_values = toy_multidomain_pvalues(seed=seed, null=True)
    n = len(p_values)
    thr = bonferroni_threshold(alpha, n)
    fisher = combine_p_values_fisher(p_values)
    per_test_reject = [p < thr for p in p_values]
    combined_reject = fisher["combined_p"] < alpha if not math.isnan(fisher["combined_p"]) else False
    return {
        "alpha": alpha,
        "n_tests": n,
        "bonferroni_threshold": thr,
        "p_values": p_values,
        "per_test_reject": per_test_reject,
        "fisher": fisher,
        "combined_reject_at_alpha": combined_reject,
        "decision": (
            "reject_H0_combined"
            if combined_reject
            else "fail_to_reject_H0"
        ),
        "disclaimer": "Demo only unless p_values come from pre-registered real tests.",
    }
