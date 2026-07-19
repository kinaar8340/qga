# Preface

**Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics**  
*(Short name: QGA)*

**Mission.** Lift Hatcher’s visual, diagrammatic number theory from the Farey plane and binary quadratic forms to unit quaternions, the Hopf fibration, and gauged flux lattices—keeping pure geometry and arithmetic defensible, and isolating physical models and observational hypotheses so they never masquerade as theorems.

---

## Why this book exists

Allen Hatcher’s *Topology of Numbers* ([free PDF](https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf); AMS paperback, 2022) teaches elementary number theory by **drawing**. Mediants, Farey edges, continued-fraction zigzags, and Conway topographs of binary quadratic forms turn dry Diophantine statements into spatial relationships you can almost walk along. Symmetries appear as linear fractional transformations; classification appears as finite lists of reduced forms; arithmetic depth appears as class groups of quadratic forms and fields. The method is as important as the theorems: **make the integers visible**.

[Kingdom Come](https://github.com/kinaar8340/kingdom_come) is a Hopf-fibration portal—code, figures, and a Gradio laboratory—built around a different but kindred intuition. Unit quaternions form the three-sphere \(S^3\). The Hopf map \(S^3 \to S^2\) fibers that sphere into linked circles. A **gauged Hopf lattice** discretizes the geometry; **flux flywheels** are topologically protected rotating configurations on that lattice. A map from atomic number \(Z\) to flywheel metrics produces a periodic-table proxy (“Magic Islands”). Across several observational domains a numerical signature \(350/\pi \approx 111.41\) appears as a working topological clock \(W_g\). The same “draw it, rotate it, see the links” ethos that animates Hatcher’s diagrams drives the portal’s visualizers.

This book, **Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics**, is the **lift** of Hatcher’s method:

| Hatcher’s plane | This book’s stage |
|-----------------|-------------------|
| Farey diagram on the hyperbolic / rational plane | Discrete structure on \(S^3\), projected by Hopf |
| Binary quadratic forms | Quaternion norms, quaternary forms, **flux topographs** |
| \(SL(2,\mathbb{Z})\)-type symmetries | Left/right unit-quaternion multiplications; lattice gauge actions |
| Representations by forms | Representations by norms **and** the \(Z\mapsto\) flywheel map |
| Class groups of quadratic forms/fields | Ideal classes of quaternion orders and algebras |

The pure mathematics spine (Parts I–IV) aims to be defensible geometric number theory and topology. Part V states **models** and **hypotheses** about emergent physics and observational constants; those claims are labeled so they never masquerade as theorems.

## What this book is not

It is **not** a modified reprint of Hatcher’s PDF, nor a substitute for it. Hatcher remains the canonical geometric introduction to Farey geometry, topographs, and class groups of binary quadratic forms. We cite him freely, invite parallel reading, and—when a construction has a clear TN counterpart—say so explicitly (see `HATCHER_MAP.md` in the project root).

It is also **not** a claim that every numerical coincidence listed in Kingdom Come is a law of nature. Where the text says **Hypothesis**, treat it as a research prompt with an eventual validation or falsification protocol (Chapter 10).

## Companion software and figures

Interactive experiments live in the Kingdom Come repository and Hugging Face Space. Pedagogical lattice/topograph/composition/algebra/validation helpers live in this book’s `lib/` package. Static figures are under `book/figures/` (see attribution there).

| Resource | Location |
|----------|----------|
| Book manuscript (this repo) | `~/Projects/qga/` · [github.com/kinaar8340/qga](https://github.com/kinaar8340/qga) |
| Kingdom Come source / portal | `~/Projects/kingdom/` · [github.com/kinaar8340/kingdom_come](https://github.com/kinaar8340/kingdom_come) |
| Shared Hopf / quaternion core | `flux_hopf_lib` |
| Figures | `book/figures/` |
| How to run labs | [`book/HOW_TO_USE.md`](HOW_TO_USE.md) |

Module pointers at the end of each chapter name the Python entry points used in labs (`kingdom.core.*`, `lib.*`, and figure generators under `scripts/`).

## How to read

- **Pure geometry and arithmetic.** Chapters 0–9; treat Chapter 10 as optional (observations and validation).  
- **Model / portal narrative first.** Chapter 0 → Chapter 2 → Chapter 3 (lattice and flywheels) → Chapter 7 → Chapter 10.  
- **Coming from Hatcher.** Keep TN open beside this book; use root `HATCHER_MAP.md` as a parallel syllabus.  
- **Coming from the Gradio app.** The Preview chapter is the “Home + Hopf Visualizer + Flux Flywheel” tour in prose; see also `HOW_TO_USE.md`.  
- **Open problems.** Living list in `notes/open_problems.md` (OP1–OP6).

Claim labels used throughout (see also `HOW_TO_USE.md`):

| Label | Meaning |
|-------|---------|
| **Theorem** | Proved here or classical |
| **Model** | Consistent mathematical or physical construction, not claimed as nature’s unique law |
| **Hypothesis** | Observational claim needing validation or falsification (Chapter 10 / Table T4) |
| **Software fact** | True of the current code or portal implementation |

## Acknowledgments

Allen Hatcher’s freely available *Topology of Numbers* made geometric elementary number theory a shared public good; this project stands on that invitation to *see* number theory. The Kingdom Come codebase and observation program (Hopf visualizers, lattice simulations, flux flywheel element maps, Magic Island sweeps, and multi-domain \(350/\pi\) investigations) supply the computational and visual backbone of the lift.

---

*Manuscript · Preface · Full draft (Parts I–V through Chapter 10). Figures: `book/figures/`.*
