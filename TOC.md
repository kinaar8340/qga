# Table of Contents

# Kingdom Come  
## A Quaternionic Geometric Approach to Number Theory and Physics

**Short name:** QGA  
**Subtitle:** Extending Allen Hatcher’s visual number theory via quaternions and the Hopf fibration

*Parts I–IV: defensible geometric number theory and topology.  
Part V: Models and Hypotheses, isolated from the theorem spine.*

---

### Front matter

- Title page  
- Dedication  
- Epigraph  
- **Preface** *(Phase 1 draft — polished)*  
  - Mission statement  
  - Why geometric number theory (Hatcher) meets Hopf topology (Kingdom Come)  
  - Framing table: Hatcher’s plane vs this book’s stage  
  - What this book is not; claim labels (Theorem / Model / Hypothesis)  
  - Companion software and figures  
  - How to read (multiple audiences)  
  - Acknowledgments  

- **How to Use the Figures and Code** *(to expand)*  
  - Notation conventions  
  - Gradio / module pointer map  
  - Claim-label discipline  

---

### Chapter 0 — A Preview

*(Phase 1 draft — ready for minor figure/caption polish only)*

0.1 From Pythagorean triples to sums of two squares  
0.2 Four squares and the birth of quaternions  
0.3 Circles and spheres as number-theoretic objects: \(S^1\), \(S^2\), unit quaternions \(S^3\)  
0.4 The Hopf fibration as a higher-dimensional Farey analogue (**Model**; discretized in Ch. 3)  
0.5 First sight of the gauged Hopf lattice and flux flywheels  
0.6 A first \(Z\mapsto\) flux sketch and the \(350/\pi\) signature (**Hypothesis**)  
0.7 Visual roadmap: Hatcher diagrams meet Hopf and Gradio simulations  
0.8 Reading plan for the rest of the book  
  Exercises 0.A–0.E · Code and asset pointers  

---

### Part I — Foundations

### Chapter 1 — Quaternions: Algebra, Geometry, and Arithmetic

*(Phase 2 draft complete)*

1.1 Definition and basic operations (\(i^2=j^2=k^2=ijk=-1\))  
1.2 Conjugation and the multiplicative norm \(N(q)=q\overline{q}\)  
1.3 Unit quaternions and the identification \(S^3\subset\mathbb{H}\cong\mathbb{R}^4\)  
1.4 Integer quaternions: Lipschitz order vs Hurwitz order  
1.5 The four-square theorem via norms (**Theorem**, classical)  
1.6 Quaternions as rotations: \(\mathrm{Spin}(3)\to SO(3)\)  
1.7 First computational labs (`kingdom.core.quaternion`)  
  Exercises 1.A–1.J · Code and asset pointers · Forward link to Ch. 2  


### Chapter 2 — The Hopf Fibration

*(Phase 2 draft complete — rebuilds Figs. 0.1–0.3)*

2.1 Definition of the Hopf fibration (complex-pair and real four-vector forms)  
2.2 Fibers and linking (Hopf invariant \(=1\))  
2.3 Stereographic projections and visualizations  
2.4 Bundle structure and charts  
2.5 Connection to quaternions and rotations  
2.6 First computational labs (`kingdom.core.hopf`, Gradio Hopf Visualizer)  
  Exercises 2.A–2.I · Code and asset pointers · Forward link to Ch. 3 (Farey lift)  


---

### Part II — The Gauged Hopf Lattice (The Farey Lift)

### Chapter 3 — Construction of the Gauged Hopf Lattice

*(Phase 3 draft complete — centers Open Problem 1)*

3.1 The Hurwitz lattice inside \(S^3\) (units + density levels)  
3.2 The gauged Hopf lattice (projection, adjacency, mediants — **Model**)  
3.3 Gauge actions: left and right multiplications  
3.4 Flux configurations and flywheels (first introduction)  
3.5 **Open Problem 1** — Canonical quaternionic Farey structure  
3.6 Software map and computational labs (`qga/lib/hopf_lattice`, `TwoGyroLattice`)  
  Exercises 3.A–3.I · Forward link to Ch. 4  


### Chapter 4 — Symmetries of the Gauged Hopf Lattice

*(Phase 3 draft complete — finishes Part II symmetry half)*

4.1 Left and right multiplications as gauge symmetries  
4.2 Comparison with Hatcher’s linear fractional transformations  
4.3 Periodic orbits and glide-like symmetries  
4.4 Symmetries acting on flux configurations and flywheels  
4.5 First computational labs  
  Exercises 4.A–4.I · OP1 equivariance tests · Forward link to Ch. 5  


---

### Part III — Forms, Topographs, and Representations

### Chapter 5 — Quaternionic Forms and Flux Topographs

*(Phase 4 draft complete — centers Open Problem 2)*

5.1 From binary quadratic forms to flux functionals  
5.2 Flux topographs and separator structures  
5.3 Periodicity, reduced configurations, and Magic Islands  
5.4 Gauge equivariance of flux topographs  
5.5 First computational labs  
  **Open Problem 2** — Flux topograph axioms  
  Exercises 5.A–5.I · Forward link to Ch. 6  


### Chapter 6 — Classification of Flux Topographs and Magic Islands

