# Open problems (living list)

Numbered research questions that structure the book’s unfinished edges.  
Each problem has a **home chapter** where it is introduced or attacked, a **status**, and an optional **owner** (person or workstream).

| # | Problem | Home chapter | Status | Owner |
|---|---------|--------------|--------|-------|
| 1 | Canonical quaternionic Farey structure | Ch. 3 | Open — core of Ch. 3; candidate_adjacency sandbox in `qga/lib/hopf_lattice.py` | `scripts/op1_adjacency` harness |
| 2 | Flux topograph axioms | Ch. 5 | Open — core of Ch. 5; sandbox `qga/lib/flux_topograph.py` | `scripts/op2_topograph` harness |
| 3 | Class number ↔ Magic Island correspondence | Ch. 6 | Open — sandbox `classify_topograph_type` / `class_number_analogue` | — |
| 4 | \(Z\to\) flywheel uniqueness (up to gauge) | Ch. 7 / 10 | Open — map defined in Ch. 7; uniqueness open | — |
| 5 | \(350/\pi\) first principles or falsification | Ch. 10 | Partial result — [`op5`](https://github.com/kinaar8340/op5) campaign `OP5-T4-2026-09-09` | `op5` |
| 6 | Composition of flywheels (Gauss lift) | Ch. 8 | Open — sandbox `qga/lib/composition.py` | — |

**Status vocabulary:** `Open` · `In progress` · `Partial result` · `Resolved` · `Deferred`

---

## Problem statements

### OP1 — Canonical quaternionic Farey structure
**Home:** Chapter 3  
**Status:** Open — core of Ch. 3; experimental candidate in book helper. Partial result (slice A only): \(\mathbb{Z}[i]\) neighbors on \(h(\Lambda_0)\). Classical \(\mathbb{Q}\) Farey still open.

Prove uniqueness (or classify) discrete adjacency / mediant rules on the gauged Hopf lattice that reduce to classical Farey under a fixed embedding \(\mathbb{Q}\cup\{\infty\}\hookrightarrow\) lattice/base. Without a chosen primary rule, “quaternionic Farey” remains a family of metaphors rather than a single theory.

**Sandbox:** `qga/lib/hopf_lattice.candidate_adjacency` (along-fiber phase neighbors + base angular threshold). Not claimed canonical. See Ch. 3 §3.5 and Exercise 3.H.

**Equivariance diagnostic (Ch. 4):** `adjacency_equivariance_score(points, unit, side=...)` — Exercise 4.H. Failures constrain admissible OP1 rules.

```
OP1 status: Open
Last harness: notes/op1_runs/20260911_Lang_book_default_none.json
  Model 2: notes/op1_runs/20260911_*_structure_group.json

how along_on_true_fiber: min Euclidean R^4 from q_j to left-U(1) orbit
  {e^{iφ} q_i}; Lang tol 1e-2, else 1e-3.
  Two Lsg lists, do not collapse:
    candidate E_parallel n_along=26, along_on_true_fiber=1.0
    constructed consecutive n_along=64, along_on_true_fiber=1.0

fiber census (read as geometry, not as a win):
  L0:   6 octahedron poles × 4 per fiber — Theorem (Hopf of 24-cell / Λ0).
        Model-2 along=24 is Software fact (U(1) occupancy), not 24 Farey neighbors.
        Slice A closed as ledger (not a problem bump): 8/12 Gaussian-Farey.
  Lang: 32 × 8 = 256 product sample — Software fact. Discrete fiber bundle
        + Delaunay base. Same integer as occupancy necklace, different graph.
  Lsg:  4 × 16 = 64 sampled true fibers — Software fact. Only set where
        along = structure group by construction.

frozen candidate_adjacency / book_default (Software fact, not a theorem):
  default candidate_adjacency recovers the ξ₂-circle on Λ_ang and
  mis-labels true-fiber neighbors as E_perp; Hurwitz Λ_0 has no
  along-edges and its inter-edges are same-fiber.
  Lang: n_along=256 along_kind=chart_xi2_circle_not_u1
        along_on_true_fiber=0 along_chart_only=1 inter_leaks=0.667
        (256 angle samples ≠ occupancy necklace)
  Lsg:  candidate names 26 of 64 constructed U(1) steps as E_parallel
  L0:   n_along=0 along_kind=no_along_edges; 36 inter, all d_S=0 exact

Model 2 structure_group_adjacency (not a status bump):
  Lsg:  n_along=64 along_kind=consecutive_u1_on_sampled_fibers
        along_on_true_fiber=1 inter_leaks=0; left-i/j along_kept=1
  Lang: n_along=256 along_kind=consecutive_u1_steps_on_product_sample
        8 phases × 32 bases, Delaunay base; NOT a Farey diagram
        along_on_true_fiber=1 inter_leaks=0; left-i/j along_kept=1
  L0:   n_along=24 along_kind=u1_occupancy_through_lambda0
        Software fact of how Model 2 occupied the Theorem 6×4 image
        n_inter=12 inter_leaks=0; base distances = π/2 (not zero)
        Engine replay (qga-math): L0 census + Hurwitz 24 + classical hopf_map, not the adjacency rule.

  OP1-A (ledger closed; problem stays Open):
    notes/op1_runs/20260911_L0_structure_group_farey_slice_A.json
    Partial result (slice A only): Z[i] neighbors on h(Λ0).
    Classical Q Farey still open.
    Chart: poles → {0,inf,±1,±i} ⊂ P¹(C) — Theorem.
    Dump / 8 of 12 / 4 misses / 1 extra — Software fact.
    Overlap = polar stars; misses = equatorial square {±1,±i} (norm 2);
    Farey-not-Model-2 = antipode {0,inf}. Octahedron 1-skeleton ≠ Gaussian
    Farey on the same six points. Not Q∪{∞}. Do not write that
    quaternionic Farey reduces.

  OP1-B (indexed, not extended):
    notes/op1_runs/20260911_slice_B_keep_rate.md
    Model 2 Lsg/L0 24×2 tables already in the structure_group JSON rows.
    Lang dump is a graph witness of the 20260911 row
    (notes/op1_runs/20260911_Lang_book_default_none_structure_group_graph.json).
    Claim lock: same rule as Lsg/L0; not a third adjacency; not slice A;
    not section C; 256 along is not occupancy-necklace 256. Do not
    overwrite the 20260911 Lang JSON row. candidate / open sample parked.
    Do not rerun run.py for B.

  L0 left-half death (Software fact, next to B; not full C):
    notes/op1_runs/20260912_L0_left_half_death.json
    Lipschitz 8: each occupancy 4-cycle maps to one fiber; along_kept=1.
    Left half-units (16): each 4-cycle splits 2+2 onto an antipodal pair;
    along_kept=0; inter_kept=5/12. Occupancy is not left-invariant on 2T.
    Death is not only min_index. OP1-C (other sections on the same L0
    graph): notes/op1_runs/20260913_L0_section_C.json. Claim lock: same
    graph; default remains min_index; do not fold C into slice A.
    Along invariant; 8/12 overlap invariant; inter index lifts 3-way
    distinct; left-half inter_kept section-dependent (max_real mixed).
    Not a third graph.

Use rule:
  Frozen default: candidate_adjacency — book figures, golden test.
  Analysis / flywheels / OP2 sandbox: only --rule structure_group, and
    only after the JSON row for that sample is attached.
  Do not mix the two edge sets in one topograph.
  Do not promote Model 2 into flux_hopf_lib or qga_engine until a Farey
  reduction is canonical (A is a named P¹(C) slice, not Q∪{∞}).

Public sentence: two adjacency Models; OP2 sandbox on Model 2 only;
Kirchhoff support; strict-sign separators; periodicity vacuous on L0
and gauge-unstable on Lsg height / Lang y1; slice A on L0: 8/12
Gaussian-Farey overlap; equatorial square missed; antipode extra; not Q;
equivariance matrix is a ledger, not an axiom; do not call Model 2
gauge-equivariant. OP1 Open. OP2 Open. OP3 not opened.

Problem stays Open (book wording: Q∪{∞}). Narrow partial is slice A only.
Vetoes still: no Q∪{∞} embedding; half-unit left keep-rates die;
Lang inter_kept<1. B indexed, not extended. C closed as ledger on the
same L0 graph (not a problem bump). No third graph.
```

These are Software facts of `scripts/op1_adjacency`. They do not resolve OP1.
Do not feed Lang's candidate 256 along-edges into OP2–OP6 as if they were Hopf \(E_\parallel\).

### OP2 — Flux topograph axioms
**Home:** Chapter 5  
**Status:** Open — core of Ch. 5; experimental sandbox in book helper  

Which properties of Conway topographs (separator structure, periodicity, river, values at faces/edges) survive for (a) quaternion norm forms and (b) lattice flux functionals? State a minimal axiom system such that Hatcher’s binary case is a specialization.

**Sandbox:** `qga/lib/flux_topograph.py` — `build_flux_topograph(adjacency="structure_group")`, `detect_separators`, `periodicity_score`, `separator_equivariance_score`. Depends on OP1 Model 2. See Ch. 5 §5.4 and Exercise 5.G.

```
OP2 status: Open
Skeleton: Model 2 structure_group_adjacency (not a theorem; not candidate ξ2).
Last harness: notes/op2_runs/20260911_Lsg_structure_group.json
  (also L0, Lang; each attaches the matching OP1 structure_group JSON)
  Equivariance ledger (left): notes/op2_runs/20260913_equivariance_matrix.json
  Equivariance ledger (right): notes/op2_runs/20260913_equivariance_matrix_right.json
  Not averaged.

Support: fiber_cycle_flux on U(1) occupancy cycles. Kirchhoff max|r|=0
  on Lsg, L0, Lang. Support ⊆ E_parallel ∪ E_perp of Model 2.

Separators (strict sign-crossing; zeros are not separators):
  Lsg  hopf_height: 4 / 5; left-i 4→4; left-j 4→5 (cut not gauge-invariant)
       hopf_y1: 0 → periodicity undefined_or_vacuous
  L0   hopf_height and hopf_y1: 0. Pole levels: y3 = {+1,-1,0,0,0,0};
       y1 = {0,0,+1,0,0,-1}. Zeros are levels, not crossings.
       periodicity_score(cut=strict_sign) = undefined_or_vacuous
  Lang hopf_height: 1 / 16, 1→1 under i and j — Delaunay periodicity, not Farey
       hopf_y1: 8 / 37, 8→9 on both i and j; OP1 inter_kept i=0.944 j=0.811

Φ=+1 on U(1) occupancy cycles is a flywheel seed, not a classification.
Candidate edges stay refused. Do not write axioms. Do not open OP3.
A/B/C on OP1 stay parked.

Public sentence: two adjacency Models; OP2 sandbox on Model 2 only;
Kirchhoff support; strict-sign separators; periodicity vacuous on L0
and gauge-unstable on Lsg height / Lang y1; equivariance matrix is a
ledger, not an axiom; do not call Model 2 gauge-equivariant.
Increment closed; problem Open.

Equivariance matrix (ledger increment, not an axiom; not a new graph):
  Left: notes/op2_runs/20260913_equivariance_matrix.json
  Right: notes/op2_runs/20260913_equivariance_matrix_right.json
  Claim lock: Model 2 is not gauge-equivariant. i/j not averaged.
  Left and right are sibling tables, not one mixed matrix.
  This increment does not enter OP3; the research problem OP3 remains Open
  (gate: do not enter it here). Do not write OP2 axioms from these cells.
  Lsg height moves 4→5 under left-j and under right-j (edges 5→7 on both);
  Lang y1 moves 8→9 under both left and both right units (j edges 37→38
  on both). Matching cut integers do not identify the tables. The split
  that already differs is Lang inter_kept (left 0.944/0.811 vs right
  0.811/0.833). Do not fold the two files.
  L0 periodicity stays vacuous because zeros are levels, not crossings
  (not keep-rate 1.0 — OP1 inter_kept=1 on Lipschitz i/j is a different object).
  That is the ledger. It is not invariance.
  A/B closed as ledgers; C closed as section ledger on the same L0 graph.
  Candidate refused. OP3 not entered.
```

### OP3 — Class number ↔ Magic Island
**Home:** Chapter 6  
**Status:** Open — experimental classification sandbox  

Is there a precise arithmetic invariant (class number, type number, discriminant, topological charge, …) whose magnitude or arithmetic type predicts Magic Island stability scores? Correlation is not enough; seek a structural map or a clear negative result.

**Sandbox:** `qga/lib/flux_topograph.py` — `classify_topograph_type`, `enumerate_reduced`, `class_number_analogue`, `magic_island_score`. Depends on OP1–OP2. See Ch. 6 §6.3 and Exercise 6.G.

### OP4 — \(Z\to\) flywheel uniqueness
**Home:** Chapters 7 and 10  
**Status:** Open — map implemented; uniqueness not proved  

Up to gauge equivalence, is the map from atomic number \(Z\) to flywheel configuration unique under stated axioms? If not, classify the ambiguity and its physical or chemical consequences.

**Sandbox:** `map_z_to_flywheel[_extended]`, `stability_landscape_z`. See Ch. 7 §7.3 and Exercise 7.I.

### OP5 — \(350/\pi\) first principles
**Home:** Chapter 10  
**Status:** Partial result — owner [`op5`](https://github.com/kinaar8340/op5)  
**Campaign:** `OP5-T4-2026-09-09`

Derive \(W_g = 350/\pi\) from lattice geometry / topological clock axioms, **or** falsify multi-domain recurrence as coincidence via pre-registered statistical tests (Table T4 protocol).

**Closed (this campaign, not a forever-settled law).** Two frames do not force \(W_g=350/\pi\). H1a–H1e under Table T4 fail to reject coincidence. Cite [`op5`](https://github.com/kinaar8340/op5) / [`docs/OP5_RESULT.md`](https://github.com/kinaar8340/op5/blob/main/docs/OP5_RESULT.md).

**Still open.** First-principles derivation. Door 1 (named-7 hunts) is parked. Door 2 (new T4 campaign) is idle — do not reuse H1a–H1e.

**Sandbox:** `qga/lib/validation.py` (Table T4 helpers) and the independent attack in `op5`. See Ch. 10 §10.5 and Exercise 10.B.

### OP6 — Composition of flywheels
**Home:** Chapter 8  
**Status:** Open — sandbox `qga/lib/composition.py`  

Does Gauss-style composition of forms admit a dynamical realization on paired flywheels (or on ideal classes of a quaternion order) that recovers classical composition in a suitable reduction? Require associativity up to gauge equivalence and compatibility with Ch. 4 gauge actions.

**Sandbox:** `compose_flywheels`, `composition_table`, `is_associative_up_to_equivalence`, `class_group_analogue` (Ch. 8); algebraic side in `qga/lib/quaternion_algebra.py` (Ch. 9: `QuaternionAlgebra`, `HurwitzOrder`, `left_ideal_class_set`, `two_sided_class_group`). Current flux-composition experiments often show low closure/associativity — document failures (Ch. 8 Labs 8.D–8.G). Use ideal theory (Ch. 9) to seek a rigorous law.

---

## How to update this file

1. Change **Status** when work starts or a result lands.  
2. Put initials or repo issue links in **Owner**.  
3. When resolved, add a one-line pointer to the theorem / section / notebook and leave the row for history.  
