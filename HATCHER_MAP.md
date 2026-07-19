# Hatcher *Topology of Numbers* ↔ Kingdom Come / QGA

Parallel reading map. Left column follows Hatcher’s free PDF TOC  
(https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf).  
Right column is the **lift** developed in this book and in  
https://github.com/kinaar8340/kingdom_come.

| Hatcher TN | QGA (part · chapter) | Conceptual lift |
|------------|----------------------|-----------------|
| Ch. 0 Preview | Preview · **Ch. 0** | Pythagorean → two squares → **four squares / quaternions**; Farey → **Hopf**; first **flux flywheel** and **350/π** glimpse |
| *(no TN counterpart)* | **Part I** · Ch. 1 Quaternions; Ch. 2 Hopf *(drafts complete)* | Foundations missing from TN |
| Ch. 1 Farey diagram (mediants, Farey series) | **Part II** · Ch. 3 Gauged Hopf lattice | Rational points / mediants on lattice projected by Hopf; **OP1** |
| Ch. 2 Continued fractions | Part II · Ch. 3–4 (paths & phase) | Zigzag CF paths → phase winding; lattice walks |
| Ch. 3 Symmetries of the Farey diagram | Part II · Ch. 4 Symmetries *(draft complete)* | Unit quaternion multiplications; gauge actions; LFT comparison; OP1 equivariance tests |
| Ch. 4 Quadratic forms (topograph, periodicity, Pell) | **Part III** · Ch. 5 Forms & flux topographs *(draft complete)* | Norm forms; flux topographs; **OP2** |
| Ch. 5 Classification of quadratic forms | Part III · Ch. 6 Classification & Magic Islands *(draft complete)* | Reduced configs; stability regions; **OP3** |
| Ch. 6 Representations by quadratic forms | Part III · Ch. 7 \(Z\mapsto\) flux map *(draft complete)* | Norms vs flux configs; `map_z_to_flywheel`; **OP4** |
| Ch. 7 Class group for quadratic forms | **Part IV** · Ch. 8 Composition & class groups *(draft complete)* | Gauss lift; ideal classes; **OP6** |
| Ch. 8 Quadratic fields | Part IV · Ch. 9 Quaternion algebras *(draft complete)* | Hurwitz; form↔ideal; lattice back-applications; **OP6** algebraic side |
| *(no TN counterpart; arithmetic labeling on geometric orbits)* | Part IV · **Ch. 9 §9.5** modulus invariants | Separate **algebraic** \(\times 2\) cycles on \(\mathbb{Z}/m\mathbb{Z}\), **sequential label progression**, and **angle–label lock** (exNMI); control via `angle_bin`; supporting stack `vortex_math` · note `notes/RESEARCH_NOTE_moduli.md` |
| Ch. 5 Classification (invariants / reduced classes) | Part III · Ch. 6 *(cross-ref to §9.5)* | Same discipline: name the invariant (class number analogue ≠ positional lock) |
| *(applications layer)* | **Part V** · Ch. 10 Observations & validation *(draft complete)* | \(350/\pi\), Z-map, Magic Islands, Table T4; **OP5** |

## Structural choice

Hatcher opens with Farey geometry *before* forms. QGA inserts **Ch. 1–2 (quaternions + Hopf)** first so the Farey lift in Ch. 3 is readable. Readers who already know \(S^3\) and Hopf can skim to Ch. 3.

## What is deliberately *not* a 1:1 copy

- No reuse of Hatcher’s prose, figures, or exercise sets.  
- Mediant / Farey generalization is **defined** for the gauged Hopf lattice, not assumed unique.  
- Physics and observational chapters are **extra floors**, not claimed theorems of TN.

## Code anchors (Kingdom Come)

| Idea | Typical module |
|------|----------------|
| Quaternion algebra | `kingdom.core.quaternion` |
| Hopf map & fibers | `kingdom.core.hopf` |
| Gauged lattice | `kingdom.core.lattice` |
| Flux flywheel / Z map | `kingdom.core.flux_flywheel` |
| Elements / stability | `kingdom.core.elements` |
| Magic Island viz | `kingdom.viz.magic_island` |
| Electron clouds | `kingdom.viz.electron_cloud` |
| Constants (e.g. 350/π) | `kingdom.core.constants` |
