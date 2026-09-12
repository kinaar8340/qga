# OP1 adjacency harness — Lsg / book_default (rule=candidate, resnap=none)

Claim type: **Software fact**. OP1 status: **Open**. Not a theorem of Chapter 3.

- flux-hopf-lib `0.3.1`
- `hopf_map((0,0,1,0)) = [0.0, 0.0, -1.0]`
- n_points = 64
- rule = `candidate`

## Experiment 1 — is E_parallel a Hopf fiber?

Top-level `along_on_true_fiber` uses the **rule's** E_parallel as denominator.
Constructed consecutive (Lsg) is a **different list** and must not be collapsed.

| field | value |
|---|---|
| n_along (rule E_parallel) | 26 |
| n_inter | 454 |
| along_on_true_fiber | 1.000000 |
| denominator | n_along=26 from candidate E_parallel; not constructed consecutive |
| how | min Euclidean R^4 from q_j to the left-U(1) orbit {e^{iφ} q_i} (same circle as sample_structure_group_fiber / common_phase); along_on_true_fiber iff that distance < 0.001 |
| along_base_near_0 | 1.000000 |
| along_chart_only | 0.000000 |
| inter_leaks_into_along | 1.000000 |
| source | `candidate_adjacency` |

### Fiber census (h(Λ), not a Farey diagram)

- n_distinct_bases = 4
- multiplicity histogram (phases per base) = {'16': 4}
- along_kind = `chart_xi2_circle_not_u1`
- along_equals_consecutive_U(1) = False
- Along-set is the angle-chart ξ2-circle, not consecutive U(1) on h(Λ) fibers.

- image: `sampled_structure_group_fibers` — **Software fact**. Controlled true fibers. Only this set has along = structure group by construction.
- along-edges claim: **Software fact** (not Farey neighbors).

Inter-edge base distances: n=454, min=0.000e+00, max=2.980e-08, n_exact_zero=314, leak_is_exact=False.

### Lsg consecutive samples (by construction, true fiber)

Denominator is **64 constructed consecutive samples**, not the rule's n_along.

| field | value |
|---|---|
| n_along | 64 |
| along_on_true_fiber | 1.000000 |
| denominator | n_along=64 consecutive samples on sample_structure_group_fiber (wrap included); not candidate E_parallel |
| along_base_near_0 | 1.000000 |
| along_chart_only | 0.000000 |

Lsg hopf_map scatter per fiber: [1.1102230246251565e-16, 1.1102230246251565e-16, 2.2887833992611187e-16, 2.237726045655905e-16] (max 2.2887833992611187e-16; pin requires < 1e-8).

## Experiment 2 — units i and j (not an L/R average)

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 0.986784 | 0.000000 | 0.000000 | 26 | 454 |
| i | R | 1.000000 | 0.986784 | 0.000000 | 0.000000 | 26 | 454 |
| j | L | 0.000000 | 0.942731 | 1.000000 | 0.000000 | 26 | 454 |
| j | R | 0.000000 | 0.942731 | 1.000000 | 0.000000 | 26 | 454 |

## Experiment 2 — 24 × 2

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 0.986784 | 0.000000 | 0.000000 | 26 | 454 |
| i | R | 1.000000 | 0.986784 | 0.000000 | 0.000000 | 26 | 454 |
| -1 | L | 0.884615 | 0.993392 | 0.115385 | 0.000000 | 26 | 454 |
| -1 | R | 0.884615 | 0.993392 | 0.115385 | 0.000000 | 26 | 454 |
| 1 | L | 1.000000 | 0.986784 | 0.000000 | 0.000000 | 26 | 454 |
| 1 | R | 1.000000 | 0.986784 | 0.000000 | 0.000000 | 26 | 454 |
| -i | L | 1.000000 | 0.986784 | 0.000000 | 0.000000 | 26 | 454 |
| -i | R | 1.000000 | 0.986784 | 0.000000 | 0.000000 | 26 | 454 |
| -j | L | 0.000000 | 0.929515 | 1.000000 | 0.000000 | 26 | 454 |
| -j | R | 0.000000 | 0.929515 | 1.000000 | 0.000000 | 26 | 454 |
| j | L | 0.000000 | 0.942731 | 1.000000 | 0.000000 | 26 | 454 |
| j | R | 0.000000 | 0.942731 | 1.000000 | 0.000000 | 26 | 454 |
| -k | L | 0.000000 | 0.929515 | 1.000000 | 0.000000 | 26 | 454 |
| -k | R | 0.000000 | 0.929515 | 1.000000 | 0.000000 | 26 | 454 |
| k | L | 0.000000 | 0.942731 | 1.000000 | 0.000000 | 26 | 454 |
| k | R | 0.000000 | 0.942731 | 1.000000 | 0.000000 | 26 | 454 |
| half_---- | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_---- | R | 0.000000 | 1.000000 | 1.000000 | 0.000000 | 26 | 454 |
| half_---+ | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_---+ | R | 0.000000 | 0.966960 | 1.000000 | 0.000000 | 26 | 454 |
| half_--+- | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_--+- | R | 0.000000 | 1.000000 | 1.000000 | 0.000000 | 26 | 454 |
| half_--++ | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_--++ | R | 0.000000 | 0.947137 | 1.000000 | 0.000000 | 26 | 454 |
| half_-+-- | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_-+-- | R | 0.000000 | 0.960352 | 1.000000 | 0.000000 | 26 | 454 |
| half_-+-+ | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_-+-+ | R | 0.000000 | 0.953744 | 1.000000 | 0.000000 | 26 | 454 |
| half_-++- | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_-++- | R | 0.000000 | 1.000000 | 1.000000 | 0.000000 | 26 | 454 |
| half_-+++ | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_-+++ | R | 0.000000 | 1.000000 | 1.000000 | 0.000000 | 26 | 454 |
| half_+--- | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_+--- | R | 0.000000 | 1.000000 | 1.000000 | 0.000000 | 26 | 454 |
| half_+--+ | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_+--+ | R | 0.000000 | 1.000000 | 1.000000 | 0.000000 | 26 | 454 |
| half_+-+- | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_+-+- | R | 0.000000 | 0.944934 | 1.000000 | 0.000000 | 26 | 454 |
| half_+-++ | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_+-++ | R | 0.000000 | 0.960352 | 1.000000 | 0.000000 | 26 | 454 |
| half_++-- | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_++-- | R | 0.000000 | 0.953744 | 1.000000 | 0.000000 | 26 | 454 |
| half_++-+ | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_++-+ | R | 0.000000 | 1.000000 | 1.000000 | 0.000000 | 26 | 454 |
| half_+++- | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_+++- | R | 0.000000 | 0.960352 | 1.000000 | 0.000000 | 26 | 454 |
| half_++++ | L | 0.000000 | 0.070485 | 0.000000 | 1.000000 | 26 | 454 |
| half_++++ | R | 0.000000 | 1.000000 | 1.000000 | 0.000000 | 26 | 454 |
