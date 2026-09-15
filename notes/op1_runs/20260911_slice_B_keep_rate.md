# OP1-B keep-rate index

Claim: **Software fact**. `slice_status`: **B indexed, not extended**. OP1 stays **Open**.

Not a new experiment. Do not rerun `scripts/op1_adjacency/run.py` for this file. The 24×2 tables on Lsg and L0 **are** B for Model 2.

```text
Model 2 Lsg → notes/op1_runs/20260911_Lsg_book_default_none_structure_group.json  (24×2)
Model 2 L0  → notes/op1_runs/20260911_L0_book_default_exact_structure_group.json (24×2)
Lang dump (witness, not B): notes/op1_runs/20260911_Lang_book_default_none_structure_group_graph.json
candidate / open sample → parked
```

Sides are not averaged. Lipschitz 8 \(\{\pm1,\pm i,\pm j,\pm k\}\): `along_kept = inter_kept = 1` on L and R, both attached sets. All 16 half-units: **right** stays 1; **left** dies (`along_kept = 0`). L0 `resnap=exact` keeps \(5/12\) of the octahedron edges under left half-units.

The Lang `_graph.json` is a Model 2 witness of the existing row, not an extension of B. Opening the book-default candidate on these sets would be a second rule in the analysis channel, not finishing B.

C is a ledger on the same L0 graph: `notes/op1_runs/20260913_L0_section_C.json`. Along occupancy is section-invariant. Slice-A 8/12 overlap is invariant. Inter *index* lifts are 3-way distinct. Left-half `inter_kept` is section-dependent (`max_real` mixed 0 or 3 of 12). B cannot see that; C did. Not a third graph.

Left-half death on L0 (not a new B matrix): `notes/op1_runs/20260912_L0_left_half_death.json`. Occupancy 4-cycles split 2+2 onto antipodes; along_kept=0 is not only `min_index`.
