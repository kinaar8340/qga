# OP1 adjacency harness — Lsg / book_default (rule=structure_group, resnap=none)

Claim type: **Software fact**. OP1 status: **Open**. Not a theorem of Chapter 3.

- flux-hopf-lib `0.3.1`
- `hopf_map((0,0,1,0)) = [0.0, 0.0, -1.0]`
- n_points = 64
- rule = `structure_group`

## Experiment 1 — is E_parallel a Hopf fiber?

Top-level `along_on_true_fiber` uses the **rule's** E_parallel as denominator.
Constructed consecutive (Lsg) is a **different list** and must not be collapsed.

| field | value |
|---|---|
| n_along (rule E_parallel) | 64 |
| n_inter | 6 |
| along_on_true_fiber | 1.000000 |
| denominator | n_along=64 from structure_group E_parallel; not constructed consecutive |
| how | min Euclidean R^4 from q_j to the left-U(1) orbit {e^{iφ} q_i} (same circle as sample_structure_group_fiber / common_phase); along_on_true_fiber iff that distance < 0.001 |
| along_base_near_0 | 1.000000 |
| along_chart_only | 0.000000 |
| inter_leaks_into_along | 0.000000 |
| source | `structure_group_adjacency` |

### Fiber census (h(Λ), not a Farey diagram)

- n_distinct_bases = 4
- multiplicity histogram (phases per base) = {'16': 4}
- along_kind = `consecutive_u1_on_sampled_fibers`
- along_equals_consecutive_U(1) = True
- Along-edges are consecutive U(1) steps on sampled structure-group fibers (true by construction). Only Lsg has along = structure group by construction. Not a Farey diagram.

- image: `sampled_structure_group_fibers` — **Software fact**. Controlled true fibers. Only this set has along = structure group by construction.
- along-edges claim: **Software fact** (not Farey neighbors).

Inter-edge base distances: n=6, min=1.571e+00, max=3.142e+00, n_exact_zero=0, leak_is_exact=False.

### Lsg consecutive samples (by construction, true fiber)

Denominator is **64 constructed consecutive samples**, not the rule's n_along.

| field | value |
|---|---|
| n_along | 64 |
| along_on_true_fiber | 1.000000 |
| denominator | n_along=64 consecutive samples on sample_structure_group_fiber (wrap included); not structure_group E_parallel |
| along_base_near_0 | 1.000000 |
| along_chart_only | 0.000000 |

Lsg hopf_map scatter per fiber: [1.1102230246251565e-16, 1.1102230246251565e-16, 2.2887833992611187e-16, 2.237726045655905e-16] (max 2.2887833992611187e-16; pin requires < 1e-8).

## Experiment 2 — units i and j (not an L/R average)

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| i | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| j | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| j | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |

## Experiment 2 — 24 × 2

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| i | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| -1 | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| -1 | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| 1 | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| 1 | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| -i | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| -i | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| -j | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| -j | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| j | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| j | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| -k | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| -k | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| k | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| k | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_---- | L | 0.000000 | 0.000000 | 0.171875 | 0.828125 | 64 | 6 |
| half_---- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_---+ | L | 0.000000 | 0.000000 | 0.156250 | 0.843750 | 64 | 6 |
| half_---+ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_--+- | L | 0.000000 | 0.000000 | 0.156250 | 0.843750 | 64 | 6 |
| half_--+- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_--++ | L | 0.000000 | 0.000000 | 0.171875 | 0.828125 | 64 | 6 |
| half_--++ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_-+-- | L | 0.000000 | 0.000000 | 0.156250 | 0.843750 | 64 | 6 |
| half_-+-- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_-+-+ | L | 0.000000 | 0.000000 | 0.171875 | 0.828125 | 64 | 6 |
| half_-+-+ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_-++- | L | 0.000000 | 0.000000 | 0.171875 | 0.828125 | 64 | 6 |
| half_-++- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_-+++ | L | 0.000000 | 0.000000 | 0.156250 | 0.843750 | 64 | 6 |
| half_-+++ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_+--- | L | 0.000000 | 0.000000 | 0.156250 | 0.843750 | 64 | 6 |
| half_+--- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_+--+ | L | 0.000000 | 0.000000 | 0.171875 | 0.828125 | 64 | 6 |
| half_+--+ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_+-+- | L | 0.000000 | 0.000000 | 0.171875 | 0.828125 | 64 | 6 |
| half_+-+- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_+-++ | L | 0.000000 | 0.000000 | 0.156250 | 0.843750 | 64 | 6 |
| half_+-++ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_++-- | L | 0.000000 | 0.000000 | 0.171875 | 0.828125 | 64 | 6 |
| half_++-- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_++-+ | L | 0.000000 | 0.000000 | 0.156250 | 0.843750 | 64 | 6 |
| half_++-+ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_+++- | L | 0.000000 | 0.000000 | 0.156250 | 0.843750 | 64 | 6 |
| half_+++- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
| half_++++ | L | 0.000000 | 0.000000 | 0.171875 | 0.828125 | 64 | 6 |
| half_++++ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 64 | 6 |
