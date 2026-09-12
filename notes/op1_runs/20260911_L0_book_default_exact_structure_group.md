# OP1 adjacency harness — L0 / book_default (rule=structure_group, resnap=exact)

Claim type: **Software fact**. OP1 status: **Open**. Not a theorem of Chapter 3.

- flux-hopf-lib `0.3.1`
- `hopf_map((0,0,1,0)) = [0.0, 0.0, -1.0]`
- n_points = 24
- rule = `structure_group`

## Experiment 1 — is E_parallel a Hopf fiber?

Top-level `along_on_true_fiber` uses the **rule's** E_parallel as denominator.
Constructed consecutive (Lsg) is a **different list** and must not be collapsed.

| field | value |
|---|---|
| n_along (rule E_parallel) | 24 |
| n_inter | 12 |
| along_on_true_fiber | 1.000000 |
| denominator | n_along=24 from structure_group E_parallel; not constructed consecutive |
| how | min Euclidean R^4 from q_j to the left-U(1) orbit {e^{iφ} q_i} (same circle as sample_structure_group_fiber / common_phase); along_on_true_fiber iff that distance < 0.001 |
| along_base_near_0 | 1.000000 |
| along_chart_only | 0.000000 |
| inter_leaks_into_along | 0.000000 |
| source | `structure_group_adjacency` |

### Fiber census (h(Λ), not a Farey diagram)

- n_distinct_bases = 6
- multiplicity histogram (phases per base) = {'4': 6}
- along_kind = `u1_occupancy_through_lambda0`
- along_equals_consecutive_U(1) = True
- 24 along-edges are occupancy of left-U(1) through Λ0 (cycles on occupied fibers), not 24 Farey neighbors. Software fact of Model 2; the 6×4 image is the Theorem.

- image: `octahedron_poles` — **Theorem**. Classical Hopf map sends the 24 Hurwitz units (24-cell vertices) to the 6 octahedron poles on S^2, four units per fiber.
- along-edges claim: **Software fact** (not Farey neighbors).

Inter-edge base distances: n=12, min=1.571e+00, max=1.571e+00, n_exact_zero=0, leak_is_exact=False.

## Experiment 2 — units i and j (not an L/R average)

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| i | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| j | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| j | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |

## Experiment 2 — 24 × 2

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| i | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| -1 | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| -1 | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| 1 | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| 1 | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| -i | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| -i | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| -j | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| -j | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| j | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| j | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| -k | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| -k | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| k | L | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| k | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_---- | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_---- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_---+ | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_---+ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_--+- | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_--+- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_--++ | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_--++ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_-+-- | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_-+-- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_-+-+ | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_-+-+ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_-++- | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_-++- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_-+++ | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_-+++ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_+--- | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_+--- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_+--+ | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_+--+ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_+-+- | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_+-+- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_+-++ | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_+-++ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_++-- | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_++-- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_++-+ | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_++-+ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_+++- | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_+++- | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
| half_++++ | L | 0.000000 | 0.416667 | 0.000000 | 1.000000 | 24 | 12 |
| half_++++ | R | 1.000000 | 1.000000 | 0.000000 | 0.000000 | 24 | 12 |
