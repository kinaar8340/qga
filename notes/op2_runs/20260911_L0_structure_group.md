# OP2 topograph harness — L0 / structure_group

Claim type: **Software fact**. OP2 status: **Open**. Skeleton is a Model choice.
OP1 remains Open. Not Ch. 5 axioms.

- attached OP1: `notes/op1_runs/20260911_L0_book_default_exact_structure_group.json`
- n_points = 24  n_along = 24  n_inter = 12
- Kirchhoff: True (max |r| = 0.0)

### Fiber census (from attached OP1 row)

- n_distinct_bases = 6
- multiplicity = {'4': 6}
- along_kind = `u1_occupancy_through_lambda0`

- image: `octahedron_poles` **Theorem**

## Separators (strict sign-crossing) and left-i / left-j

| functional | n_components | n_sep_edges | left-i n_comp after | left-j n_comp after | periodicity |
|---|---|---|---|---|---|
| hopf_height | 0 | 0 | 0 | 0 | i:undefined_or_vacuous j:undefined_or_vacuous |

Pole level sets for `hopf_height` (zeros are levels, not crossings):
- base [0.0, -0.0, 1.0] ×4: value=1.0
- base [0.0, 0.0, -1.0] ×4: value=-1.0
- base [1.0, 0.0, 0.0] ×4: value=0.0
- base [0.0, -1.0, 0.0] ×4: value=0.0
- base [0.0, 1.0, 0.0] ×4: value=0.0
- base [-1.0, 0.0, 0.0] ×4: value=0.0

| hopf_y1 | 0 | 0 | 0 | 0 | i:undefined_or_vacuous j:undefined_or_vacuous |

Pole level sets for `hopf_y1` (zeros are levels, not crossings):
- base [0.0, -0.0, 1.0] ×4: value=0.0
- base [0.0, 0.0, -1.0] ×4: value=0.0
- base [1.0, 0.0, 0.0] ×4: value=1.0
- base [0.0, -1.0, 0.0] ×4: value=0.0
- base [0.0, 1.0, 0.0] ×4: value=0.0
- base [-1.0, 0.0, 0.0] ×4: value=-1.0


Do not average L/R or i/j. Do not mix candidate edges.
