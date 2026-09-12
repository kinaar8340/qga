# OP1-B keep-rate index

Claim: **Software fact**. `slice_status`: **B indexed, not extended**. OP1 stays **Open**.

Not a new experiment. Do not rerun `scripts/op1_adjacency/run.py` for this file. The 24×2 tables on Lsg and L0 **are** B for Model 2.

```text
Model 2 Lsg → notes/op1_runs/20260911_Lsg_book_default_none_structure_group.json  (24×2)
Model 2 L0  → notes/op1_runs/20260911_L0_book_default_exact_structure_group.json (24×2)
Lang / candidate / open sample → parked
```

Sides are not averaged. Lipschitz 8 \(\{\pm1,\pm i,\pm j,\pm k\}\): `along_kept = inter_kept = 1` on L and R, both attached sets. All 16 half-units: **right** stays 1; **left** dies (`along_kept = 0`). L0 `resnap=exact` keeps \(5/12\) of the octahedron edges under left half-units.

Opening Lang or the book-default candidate on the same three sets would be a third graph / a second rule in the analysis channel, not finishing B.

C (section sensitivity of Delaunay + `min_index` vs two other sections on the same L0 graph) can change `inter` and the 8/12 overlap. B cannot.

Left-half death on L0 (not a new B matrix): `notes/op1_runs/20260912_L0_left_half_death.json`. Occupancy 4-cycles split 2+2 onto antipodes; along_kept=0 is not only `min_index`. Full C still parked.