*(Phase 4 draft complete — centers Open Problem 3)*

6.1 The four types of flux topographs  
6.2 Equivalence of flux topographs  
6.3 Magic Islands as higher-dimensional class-number phenomena  
6.4 First computational labs  
  **Open Problem 3** — Class number ↔ Magic Island invariants  
  Exercises 6.A–6.I · Forward link to Ch. 7  


### Chapter 7 — The \(Z\mapsto\) Flux Map and Representation Theory

*(Phase 5 draft complete — completes Part III representation arc)*

7.1 The \(Z\mapsto\) flux map (`map_z_to_flywheel[_extended]`)  
7.2 Representation theory on the gauged Hopf lattice  
7.3 Magic Islands and real chemical stability  
7.4 Electron clouds as flux distributions  
7.5 First computational labs  
  **Open Problem 4** — \(Z\to\) flywheel uniqueness (shared with Ch. 10)  
  Exercises 7.A–7.I · Forward link to Ch. 8  


---

### Part IV — Arithmetic Depth (Class Groups and Algebras)

### Chapter 8 — Composition and Class Groups in the Quaternionic Setting

*(Phase 6 draft complete — centers Open Problem 6)*

8.1 Gauss composition — classical reminder  
8.2 Lifting composition to flux configurations and flywheels  
8.3 Class-group analogues  
8.4 First computational labs  
  **Open Problem 6** — Composition of flywheels / Gauss lift  
  Exercises 8.A–8.I · Forward link to Ch. 9  


### Chapter 9 — Quaternion Algebras and Ideal Theory

*(Phase 7 draft complete — algebraic foundation for OP6)*

9.1 Quaternion algebras over \(\mathbb{Q}\) (ramification)  
9.2 Orders: Lipschitz, Hurwitz, maximal  
9.3 Ideal theory and class groups  
9.4 From ideals to flux topographs / flywheels (**Model** bridge)  
9.5 First computational labs  
  **Open Problem 6** continued · Exercises 9.A–9.I · Forward link to Ch. 10  


---

### Part V — Observations and Models

### Chapter 10 — Observations, Hypotheses, and Validation Protocols

*Throughout: claim types labeled **Theorem**, **Model**, or **Hypothesis**.*

10.1 The \(350/\pi\) signature across domains (full accounting)  
10.2 QVPIC, cuprate sketches, pulsar timing, Bitcoin Pi Cycle, TLS bursts  
10.3 Statistical validation checklist and falsification criteria  
10.4 Cosmological and emergent-physics language (scope and non-claims)  
10.5 Interactive companion: Hopf visualizer, lattice simulator, flux flywheel slider  
10.6 Research program: confirm / refine / falsify  
  **Open Problem 5** — \(350/\pi\) first principles  
  **Open Problem 4** — \(Z\to\) flywheel uniqueness  

---

### Appendix / Back Matter

**A** Nonstandard terminology  
 flux flywheel · gauged Hopf lattice · QVPIC · Magic Island · porous vacuum · separator surface · …

**B** Notation sheet  

**C** Background refresher: Farey diagram and Conway topograph (pointer to Hatcher; minimal recap)  

**D** Proof sketches: four-square theorem; Hurwitz Euclidean algorithm  

**E** Figure atlas and notebook index  

**F** Data provenance for observational tables  

**Open Problems** — living list with status tracking (`notes/open_problems.md`)  

**HATCHER_MAP** — chapter-by-chapter parallel reading guide (`HATCHER_MAP.md`)  

**Tables**  
 T1 Stability metrics for \(Z = 1\) to \(118+\)  
 T2 Magic Island parameter ranges  
 T3 Periodic separator / topograph data  
 T4 \(350/\pi\) observational correlations (source, method, confidence)  
 T5 Hatcher ↔ QGA concept dictionary  
 T6 Software module index  

**Bibliography**  
**Index of names / symbols / subjects**  
**Figure attributions** (`book/figures/ATTRIBUTION.md`)  

---

## Architecture at a glance

| Part | Chapters | Hatcher analogue | Role |
|------|----------|------------------|------|
| Preview | 0 | Ch. 0 | Motivation and map |
| **I** Foundations | 1–2 | *(new floor)* | Quaternions + Hopf |
| **II** Farey lift | 3–4 | Ch. 1–3 | Lattice + symmetries |
| **III** Forms & reps | 5–7 | Ch. 4–6 | Topographs, Magic Islands, \(Z\)-map |
| **IV** Arithmetic depth | 8–9 | Ch. 7–8 | Class groups + algebras |
| **V** Observations | 10 | *(new floor)* | Hypotheses + validation |

### Open problems → home chapters

| # | Problem | Home |
|---|---------|------|
| 1 | Canonical quaternionic Farey structure | Ch. 3 |
| 2 | Flux topograph axioms | Ch. 5 |
| 3 | Class number ↔ Magic Island | Ch. 6 |
| 4 | \(Z\to\) flywheel uniqueness | Ch. 7 / 10 |
| 5 | \(350/\pi\) first principles | Ch. 10 |
| 6 | Composition of flywheels | Ch. 8 |

---

*Canonical title:* **Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics**  
*Short name:* **QGA**
