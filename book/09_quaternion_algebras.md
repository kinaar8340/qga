# Chapter 9 — Quaternion Algebras and Ideal Theory

This chapter supplies the rigorous algebraic foundation for the class-group analogues and composition laws of Chapter 8. We introduce quaternion algebras over \(\mathbb{Q}\), their orders (especially the Hurwitz order), and the ideal theory that turns equivalence classes of ideals into a group. This framework is the natural home for making the Model constructions of previous chapters more arithmetic and for attacking Open Problem 6 with algebraic tools.

**Learning goals**

1. Define quaternion algebras over \(\mathbb{Q}\) and understand ramification.  
2. Work with orders (Lipschitz, Hurwitz, maximal) and their ideal theory.  
3. See how ideal classes form a group and how this relates to the class-group analogues of Chapter 8.  
4. Connect ideal theory back to composition of forms / flywheels and to Magic Islands (**Model** dictionary).  
5. Prepare algebraic language for rigorous uniqueness and composition statements (OP6 and beyond).

**Figures in this chapter**

| Tag | File | Role |
|-----|------|------|
| Fig. 9.1 | `figures/fig9_1_quaternion_algebra.png` | Quaternion algebra ramification diagram |
| Fig. 9.2 | `figures/fig9_2_hurwitz_order.png` | Hurwitz order units / comparison |
| Fig. 9.3 | `figures/fig9_3_ideal_class_group.png` | Ideal class group schematic |
| Fig. 9.4 | `figures/fig9_4_ideal_to_flywheel.png` | Ideal class → flywheel (Model bridge) |
| Aux A9.1 | `figures/aux9_1_ramification_table.png` | Hilbert-symbol ramification table |

**Claim discipline**

| Claim | Type |
|-------|------|
| Quaternion algebras, Hilbert symbols, Hurwitz Euclidean property, Hurwitz class number 1 | **Theorem** (classical) |
| Dictionary between ideal classes and flux topographs / Magic Islands | **Model** |
| `qga/lib/quaternion_algebra.py` helpers (including toy class-number reports) | **Software fact** |

---

## 9.1 Quaternion algebras over \(\mathbb{Q}\)

A **quaternion algebra** over \(\mathbb{Q}\) is a 4-dimensional central simple algebra over \(\mathbb{Q}\). Up to isomorphism, each is given by square-free integers \(a,b\neq 0\) via
\[
\Bigl(\frac{a,b}{\mathbb{Q}}\Bigr)
=
\mathbb{Q}+\mathbb{Q}i+\mathbb{Q}j+\mathbb{Q}ij,
\qquad
i^2=a,\; j^2=b,\; ij=-ji.
\]
The Hamilton algebra corresponds (over \(\mathbb{R}\)) to \(a=b=-1\); as an algebra over \(\mathbb{Q}\) one studies \(\bigl(\frac{-1,-1}{\mathbb{Q}}\bigr)\).

### Ramification

At each place \(p\) (finite prime or \(\infty\)), the local Hilbert symbol \((a,b)_p\in\{\pm 1\}\) detects whether the algebra is a division algebra (\(-1\), **ramified**) or isomorphic to \(M_2\) (**split**). The set of ramified places is finite and of even cardinality; it classifies the algebra.

```text
QuaternionAlgebra(a, b)
  .ramified_places()
  .is_definite()          # True iff ramified at ∞
  .hilbert_at(p)
```

![Figure 9.1 — Ramification of a quaternion algebra.](figures/fig9_1_quaternion_algebra.png)

*Figure 9.1.* Example \(\bigl(\frac{-1,-1}{\mathbb{Q}}\bigr)\): ramified at \(2\) and \(\infty\) (definite over \(\mathbb{R}\)).

![Auxiliary Figure A9.1 — Hilbert-symbol table.](figures/aux9_1_ramification_table.png)

*Auxiliary Figure A9.1.* Hilbert symbols for several \((a,b)\) at small places; red \(-1\) marks ramification.

**Claim type.** Classification by ramification sets and Hilbert symbols: **Theorem** (classical). Implementation in the book helper: **Software fact** (pedagogical, not a full number-theory library).

---

## 9.2 Orders in quaternion algebras

An **order** is a subring that is a full-rank \(\mathbb{Z}\)-lattice in the algebra. In the Hamilton setting:

