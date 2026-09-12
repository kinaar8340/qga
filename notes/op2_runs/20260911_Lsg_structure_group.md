# OP2 topograph harness — Lsg / structure_group

Claim type: **Software fact**. OP2 status: **Open**. Skeleton is a Model choice.
OP1 remains Open. Not Ch. 5 axioms.

- attached OP1: `notes/op1_runs/20260911_Lsg_book_default_none_structure_group.json`
- n_points = 64  n_along = 64  n_inter = 6
- Kirchhoff: True (max |r| = 0.0)

### Fiber census (from attached OP1 row)

- n_distinct_bases = 4
- multiplicity = {'16': 4}
- along_kind = `consecutive_u1_on_sampled_fibers`

- image: `sampled_structure_group_fibers` **Software fact**

## Separators (strict sign-crossing) and left-i / left-j

| functional | n_components | n_sep_edges | left-i n_comp after | left-j n_comp after | periodicity |
|---|---|---|---|---|---|
| hopf_height | 4 | 5 | 4 | 5 | i 4→4 j 4→5 (separator_component_count) |
| hopf_y1 | 0 | 0 | 0 | 0 | i:undefined_or_vacuous j:undefined_or_vacuous |

Do not average L/R or i/j. Do not mix candidate edges.
