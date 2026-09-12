# OP1 adjacency harness — Lang / book_default (rule=candidate, resnap=nearest)

Claim type: **Software fact**. OP1 status: **Open**. Not a theorem of Chapter 3.

- flux-hopf-lib `0.3.1`
- `hopf_map((0,0,1,0)) = [0.0, 0.0, -1.0]`
- n_points = 256
- rule = `candidate`

## Experiment 1 — is E_parallel a Hopf fiber?

Top-level `along_on_true_fiber` uses the **rule's** E_parallel as denominator.
Constructed consecutive (Lsg) is a **different list** and must not be collapsed.

| field | value |
|---|---|
| n_along (rule E_parallel) | 256 |
| n_inter | 1344 |
| along_on_true_fiber | 0.000000 |
| denominator | n_along=256 from candidate E_parallel; not constructed consecutive |
| how | min Euclidean R^4 from q_j to the left-U(1) orbit {e^{iφ} q_i} (same circle as sample_structure_group_fiber / common_phase); along_on_true_fiber iff that distance < 0.01 |
| along_base_near_0 | 0.000000 |
| along_chart_only | 1.000000 |
| inter_leaks_into_along | 0.666667 |
| source | `candidate_adjacency` |

### Fiber census (h(Λ), not a Farey diagram)

- n_distinct_bases = 32
- multiplicity histogram (phases per base) = {'8': 32}
- along_kind = `chart_xi2_circle_not_u1`
- along_equals_consecutive_U(1) = False
- Along-set is the angle-chart ξ2-circle, not consecutive U(1) on h(Λ) fibers.

- image: `angle_product_sample` — **Software fact**. Product sample, not a theorem of the 24-cell. Same integer 256 as the occupancy necklace, different graph.
- along-edges claim: **Software fact** (not Farey neighbors).

Inter-edge base distances: n=1344, min=0.000e+00, max=2.992e-01, n_exact_zero=457, leak_is_exact=False.

## Experiment 2 — units i and j (not an L/R average)

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| i | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| j | L | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |
| j | R | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |

## Experiment 2 — 24 × 2

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| i | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| -1 | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| -1 | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| 1 | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| 1 | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| -i | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| -i | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 256 | 1344 |
| -j | L | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |
| -j | R | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |
| j | L | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |
| j | R | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |
| -k | L | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |
| -k | R | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |
| k | L | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |
| k | R | 0.000000 | 0.666667 | 0.000000 | 1.000000 | 256 | 1344 |
| half_---- | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_---- | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_---+ | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_---+ | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_--+- | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_--+- | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_--++ | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_--++ | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_-+-- | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_-+-- | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_-+-+ | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_-+-+ | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_-++- | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_-++- | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_-+++ | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_-+++ | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_+--- | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_+--- | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_+--+ | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_+--+ | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_+-+- | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_+-+- | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_+-++ | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_+-++ | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_++-- | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_++-- | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_++-+ | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_++-+ | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_+++- | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_+++- | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
| half_++++ | L | 0.000000 | 0.130952 | 0.000000 | 1.000000 | 256 | 1344 |
| half_++++ | R | 0.000000 | 0.916667 | 0.125000 | 0.875000 | 256 | 1344 |