| Order | Definition | Units | Euclidean? |
|-------|------------|-------|------------|
| Lipschitz | \(\mathbb{Z}[i,j,k]\) | 8 | No |
| Hurwitz | all-integer or all-half-integer coords | 24 | Yes (maximal) |

The Hurwitz order is preferred for arithmetic (Chapter 1 **Model** preference for lattice work; Euclidean algorithm is classical **Theorem**). Its unit group is the binary tetrahedral group—the set \(\Lambda_0\) of Chapter 3.

![Figure 9.2 — Hurwitz order.](figures/fig9_2_hurwitz_order.png)

*Figure 9.2.* 24 Hurwitz units in stereographic \(S^3\), and Lipschitz vs Hurwitz comparison.

```text
HurwitzOrder().units          # 24
HurwitzOrder().is_euclidean() # True (classical fact)
HurwitzOrder().is_maximal()   # True (classical fact)
LipschitzOrder().n_units()    # 8
```

In general quaternion algebras, **maximal orders** play the role of rings of integers in number fields; different maximal orders need not be conjugate when the class number is nontrivial.

---

## 9.3 Ideal theory and class groups

One studies left ideals, right ideals, and two-sided ideals of an order. For **definite** quaternion algebras (ramified at \(\infty\)), the left ideal class set of a maximal order is finite. Ideal multiplication induces a group structure on (two-sided) ideal classes, and related class sets control representation of integers by norms of ideals.

### Hurwitz class number (classical)

The left ideal class number of the Hurwitz order is **1**: every left ideal is principal. The book helper reports this as a cited classical fact with a finite sample check of small-norm elements—not a full ideal enumeration.

```text
left_ideal_class_group(HurwitzOrder())
  → IdealClassGroupResult(order=1, method='classical_hurwitz_class_number_one', ...)
```

![Figure 9.3 — Ideal class group schematic.](figures/fig9_3_ideal_class_group.png)

*Figure 9.3.* Ideal classes with multiplication. For Hurwitz, a single class; general definite orders may have larger finite class numbers.

**Claim type.** Finiteness for definite maximal orders; Hurwitz class number 1: **Theorem** (classical). Full algorithmic enumeration of ideals for general \((a,b)\): out of scope for this sandbox.

---

## 9.4 From ideals to flux topographs and flywheels (Model bridge)

Chapter 8 approximated class groups with composition of flux topographs. The natural dictionary is still a **Model**:

| Algebraic object | Geometric / Model object |
|------------------|--------------------------|
| Ideal in a quaternion order | Flux configuration / supporting cycle on the gauged Hopf lattice |
| Ideal class | Equivalence class of reduced flux topographs |
| Ideal class group | Class-group analogue of Chapter 8 |
| Norm of an ideal | Stability score or `magic_island_score` |
| Ideal multiplication | Composition of flywheels (when well-defined — OP6) |

![Figure 9.4 — From ideal class to flux flywheel.](figures/fig9_4_ideal_to_flywheel.png)

*Figure 9.4.* Schematic Model bridge. Not a proved functor.

**Open Problem 6 (continued).**  
Use ideal theory of quaternion algebras to define a rigorous composition law on classes of flux configurations that is associative, gauge-compatible, and reduces to Gauss composition in suitable limits. Determine whether the resulting class group predicts Magic Island location and size.

```text
form_ideal_dictionary_entry()   # static dictionary for labs
class_group_analogue(...)       # Ch. 8 Model side
left_ideal_class_group(...)     # algebraic side (Hurwitz: order 1)
```

---

## 9.5 First computational labs

```text
qga/lib/quaternion_algebra.py
qga/lib/composition.py
qga/lib/flux_topograph.py
```

### Lab 9.A — Construct a small quaternion algebra

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "Projects" / "qga"))

from lib.quaternion_algebra import QuaternionAlgebra

A = QuaternionAlgebra(-1, -1)
print(A.presentation())
print("ramified:", A.ramified_places())
print("definite:", A.is_definite())

B = QuaternionAlgebra(2, 3)
print(B.presentation(), "ramified:", B.ramified_places(), "definite:", B.is_definite())
```

### Lab 9.B — Hurwitz order and its units

```python
from lib.quaternion_algebra import HurwitzOrder, LipschitzOrder

