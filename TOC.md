# Table of Contents

# Kingdom Come  
## A Quaternionic Geometric Approach to Number Theory and Physics

**Short name:** QGA  
**Subtitle:** Extending Allen Hatcher’s visual number theory via quaternions and the Hopf fibration  
**Status:** Full manuscript draft complete (Parts I–V · Chapters 0–10)  
**Remote:** https://github.com/kinaar8340/qga

*Parts I–IV: geometric number theory and topology (with labeled Models).  
Part V: Models and Hypotheses, isolated from the theorem spine.*

---

### Front matter

- Title page · Dedication · Epigraph  
- **Preface**  
  - Mission statement  
  - Why geometric number theory (Hatcher) meets Hopf topology (Kingdom Come)  
  - Framing table: Hatcher’s plane vs this book’s stage  
  - What this book is not; claim labels  
  - Companion software and figures  
  - How to read  
  - Acknowledgments  

- **How to Use the Figures and Code** → [`book/HOW_TO_USE.md`](book/HOW_TO_USE.md)  
  - Claim labels (Theorem / Model / Hypothesis / Software fact)  
  - Repo layout and lab setup  
  - API honesty notes  
  - Gradio ↔ chapter map · Hatcher parallel reading  

---

### Chapter 0 — A Preview

0.1 From Pythagorean triples to sums of two squares  
0.2 Four squares and the birth of quaternions  
0.3 Circles and spheres as number-theoretic objects  
0.4 The Hopf fibration as a higher-dimensional Farey analogue (**Model**; discretized in Ch. 3)  
0.5 First sight of the gauged Hopf lattice and flux flywheels  
0.6 A first \(Z\mapsto\) flux sketch and the \(350/\pi\) signature (**Hypothesis**)  
0.7 Visual roadmap: Hatcher diagrams meet Hopf and Gradio  
0.8 Reading plan for the rest of the book  
  Exercises 0.A–0.E  

---

### Part I — Foundations

### Chapter 1 — Quaternions: Algebra, Geometry, and Arithmetic

1.1 Definition and basic operations  
1.2 Conjugation and the multiplicative norm  
1.3 Unit quaternions and \(S^3\subset\mathbb{H}\)  
1.4 Lipschitz vs Hurwitz orders  
1.5 Four-square theorem via norms (**Theorem**)  
1.6 Double cover \(\mathrm{Spin}(3)\to SO(3)\)  
1.7 Computational labs  
  Exercises 1.A–1.J  

### Chapter 2 — The Hopf Fibration

2.1 Definition (complex-pair and real four-vector forms)  
2.2 Fibers and linking (Hopf invariant \(=1\))  
2.3 Stereographic projections and visualizations  
2.4 Bundle structure and charts  
2.5 Connection to quaternions and rotations  
2.6 Computational labs  
  Exercises 2.A–2.I · Forward to Ch. 3  

---

### Part II — The Gauged Hopf Lattice (The Farey Lift)

### Chapter 3 — Construction of the Gauged Hopf Lattice

3.1 Hurwitz lattice inside \(S^3\)  
3.2 Gauged Hopf lattice (projection, adjacency — **Model**)  
3.3 Gauge actions: left and right multiplications  
3.4 Flux configurations and flywheels  
3.5 **Open Problem 1** — Canonical quaternionic Farey structure  
3.6 Software map and labs (`lib/hopf_lattice`, `TwoGyroLattice`)  
  Exercises 3.A–3.I  

### Chapter 4 — Symmetries of the Gauged Hopf Lattice

4.1 Left and right multiplications as gauge symmetries  
4.2 Comparison with Hatcher’s linear fractional transformations  
4.3 Periodic orbits and glide-like symmetries  
4.4 Symmetries on flux configurations and flywheels  
4.5 Computational labs  
  Exercises 4.A–4.I · OP1 equivariance  

---

### Part III — Forms, Topographs, and Representations

### Chapter 5 — Quaternionic Forms and Flux Topographs

5.1 From binary quadratic forms to flux functionals  
5.2 Flux topographs and separator structures  
5.3 Periodicity, reduced configurations, and Magic Islands  
5.4 Gauge equivariance · **Open Problem 2**  
5.5 Computational labs  
  Exercises 5.A–5.I  

