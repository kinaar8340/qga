# OP2 topograph harness — Lang / structure_group

Claim type: **Software fact**. OP2 status: **Open**. Skeleton is a Model choice.
OP1 remains Open. Not Ch. 5 axioms.

- attached OP1: `notes/op1_runs/20260911_Lang_book_default_none_structure_group.json`
- n_points = 256  n_along = 256  n_inter = 90
- Kirchhoff: True (max |r| = 0.0)

### Fiber census (from attached OP1 row)

- n_distinct_bases = 32
- multiplicity = {'8': 32}
- along_kind = `consecutive_u1_steps_on_product_sample`

- image: `angle_product_sample` **Software fact**

## Separators (strict sign-crossing) and left-i / left-j

| functional | n_components | n_sep_edges | left-i n_comp after | left-j n_comp after | periodicity |
|---|---|---|---|---|---|
| hopf_height | 1 | 16 | 1 | 1 | i 1→1 j 1→1 (delaunay_periodicity) |
| hopf_y1 | 8 | 37 | 9 | 9 | i 8→9 j 8→9 (delaunay_periodicity) |
OP1 inter_kept attached for `hopf_y1`: left-i=0.9444444444444444 left-j=0.8111111111111111. 8→9 component move is OP1 inter_kept<1 visible in OP2. Do not smooth it.


Do not average L/R or i/j. Do not mix candidate edges.
