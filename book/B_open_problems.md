# Appendix B — Open Problems (Extended)

Living research edges of the project. The main text (especially Chapters 3, 5–10) states each problem briefly; this appendix keeps the full statements, sandboxes, and status tracking.

**Status vocabulary:** `Open` · `In progress` · `Partial result` · `Resolved` · `Deferred`

---

## B.1 Status table

| # | Problem | Home | Status | Sandbox |
|---|---------|------|--------|---------|
| OP1 | Canonical quaternionic Farey structure | Ch. 3 | Open | `lib.hopf_lattice.candidate_adjacency` |
| OP2 | Flux topograph axioms | Ch. 5 | Open | `lib.flux_topograph` |
| OP3 | Class number ↔ Magic Island | Ch. 6 | Open | `classify_topograph_type`, `class_number_analogue` |
| OP4 | \(Z\to\) flywheel uniqueness | Ch. 7 / 10 | Open | `map_z_to_flywheel`, `stability_landscape_z` |
| OP5 | \(350/\pi\) first principles or falsification | Ch. 10 | Open | `lib.validation` · Table T4 (Appendix D) |
| OP6 | Composition of flywheels (Gauss lift) | Ch. 8–9 | Open | `lib.composition` · `lib.quaternion_algebra` |

---

## B.2 Problem statements

### OP1 — Canonical quaternionic Farey structure

**Home:** Chapter 3  

Prove uniqueness (or classify) discrete adjacency / mediant rules on the gauged Hopf lattice that reduce to classical Farey under a fixed embedding \(\mathbb{Q}\cup\{\infty\}\hookrightarrow\) lattice/base. Without a chosen primary rule, “quaternionic Farey” remains a family of metaphors rather than a single theory.

**Sandbox:** `candidate_adjacency` (along-fiber phase neighbors + base angular threshold). Not claimed canonical.  
**Diagnostics:** `adjacency_equivariance_score` (Ch. 4, Exercise 4.H).  
**Success criteria:** equivariant rule + documented Farey reduction + comparable mediant algorithm.

### OP2 — Flux topograph axioms

**Home:** Chapter 5  

Which properties of Conway topographs (separator structure, periodicity, river, face/edge values) survive for (a) quaternion norm forms and (b) lattice flux functionals? State a minimal axiom system such that Hatcher’s binary case is a specialization.

**Sandbox:** `build_flux_topograph`, `detect_separators`, `periodicity_score`, `separator_equivariance_score`. Depends on OP1.  
**Success criteria:** axioms + proof or counterexample of reduction to TN Ch. 4.

### OP3 — Class number ↔ Magic Island

**Home:** Chapter 6  

Is there a precise arithmetic invariant (class number, type number, discriminant, topological charge, …) whose magnitude or type predicts Magic Island stability scores? Correlation is not enough; seek a structural map or a clear negative result.

**Sandbox:** `classify_topograph_type`, `enumerate_reduced`, `class_number_analogue`, `magic_island_score`. Depends on OP1–OP2.  
**Success criteria:** invariant with out-of-sample predictive power or rigorous non-existence under stated axioms.

### OP4 — \(Z\to\) flywheel uniqueness

**Home:** Chapters 7 and 10  

Up to gauge equivalence, is the map from atomic number \(Z\) to flywheel configuration unique under stated axioms? If not, classify the ambiguity and its chemical consequences.

**Sandbox:** `map_z_to_flywheel[_extended]`, `stability_landscape_z`.  
**Success criteria:** uniqueness theorem up to gauge, or explicit moduli of ambiguity.

### OP5 — \(350/\pi\) first principles or falsification

**Home:** Chapter 10  

Derive \(W_g = 350/\pi\) from lattice geometry / topological clock axioms, **or** falsify multi-domain recurrence as coincidence via pre-registered statistical tests (Table T4, Appendix D).

**Sandbox:** `table_t4_checklist`, `default_hypotheses`, `run_table_t4_demo`, `combine_p_values_fisher`, `proximity_to_wg`.  
**Success criteria:** derivation paper, or registered negative result with full T4 compliance.

### OP6 — Composition of flywheels (Gauss lift)

**Home:** Chapters 8–9  

Does Gauss-style composition admit a dynamical or ideal-theoretic realization on flywheels / flux classes that is associative up to gauge equivalence, compatible with Ch. 4 actions, and reduces to classical composition under restriction?

**Sandbox:** `compose_flywheels`, `composition_table`, `is_associative_up_to_equivalence`, `class_group_analogue`; algebraic side `QuaternionAlgebra`, `HurwitzOrder`, `left_ideal_class_group`.  
**Current note:** flux-composition experiments often show **low closure and low associativity** — document failures as progress.  
**Success criteria:** associative group law on classes + comparison with Hurwitz / other orders.

---

## B.3 How to update

1. Change **Status** when work starts or a result lands.  
2. Put initials or issue links in an Owner column (optional).  
3. When resolved, add a one-line pointer to the theorem / section / notebook and keep the row for history.  
4. Keep `notes/open_problems.md` in sync with this appendix (or treat this appendix as the print form of that file).

---

## B.4 Dependency sketch

```text
OP1 (adjacency)
  └─► OP2 (topographs)
        └─► OP3 (class number / islands)
              ├─► OP4 (Z-map uniqueness)
              └─► OP6 (composition) ◄── Ch. 9 ideal theory
OP5 (350/π) ── independent empirical track, informed by geometry
```

---

*Manuscript · Appendix B · Open Problems (Extended).*