O = HurwitzOrder()
print("n_units:", O.n_units())           # 24
print("euclidean:", O.is_euclidean())    # True
print("maximal:", O.is_maximal())        # True
print("half unit in order:", O.contains([0.5, 0.5, 0.5, 0.5]))

L = LipschitzOrder()
print("Lipschitz units:", L.n_units(), "euclidean:", L.is_euclidean())
```

### Lab 9.C — Ideal class number (Hurwitz)

```python
from lib.quaternion_algebra import left_ideal_class_group

cg = left_ideal_class_group(O, bound=100)
print("class number:", cg.order)
print("method:", cg.method)
print(cg.notes)
```

### Lab 9.D — Bridge to Model class_number_analogue

```python
from lib.hopf_lattice import sample_angle_lattice, candidate_adjacency
from lib.flux_topograph import build_flux_topograph
from lib.composition import class_group_analogue

pts = sample_angle_lattice(n_eta=2, n_xi1=6, n_xi2=6)
along, inter = candidate_adjacency(pts, base_angle_thresh=0.55, fiber_phase_bins=6)
topo = build_flux_topograph(pts, edges=along + inter, functional="hopf_height")
cg_model = class_group_analogue(topo, dedup_tol=0.1, samples=8)
print("Model order:", cg_model["order"], "structure:", cg_model["structure"])
print("Algebraic Hurwitz class number:", cg.order)
# Expect: algebraic order 1 vs Model order often > 1 — different objects
```

### Lab 9.E — Hilbert symbols table

```python
from lib.quaternion_algebra import hilbert_symbol

for a, b in [(-1, -1), (2, 3), (-1, 3)]:
    print((a, b), {p: hilbert_symbol(a, b, p) for p in [2, 3, 5, "inf"]})
```

---

## Exercises

**9.A (hand).** Define a quaternion algebra over \(\mathbb{Q}\) and state what ramification means.

**9.B (hand).** Why is the Hurwitz order preferred over the Lipschitz order for most arithmetic work?

**9.C (code).** Complete Labs 9.A–9.B. Confirm 24 Hurwitz units and Euclidean / maximal flags.

**9.D (code).** Run Lab 9.C. What class number do you obtain for Hurwitz, and what does the `method` string say?

**9.E (code).** Complete Lab 9.D. Compare algebraic class number \(1\) with the Model `class_group_analogue` order. Why can they differ?

**9.F (Hatcher bridge).** In Hatcher Chapter 8, forms correspond to ideals. Sketch how §9.4’s dictionary might be made precise for a quaternion order (even if only conjecturally).

**9.G (Open Problem 6).** Using Hurwitz class number 1, what would a *successful* OP6 composition law look like when restricted to configurations “coming from” principal ideals? What obstructions remain for non-principal classes in other algebras?

**9.H (forward).** Why will Chapter 10’s observational validation benefit from a rigorous ideal-theoretic home for class-group analogues?

**9.I (software honesty).** Distinguish: (i) classical ideal class groups (**Theorem**), (ii) `left_ideal_class_group` toy report (**software** citing theorem), (iii) Ch. 8 `class_group_analogue` (**Model**).

---

## Code and asset pointers

```text
qga/lib/quaternion_algebra.py
  QuaternionAlgebra, hilbert_symbol,
  HurwitzOrder, LipschitzOrder,
  left_ideal_class_group, form_ideal_dictionary_entry

qga/lib/composition.py
qga/lib/hopf_lattice.py   # HURWITZ_UNITS shared with Ch. 3
```

**Figures:** `scripts/generate_ch9_figures.py`  
**Open problems:** OP6 (composition via ideal theory); OP1–OP3 for the geometric side of the dictionary.

---

## Looking ahead

We now have the algebraic backbone—quaternion algebras, orders, and ideal class groups—that can host rigorous versions of the Model constructions in Chapters 5–8. In **Chapter 10** we return to the observational layer: statistical protocols for \(350/\pi\), the \(Z\mapsto\) map, Magic Islands, and any class-group predictions that become precise enough to test.

With the ideal-theoretic foundation in place, the full construction is ready for observational scrutiny.

---

*Manuscript · Part IV · Chapter 9 · Figures in `book/figures/` · Helpers: `lib/quaternion_algebra.py`.*
