# Appendix D — Table T4 Validation Protocols (Full)

Pre-registered validation machinery for Part V Hypotheses. Chapter 10 keeps a short summary; this appendix is the full checklist, hypothesis catalog, and demo usage.

Helpers: `lib/validation.py`.

---

## D.1 Core checklist (Table T4)

| ID | Element | Description |
|----|---------|-------------|
| T4.1 | Null hypothesis definition | State \(H_0\) with significance level \(\alpha\) (default \(0.01\)). |
| T4.2 | Data sources and preprocessing | List datasets, windows, and cleaning rules. |
| T4.3 | Test statistic | Define the scalar or vector statistic used for decision. |
| T4.4 | Multiple-testing correction | Bonferroni or FDR control across domains/tests. |
| T4.5 | Pre-registered sample size | Was the pre-registered \((n)\) achieved? Not post-hoc power after T4.4. |
| T4.6 | Falsification criteria | What result counts as strong evidence against the alternative. |
| T4.7 | Pre-registration | Timestamped commit or external registry **before** looking at new data. |
| T4.8 | Reproducibility | Full code, seeds, and environment for every figure and table. |

```python
from lib.validation import table_t4_checklist
for row in table_t4_checklist():
    print(row["id"], row["element"])
```

---

## D.2 Catalog of major hypotheses

These match `default_hypotheses()` in code.

### H1a–H1e — \(W_g=350/\pi\) per domain (not one bundled clock)

Domain list locked \(2026\text{-}08\text{-}28\) **before** \(p\)-values. One symbol: \(W_g=350/\pi\) (not \(350\pi\)). Bonferroni \(n=5\). Each row has its own T4 checklist, MDE, and pre-registered \(n\) (T4.5).

| ID | Domain | Claim (Hypothesis) |
|----|--------|--------------------|
| H1a | pulsar_timing | Clustering near \(W_g=350/\pi\) in pulsar-timing narratives |
| H1b | bitcoin_pi_cycle | Clustering near \(W_g=350/\pi\) in Bitcoin Pi Cycle notes |
| H1c | tls_trees | Clustering near \(W_g=350/\pi\) in TLS tree analysis |
| H1d | cuprate_superconductors | Clustering near \(W_g=350/\pi\) in cuprate sketches |
| H1e | structural_constants | Clustering near \(W_g=350/\pi\) in structural constants |

| Field | Content (each H1\(\ast\)) |
|-------|---------|
| **Type** | Hypothesis |
| **Null** | Recurrence in *that* domain is consistent with random coincidence at \(\alpha=0.01\). |
| **Correction** | Bonferroni \(n=5\) (locked with the domain list) |
| **T4.5** | Was the pre-registered \((n)\) for that domain achieved? |
| **Falsification** | Fail to reject \(H_0\) in that domain after pre-registration; or pre-registered \(n\) not achieved |

Do not recombine H1a–H1e into a single “shared clock” claim. No new observational domains on H1 in this revision.

### H2 — \(Z\mapsto\) map as periodic-table proxy

| Field | Content |
|-------|---------|
| **Claim** | `map_z_to_flywheel` stability peaks reflect genuine chemical/nuclear specialness beyond model tuning. |
| **Type** | Hypothesis |
| **Null** | High scores near noble gases are explained by explicit model bonuses alone (no extra predictive content). |
| **Domains** | periodic table; ionization energy; nuclear magic numbers |
| **Statistic** | Out-of-sample correlation or ablation study |
| **Falsification** | Ablating noble-gas bonuses removes all predictive alignment; held-out properties not above chance |

### H3 — Magic Island ↔ class-number association

| Field | Content |
|-------|---------|
| **Claim** | Magic Island structure is predicted by class-number-like invariants. |
| **Type** | Hypothesis |
| **Null** | Island locations independent of `class_number_analogue`. |
| **Statistic** | Association / rank correlation |
| **Correction** | FDR |
| **Falsification** | No significant association after pre-registration |

```python
from lib.validation import default_hypotheses
for h in default_hypotheses():
    print(h.name, h.alpha, h.null_hypothesis[:60], "...")
```

---

## D.3 Statistical helpers

```python
from lib.validation import (
    WG_350_OVER_PI,
    bonferroni_threshold,
    combine_p_values_fisher,
    proximity_to_wg,
    run_table_t4_demo,
    toy_multidomain_pvalues,
)

print("W_g =", WG_350_OVER_PI)
print("Bonferroni thr (α=0.01, n=5):", bonferroni_threshold(0.01, 5))

# Toy null demo — NOT evidence for 350/π
demo = run_table_t4_demo(seed=1, alpha=0.01)
print(demo["decision"], demo["fisher"])

# Diagnostic closeness of constants to W_g
print(proximity_to_wg([111.4, 111.5, 110.0, 111.408]))
```

Under the **null toy** generator, expect frequent `fail_to_reject_H0`. Real domain \(p\)-values without pre-registration do **not** count as T4 success.

---

## D.4 Decision flowchart (narrative)

1. Write \(H_0\), \(\alpha\), statistic, and falsification (T4.1, T4.3, T4.6).  
2. Lock data sources and preprocessing (T4.2).  
3. Pre-register (T4.7) — e.g. git tag / commit hash.  
4. Compute statistics; apply multiple-testing correction (T4.4).  
5. Check that the pre-registered \((n)\) was achieved (T4.5) — not post-hoc power.  
6. Decide: reject \(H_0\) / fail to reject / refine design.  
7. Publish code and seeds (T4.8).

Figure 10.4 in Chapter 10 is the visual summary of this flow.

---

## D.5 Claim discipline for validation results

| Statement | Label |
|-----------|--------|
| “Table T4 exists in the repo” | **Software fact** |
| “Hypothesis \(X\) passed T4” | **Hypothesis** until full checklist executed and reviewed |
| “\(W_g\) is a law of nature” | **Hypothesis** (not default) |

---

*Manuscript · Appendix D · Table T4 Validation Protocols.*
