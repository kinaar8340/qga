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
| T4.5 | Power analysis | Minimum detectable effect at 80% power. |
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

### H1 — Multi-domain \(350/\pi\)

| Field | Content |
|-------|---------|
| **Claim** | \(W_g=350/\pi\) is a shared topological clock across named domains. |
| **Type** | Hypothesis |
| **Null** | Recurrence near \(350/\pi\) is consistent with random coincidence at \(\alpha=0.01\). |
| **Domains** | pulsar timing; Bitcoin Pi Cycle; TLS trees; cuprate SC sketches; structural constants |
| **Sources** | `kingdom/observations/`; portal Observations tab; related assets |
| **Statistic** | Combined \(p\)-value or topological distance to model sequences |
| **Correction** | Bonferroni |
| **Falsification** | Fail to reject \(H_0\) after pre-registration + correction; or independent replication finds no excess clustering |

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
5. Check power (T4.5).  
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
