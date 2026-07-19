# Open problems (living list)

Numbered research questions that structure the book’s unfinished edges.  
Each problem has a **home chapter** where it is introduced or attacked, a **status**, and an optional **owner** (person or workstream).

| # | Problem | Home chapter | Status | Owner |
|---|---------|--------------|--------|-------|
| 1 | Canonical quaternionic Farey structure | Ch. 3 | Open — core of Ch. 3; candidate_adjacency sandbox in `qga/lib/hopf_lattice.py` | — |
| 2 | Flux topograph axioms | Ch. 5 | Open — core of Ch. 5; sandbox `qga/lib/flux_topograph.py` | — |
| 3 | Class number ↔ Magic Island correspondence | Ch. 6 | Open — sandbox `classify_topograph_type` / `class_number_analogue` | — |
| 4 | \(Z\to\) flywheel uniqueness (up to gauge) | Ch. 7 / 10 | Open — map defined in Ch. 7; uniqueness open | — |
| 5 | \(350/\pi\) first principles or falsification | Ch. 10 | Open — hypothesis layer | — |
| 6 | Composition of flywheels (Gauss lift) | Ch. 8 | Open | — |

**Status vocabulary:** `Open` · `In progress` · `Partial result` · `Resolved` · `Deferred`

---

## Problem statements

### OP1 — Canonical quaternionic Farey structure
**Home:** Chapter 3  
**Status:** Open — core of Ch. 3; experimental candidate in book helper  

Prove uniqueness (or classify) discrete adjacency / mediant rules on the gauged Hopf lattice that reduce to classical Farey under a fixed embedding \(\mathbb{Q}\cup\{\infty\}\hookrightarrow\) lattice/base. Without a chosen primary rule, “quaternionic Farey” remains a family of metaphors rather than a single theory.

**Sandbox:** `qga/lib/hopf_lattice.candidate_adjacency` (along-fiber phase neighbors + base angular threshold). Not claimed canonical. See Ch. 3 §3.5 and Exercise 3.H.

**Equivariance diagnostic (Ch. 4):** `adjacency_equivariance_score(points, unit, side=...)` — Exercise 4.H. Failures constrain admissible OP1 rules.

### OP2 — Flux topograph axioms
**Home:** Chapter 5  
**Status:** Open — core of Ch. 5; experimental sandbox in book helper  

Which properties of Conway topographs (separator structure, periodicity, river, values at faces/edges) survive for (a) quaternion norm forms and (b) lattice flux functionals? State a minimal axiom system such that Hatcher’s binary case is a specialization.

**Sandbox:** `qga/lib/flux_topograph.py` — `build_flux_topograph`, `detect_separators`, `periodicity_score`, `separator_equivariance_score`. Depends on OP1 adjacency. See Ch. 5 §5.4 and Exercise 5.G.

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
**Status:** Open — hypothesis layer  

Derive \(W_g = 350/\pi\) from lattice geometry / topological clock axioms, **or** falsify multi-domain recurrence as coincidence via pre-registered statistical tests (Table T4 protocol).

### OP6 — Composition of flywheels
**Home:** Chapter 8  
**Status:** Open  

Does Gauss-style composition of forms admit a dynamical realization on paired flywheels (or on ideal classes of a quaternion order) that recovers classical composition in a suitable reduction?

---

## How to update this file

1. Change **Status** when work starts or a result lands.  
2. Put initials or repo issue links in **Owner**.  
3. When resolved, add a one-line pointer to the theorem / section / notebook and leave the row for history.  
