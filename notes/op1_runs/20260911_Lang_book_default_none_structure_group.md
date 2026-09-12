# OP1 adjacency harness — Lang / book_default (rule=structure_group, resnap=none)

Claim type: **Software fact**. OP1 status: **Open**. Not a theorem of Chapter 3.

- flux-hopf-lib `0.3.1`
- `hopf_map((0,0,1,0)) = [0.0, 0.0, -1.0]`
- n_points = 256
- rule = `structure_group`

## Experiment 1 — is E_parallel a Hopf fiber?

Top-level `along_on_true_fiber` uses the **rule's** E_parallel as denominator.
Constructed consecutive (Lsg) is a **different list** and must not be collapsed.

| field | value |
|---|---|
| n_along (rule E_parallel) | 256 |
| n_inter | 90 |
| along_on_true_fiber | 1.000000 |
| denominator | n_along=256 from structure_group E_parallel; not constructed consecutive |
| how | min Euclidean R^4 from q_j to the left-U(1) orbit {e^{iφ} q_i} (same circle as sample_structure_group_fiber / common_phase); along_on_true_fiber iff that distance < 0.01 |
| along_base_near_0 | 1.000000 |
| along_chart_only | 0.000000 |
| inter_leaks_into_along | 0.000000 |
| source | `structure_group_adjacency` |

### Fiber census (h(Λ), not a Farey diagram)

- n_distinct_bases = 32
- multiplicity histogram (phases per base) = {'8': 32}
- along_kind = `consecutive_u1_steps_on_product_sample`
- along_equals_consecutive_U(1) = True
- 8 phases × 32 bases: discrete fiber bundle with a Delaunay base. Not a Farey diagram and not occupancy-necklace 256.

- image: `angle_product_sample` — **Software fact**. Product sample, not a theorem of the 24-cell. Same integer 256 as the occupancy necklace, different graph.
- along-edges claim: **Software fact** (not Farey neighbors).

Inter-edge base distances: n=90, min=2.992e-01, max=1.483e+00, n_exact_zero=0, leak_is_exact=False.

## Experiment 2 — units i and j (not an L/R average)

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 0.944444 | 0.000000 | 0.000000 | 256 | 90 |
| i | R | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
| j | L | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
| j | R | 1.000000 | 0.833333 | 0.000000 | 0.000000 | 256 | 90 |

## Experiment 2 — 24 × 2

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 0.944444 | 0.000000 | 0.000000 | 256 | 90 |
| i | R | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
| -1 | L | 1.000000 | 0.944444 | 0.000000 | 0.000000 | 256 | 90 |
| -1 | R | 1.000000 | 0.944444 | 0.000000 | 0.000000 | 256 | 90 |
| 1 | L | 1.000000 | 0.944444 | 0.000000 | 0.000000 | 256 | 90 |
| 1 | R | 1.000000 | 0.944444 | 0.000000 | 0.000000 | 256 | 90 |
| -i | L | 1.000000 | 0.944444 | 0.000000 | 0.000000 | 256 | 90 |
| -i | R | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
| -j | L | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
| -j | R | 1.000000 | 0.833333 | 0.000000 | 0.000000 | 256 | 90 |
| j | L | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
| j | R | 1.000000 | 0.833333 | 0.000000 | 0.000000 | 256 | 90 |
| -k | L | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
| -k | R | 1.000000 | 0.877778 | 0.000000 | 0.000000 | 256 | 90 |
| k | L | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
| k | R | 1.000000 | 0.877778 | 0.000000 | 0.000000 | 256 | 90 |
| half_---- | L | 0.000000 | 0.111111 | 0.011719 | 0.988281 | 256 | 90 |
| half_---- | R | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
| half_---+ | L | 0.000000 | 0.155556 | 0.011719 | 0.988281 | 256 | 90 |
| half_---+ | R | 1.000000 | 0.800000 | 0.000000 | 0.000000 | 256 | 90 |
| half_--+- | L | 0.000000 | 0.122222 | 0.011719 | 0.988281 | 256 | 90 |
| half_--+- | R | 1.000000 | 0.800000 | 0.000000 | 0.000000 | 256 | 90 |
| half_--++ | L | 0.000000 | 0.133333 | 0.011719 | 0.988281 | 256 | 90 |
| half_--++ | R | 1.000000 | 0.788889 | 0.000000 | 0.000000 | 256 | 90 |
| half_-+-- | L | 0.000000 | 0.111111 | 0.011719 | 0.988281 | 256 | 90 |
| half_-+-- | R | 1.000000 | 0.777778 | 0.000000 | 0.000000 | 256 | 90 |
| half_-+-+ | L | 0.000000 | 0.166667 | 0.011719 | 0.988281 | 256 | 90 |
| half_-+-+ | R | 1.000000 | 0.822222 | 0.000000 | 0.000000 | 256 | 90 |
| half_-++- | L | 0.000000 | 0.155556 | 0.011719 | 0.988281 | 256 | 90 |
| half_-++- | R | 1.000000 | 0.755556 | 0.000000 | 0.000000 | 256 | 90 |
| half_-+++ | L | 0.000000 | 0.155556 | 0.011719 | 0.988281 | 256 | 90 |
| half_-+++ | R | 1.000000 | 0.777778 | 0.000000 | 0.000000 | 256 | 90 |
| half_+--- | L | 0.000000 | 0.155556 | 0.011719 | 0.988281 | 256 | 90 |
| half_+--- | R | 1.000000 | 0.777778 | 0.000000 | 0.000000 | 256 | 90 |
| half_+--+ | L | 0.000000 | 0.155556 | 0.011719 | 0.988281 | 256 | 90 |
| half_+--+ | R | 1.000000 | 0.755556 | 0.000000 | 0.000000 | 256 | 90 |
| half_+-+- | L | 0.000000 | 0.166667 | 0.011719 | 0.988281 | 256 | 90 |
| half_+-+- | R | 1.000000 | 0.822222 | 0.000000 | 0.000000 | 256 | 90 |
| half_+-++ | L | 0.000000 | 0.111111 | 0.011719 | 0.988281 | 256 | 90 |
| half_+-++ | R | 1.000000 | 0.777778 | 0.000000 | 0.000000 | 256 | 90 |
| half_++-- | L | 0.000000 | 0.133333 | 0.011719 | 0.988281 | 256 | 90 |
| half_++-- | R | 1.000000 | 0.788889 | 0.000000 | 0.000000 | 256 | 90 |
| half_++-+ | L | 0.000000 | 0.122222 | 0.011719 | 0.988281 | 256 | 90 |
| half_++-+ | R | 1.000000 | 0.800000 | 0.000000 | 0.000000 | 256 | 90 |
| half_+++- | L | 0.000000 | 0.155556 | 0.011719 | 0.988281 | 256 | 90 |
| half_+++- | R | 1.000000 | 0.800000 | 0.000000 | 0.000000 | 256 | 90 |
| half_++++ | L | 0.000000 | 0.111111 | 0.011719 | 0.988281 | 256 | 90 |
| half_++++ | R | 1.000000 | 0.811111 | 0.000000 | 0.000000 | 256 | 90 |