### Chapter 6 — Classification of Flux Topographs and Magic Islands

6.1 Four types of flux topographs  
6.2 Equivalence of flux topographs  
6.3 Magic Islands as class-number phenomena · **Open Problem 3**  
6.4 Computational labs  
  Exercises 6.A–6.I  

### Chapter 7 — The \(Z\mapsto\) Flux Map and Representation Theory

7.1 The \(Z\mapsto\) flux map  
7.2 Representation theory on the gauged Hopf lattice  
7.3 Magic Islands and chemical stability  
7.4 Electron clouds as flux distributions  
7.5 Computational labs · **Open Problem 4**  
  Exercises 7.A–7.I  

---

### Part IV — Arithmetic Depth (Class Groups and Algebras)

### Chapter 8 — Composition and Class Groups in the Quaternionic Setting

8.1 Gauss composition — classical reminder  
8.2 Lifting composition to flux configurations · **Open Problem 6**  
8.3 Class-group analogues  
8.4 Computational labs  
  Exercises 8.A–8.I  

### Chapter 9 — Quaternion Algebras and Ideal Theory

9.1 Quaternion algebras over \(\mathbb{Q}\)  
9.2 Orders: Lipschitz, Hurwitz, maximal  
9.3 Ideal theory and class groups  
9.4 Ideals ↔ flywheels (**Model** bridge) · OP6 continued  
9.5 Modulus, invariants, and angle–label locking (**Model** · supporting stack `vortex_math`)  
9.6 Computational labs  
  Exercises 9.A–9.K  
  Research note: [`notes/RESEARCH_NOTE_moduli.md`](notes/RESEARCH_NOTE_moduli.md) · Fig. 9.5

---

### Part V — Observations and Models

### Chapter 10 — Observations, Hypotheses, and Validation

10.1 Major observational signatures (\(350/\pi\))  
10.2 The \(Z\mapsto\) map — current status  
10.3 Magic Islands and chemical/nuclear specialness  
10.4 Summary of Open Problems OP1–OP6  
10.5 Validation protocols (**Table T4**) · **Open Problem 5**  
10.6 Summary of the entire construction  
10.7 Outlook and invitation  
  Exercises 10.A–10.F · Closing  

---

### Appendices

| App | File | Content |
|-----|------|---------|
| **A** | `book/A_terminology_notation.md` | Terminology and notation |
| **B** | `book/B_open_problems.md` | Open Problems OP1–OP6 (full) |
| **C** | `book/C_lab_code_reference.md` | Laboratory code reference |
| **D** | `book/D_validation_t4.md` | Table T4 validation protocols (full) |
| **E** | `book/E_figure_atlas.md` | Figure atlas |
| **F** | `book/F_hatcher_dictionary.md` | Hatcher parallel dictionary |

Also: `notes/open_problems.md` (dev tracking) · `HATCHER_MAP.md` · `book/FIGURES.md` · bibliography seed in LaTeX back matter.  

---

## Architecture at a glance

| Part | Chapters | Hatcher analogue | Role |
|------|----------|------------------|------|
| Preview | 0 | Ch. 0 | Motivation |
| **I** Foundations | 1–2 | *(new)* | Quaternions + Hopf |
| **II** Farey lift | 3–4 | Ch. 1–3 | Lattice + symmetries |
| **III** Forms & reps | 5–7 | Ch. 4–6 | Topographs, islands, \(Z\)-map |
| **IV** Arithmetic | 8–9 | Ch. 7–8 | Composition + quaternion ideals |
| **V** Observations | 10 | *(new)* | Hypotheses + Table T4 |

### Open problems → home chapters

| # | Problem | Home |
|---|---------|------|
| 1 | Canonical quaternionic Farey structure | Ch. 3 |
| 2 | Flux topograph axioms | Ch. 5 |
| 3 | Class number ↔ Magic Island | Ch. 6 |
| 4 | \(Z\to\) flywheel uniqueness | Ch. 7 / 10 |
| 5 | \(350/\pi\) first principles or falsification | Ch. 10 |
| 6 | Composition of flywheels (Gauss lift) | Ch. 8–9 |

---

*Canonical title:* **Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics**
