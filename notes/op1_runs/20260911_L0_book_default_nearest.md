# OP1 adjacency harness — L0 / book_default (rule=candidate, resnap=nearest)

Claim type: **Software fact**. OP1 status: **Open**. Not a theorem of Chapter 3.

- flux-hopf-lib `0.3.1`
- `hopf_map((0,0,1,0)) = [0.0, 0.0, -1.0]`
- n_points = 24
- rule = `candidate`

## Experiment 1 — is E_parallel a Hopf fiber?

Top-level `along_on_true_fiber` uses the **rule's** E_parallel as denominator.
Constructed consecutive (Lsg) is a **different list** and must not be collapsed.

| field | value |
|---|---|
| n_along (rule E_parallel) | 0 |
| n_inter | 36 |
| along_on_true_fiber | n/a (0 edges) |
| denominator | n_along=0 from candidate E_parallel; not constructed consecutive |
| how | min Euclidean R^4 from q_j to the left-U(1) orbit {e^{iφ} q_i} (same circle as sample_structure_group_fiber / common_phase); along_on_true_fiber iff that distance < 0.001 |
| along_base_near_0 | n/a (0 edges) |
| along_chart_only | n/a (0 edges) |
| inter_leaks_into_along | 1.000000 |
| source | `candidate_adjacency` |

### Fiber census (h(Λ), not a Farey diagram)

- n_distinct_bases = 6
- multiplicity histogram (phases per base) = {'4': 6}
- along_kind = `no_along_edges`
- along_equals_consecutive_U(1) = False
- No along-edges. On Λ0 at book_default this is chart sparsity (not a Farey graph). Use U(1) occupancy, not a looser η-tol.

- image: `octahedron_poles` — **Theorem**. Classical Hopf map sends the 24 Hurwitz units (24-cell vertices) to the 6 octahedron poles on S^2, four units per fiber.
- along-edges claim: **Software fact** (not Farey neighbors).

Inter-edge base distances: n=36, min=0.000e+00, max=0.000e+00, n_exact_zero=36, leak_is_exact=True.

## Experiment 2 — units i and j (not an L/R average)

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| i | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| j | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| j | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |

## Experiment 2 — 24 × 2

| unit | side | along_kept | inter_kept | along_to_inter | lost | n_along | n_inter |
|---|---|---|---|---|---|---|---|
| i | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| i | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| -1 | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| -1 | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| 1 | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| 1 | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| -i | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| -i | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| -j | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| -j | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| j | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| j | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| -k | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| -k | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| k | L | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| k | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_---- | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_---- | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_---+ | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_---+ | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_--+- | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_--+- | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_--++ | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_--++ | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_-+-- | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_-+-- | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_-+-+ | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_-+-+ | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_-++- | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_-++- | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_-+++ | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_-+++ | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+--- | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+--- | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+--+ | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+--+ | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+-+- | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+-+- | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+-++ | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+-++ | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_++-- | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_++-- | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_++-+ | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_++-+ | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+++- | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_+++- | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_++++ | L | n/a (0 edges) | 0.333333 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
| half_++++ | R | n/a (0 edges) | 1.000000 | n/a (0 edges) | n/a (0 edges) | 0 | 36 |
