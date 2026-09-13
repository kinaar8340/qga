# QGA Spine Note: Quaternion Orders, Hopf, and the Hatcher Lift

This is a short extract of theorems already on the QGA spine. It is **not** the book.

The book remains *Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics* (`book/*.md`, GitHub Release **`draft-D`**). This note does not add a Part, does not replace that PDF, and is not a crate. crates.io publish and Open Problem 1 (canonical adjacency) wait on the finished note; they are not settled here.

**Compatibility (Software fact of the stack, not a theorem).** The book draft D works with `flux-hopf-lib==0.3.1` (git tag `v0.3.1`), `qga_engine@7e7866b`, and `qga_gpu@b9c9994`. Do not float `main`. Details of those pins sit in the marked appendix.

Models, hypotheses, and lab Software facts that *use* the spine live in [`appendix_models.md`](appendix_models.md). Nothing in that appendix is a QGA theorem.

Sources restated, not invented: `book/01_quaternions.md`, `book/02_hopf.md`, `book/03_gauged_hopf_lattice.md` §3.1 and §3.5, `book/04_symmetries.md` §4.2, `book/HOW_TO_USE.md`, `HATCHER_MAP.md`, `TOC.md`, `notes/open_problems.md`, `flux_hopf_lib` 0.3.1.

---

## 1. Claim labels

Every major claim in this note is one of four kinds. The table is the same as `book/HOW_TO_USE.md` §1 and the `qga` README.

| Label | Meaning | In this note |
|-------|---------|----------------|
| **Theorem** | Geometry or arithmetic already on the spine | Quaternion algebra and orders; four-square via the multiplicative norm; classical Hopf map, fibers, Hopf invariant \(1\); cardinality of the 24 Hurwitz units |
| **Model** | Construction that uses the spine | **Appendix only** |
| **Hypothesis** | Observational claim that can fail | **Appendix only** |
| **Software fact** | True of current SoT code or of a named helper | Listing order of `HURWITZ_UNITS` in `flux_hopf_lib==0.3.1`; `hopf_map` call signatures |

**Rule of thumb.** Geometry and classical algebra → Theorem. Lattice / topograph / flywheel design choices → Model (appendix). Portal numerics about the physical world → Hypothesis (appendix). “What this function returns today” → Software fact.

This note does not promote a Model into a Theorem.

---

## 2. Quaternion orders

From `book/01_quaternions.md` §§1.1–1.5. Double cover \(\mathrm{Spin}(3)\to SO(3)\) is recalled only as far as the Hopf section needs it (§1.6). Portal labs and the **Model** preference “use Hurwitz later for flux work” stay out of this body.

### 2.1 The algebra \(\mathbb{H}\)

A quaternion is \(q = a + bi + cj + dk\) with \(a,b,c,d\in\mathbb{R}\) and Hamilton’s rules \(i^2=j^2=k^2=ijk=-1\). These force \(ij=k\), \(jk=i\), \(ki=j\) and the opposite signs on the reverse products. Multiplication is associative and distributive, and **not commutative**.

As a real vector space \(\mathbb{H}\cong\mathbb{R}^4\) with basis \(\{1,i,j,k\}\). Identifying \(\mathbb{C}\) with \(\mathrm{span}_{\mathbb{R}}\{1,i\}\) gives the unique writing
\[
q = z_1 + z_2\, j,\qquad z_1,z_2\in\mathbb{C},
\]
the bridge to the Hopf map in §3.

If \(q_1 = a_1 + b_1 i + c_1 j + d_1 k\) and \(q_2 = a_2 + b_2 i + c_2 j + d_2 k\), the product is
\begin{align*}
q_1 q_2
&=
(a_1 a_2 - b_1 b_2 - c_1 c_2 - d_1 d_2)\\
&\quad+ (a_1 b_2 + b_1 a_2 + c_1 d_2 - d_1 c_2)\, i\\
&\quad+ (a_1 c_2 - b_1 d_2 + c_1 a_2 + d_1 b_2)\, j\\
&\quad+ (a_1 d_2 + b_1 c_2 - c_1 b_2 + d_1 a_2)\, k.
\end{align*}
**Theorem.** This is the bilinear product of \(\mathbb{H}\). **Software fact:** it is exactly `Quaternion.multiply` in `flux_hopf_lib` 0.3.1 (pedagogical re-export in `lib/`). Do not fork a second formula.

### 2.2 Conjugate and multiplicative norm

The conjugate is \(\overline{q}=a-bi-cj-dk\). **Theorems:** \(\overline{\overline{q}}=q\), conjugation of a sum is the sum of conjugates, and \(\overline{q_1 q_2}=\overline{q_2}\,\overline{q_1}\) (order reversal).

The **multiplicative norm** is
\[
N(q) \;:=\; q\,\overline{q} \;=\; a^2+b^2+c^2+d^2.
\]
In code, `Quaternion.norm()` returns the Euclidean length \(|q|=\sqrt{N(q)}\). Number theory uses \(N(q)\).

**Theorem (multiplicativity).** For all \(q_1,q_2\in\mathbb{H}\), \(N(q_1 q_2)=N(q_1)N(q_2)\). Sketch: \(N(q_1 q_2)=(q_1 q_2)\overline{q_2}\,\overline{q_1}=q_1 N(q_2)\overline{q_1}=N(q_1)N(q_2)\), since \(N(q_2)\) is real, hence central.

If \(q\neq 0\), then \(q^{-1}=\overline{q}/N(q)\). \(\mathbb{H}\) is a division ring.

### 2.3 Unit quaternions as \(S^3\)

**Theorem.** The set of unit quaternions
\[
\mathrm{Sp}(1) \;=\; \{ q\in\mathbb{H}: N(q)=1 \} \;=\; S^3\subset\mathbb{R}^4
\]
is a compact Lie group under quaternion multiplication (associative, identity \(1\), inverses \(\overline{q}\)). Left or right multiplication by a fixed unit is an isometry of \(S^3\) with respect to the round metric. As a complex pair, unit length is \(|z_1|^2+|z_2|^2=1\).

Geometrically \(S^3\) is the unit sphere in four-dimensional Euclidean space. Removing a point and projecting to a tangent \(\mathbb{R}^3\) yields a global chart on \(S^3\setminus\{\mathrm{pt}\}\). That chart is used to *draw* fibers later; it is not a second Hopf map.

### 2.4 Lipschitz and Hurwitz orders

The **Lipschitz order** is \(L=\mathbb{Z}[i,j,k]\). It is a free \(\mathbb{Z}\)-module of rank 4, closed under multiplication, with eight units \(\{\pm 1,\pm i,\pm j,\pm k\}\).

The **Hurwitz order** \(\mathcal{H}\) consists of quaternions whose coordinates are either all integers or all half-integers:
\[
\mathcal{H} \;=\; L \;\cup\; \bigl(\tfrac12+\tfrac12 i+\tfrac12 j+\tfrac12 k+L\bigr).
\]
It is a ring (a maximal order in the rational quaternion algebra).

**Theorem.** The unit group of \(\mathcal{H}\) has **24** elements—the binary tetrahedral group:
\[
\{\pm 1,\pm i,\pm j,\pm k\}
\;\cup\;
\bigl\{\tfrac12(\pm 1\pm i\pm j\pm k)\bigr\}
\]
(all sign combinations in the second family). \(\mathcal{H}\) is Euclidean with respect to the norm: for \(q,d\in\mathcal{H}\) with \(d\neq 0\) there exist \(m,r\in\mathcal{H}\) with \(q=md+r\) and \(N(r)<N(d)\).

**Software fact** (`flux_hopf_lib==0.3.1`, `flux_hopf_lib.quaternion.hurwitz`). Cardinality 24 is the theorem above. The listed order of `HURWITZ_UNITS` is not: \(\pm 1,\pm i,\pm j,\pm k\) as minus-then-plus on each axis, then \((\pm 1\pm i\pm j\pm k)/2\) via `itertools.product([-1/2, 1/2], repeat=4)` with the last index fastest. Pedagogical re-export: `lib/hopf_lattice.py`. That array is not a GPU constant and not a second algebra.

Preferring Hurwitz as the *working lattice for later flux chapters* is a **Model** (`book/01_quaternions.md` §1.4). It is not in this body.

### 2.5 Four squares

**Theorem (Lagrange).** Every natural number is a sum of four integer squares.

**Quaternionic reading.** For every \(n\in\mathbb{N}\) there exists \(q\in L\) with \(N(q)=n\). Euler’s four-square identity is \(N(q_1 q_2)=N(q_1)N(q_2)\) in coordinates, so it suffices to treat primes (or square-free \(n\)) and multiply representations. Classical proofs then show every prime is a norm from \(\mathcal{H}\) (or handle \(2\) and the two residue classes of odd primes by standard casework). This note claims no new proof. Four squares are the norm theory of integer quaternions.

Hatcher’s early chapters work with **two** squares and binary quadratic forms. Quaternions are the four-dimensional upgrade of that instinct, not a reprint of those chapters.

### 2.6 Double cover, as much as Hopf needs

Identify \(\mathbb{R}^3\) with the pure imaginaries \(\mathrm{Im}\,\mathbb{H}=\{bi+cj+dk\}\). For a **unit** \(q\in S^3\) and \(v\in\mathrm{Im}\,\mathbb{H}\),
\[
\rho_q(v) \;:=\; q\, v\, \overline{q}
\]
is again pure imaginary, and \(\rho_q\in SO(3)\). This is a homomorphism \(\rho:S^3\to SO(3)\). If \(q=\cos(\theta/2)+\sin(\theta/2)\,u\) with unit pure imaginary \(u\), then \(\rho_q\) is rotation by \(\theta\) about \(u\) (Rodrigues). **Theorem:** \(\ker\rho=\{\pm 1\}\), so \(\rho\) is the classical double cover \(\mathrm{Spin}(3)\to SO(3)\). Paths in \(SO(3)\) that rotate by \(2\pi\) lift to paths from \(q\) to \(-q\); only \(4\pi\) closes in the cover.

The same unit quaternions are the total space of the Hopf map in §3. Directions in \(\mathbb{R}^3\) relate to the base \(S^2\); the fiber phase is the extra spinorial degree of freedom. That last sentence is the classical bundle, not a lattice Model.

---

## 3. Classical Hopf map

From `book/02_hopf.md` §§2.1–2.2, and §2.5 only for “one fiber per unit quaternion.” Portal layout and gauged-lattice adjacency stay out.

### 3.1 Complex-pair and real four-vector forms

Identify unit quaternions with \((z_1,z_2)\in\mathbb{C}^2\), \(|z_1|^2+|z_2|^2=1\). One classical form of the **Hopf map** \(h:S^3\to S^2\) is
\[
h(z_1,z_2)
=
\bigl(
  2\,\mathrm{Re}(\overline{z_1} z_2),\;
  2\,\mathrm{Im}(\overline{z_1} z_2),\;
  |z_1|^2-|z_2|^2
\bigr)
\in S^2,
\]
equivalently the projectivized ratio \([z_1:z_2]\in\mathbb{CP}^1\cong S^2\). Common phase \(e^{i\phi}\) does not change the projective point: that circle is the fiber.

Write \(z_1=x_1+i x_2\), \(z_2=x_3+i x_4\). The same map is
\[
y_1=2(x_1 x_3+x_2 x_4),\quad
y_2=2(x_1 x_4-x_2 x_3),\quad
y_3=x_1^2+x_2^2-x_3^2-x_4^2.
\]

**Theorem.** On a unit 4-vector this already lands on \(S^2\). There is **no** output-normalization by \(\|y\|\).

**Software fact.** The one library map is `flux_hopf_lib.hopf.fibration.hopf_map` (alias `hopf_map_classical`) at `0.3.1`. The book helper `lib.hopf_lattice.hopf_map` re-exports it. Do not fork. A non-unit input is a numerical guard (homogeneous of degree 2: divide by \(\|q\|^2\)), not a feature of the map.

Call signatures are component-wise:
```text
hopf_map(x1, x2, x3, x4)           → (y1, y2, y3)
hopf_map_quaternion(w, x, y, z)    → (y1, y2, y3)
Quaternion(...).hopf_image()       → (y1, y2, y3)
```
Do not assume `hopf_map(q)` for a `Quaternion` object.

**Not a Hopf map.** The old three-component formula \(y_1=x_1^2-x_2^2\), \(y_2=2x_1 x_2\), \(y_3=2(x_3 x_4+x_1 x_2)\) (then divide by \(\|y\|\)) ignores \((x_3,x_4)\) in \(y_1,y_2\), vanishes at \((0,0,1,0)\), and is not constant on Hopf fibers. It is kept only as `legacy_portal_map` and is **not** called Hopf.

### 3.2 Structure-group fiber versus the angle-chart \(\xi_2\)-circle

Hopf angles \((\eta,\xi_1,\xi_2)\) via `hopf_coordinates` are
\[
\begin{aligned}
x_1&=\cos\eta\cos\xi_1, &
x_2&=\cos\eta\sin\xi_1,\\
x_3&=\sin\eta\cos\xi_2, &
x_4&=\sin\eta\sin\xi_2,
\end{aligned}
\]
with \(\eta\in[0,\pi/2]\) and \(\xi_1,\xi_2\in[0,2\pi)\). Fixing \((\eta,\xi_1)\) and sweeping \(\xi_2\) traces the **angle-chart \(\xi_2\)-circle**. That is **not** the structure-group fiber.

The Hopf fiber through \((z_1,z_2)\) is the diagonal \(U(1)\) action
\[
(z_1,z_2)\;\longmapsto\;(e^{i\phi}z_1,\,e^{i\phi}z_2),
\]
which shifts \(\xi_1\) and \(\xi_2\) **together**. Under \(q=z_1+z_2 j\) that action is left multiplication by \(e^{i\phi}=\cos\phi+i\sin\phi\in\mathrm{span}\{1,i\}\). General left or right multiplication by an arbitrary unit of \(S^3\) **moves fibers**.

This distinction is a Theorem of the classical bundle, recorded so that later adjacency Models (appendix) cannot be smuggled in as Hopf.

### 3.3 Fibers, linking, one fiber per unit

**Theorem.** Over each \(p\in S^2\) the preimage \(h^{-1}(p)\) is diffeomorphic to a circle. That circle is the structure-group \(U(1)\) action above.

**Theorem.** Any two distinct fibers are linked exactly once in \(S^3\). The Hopf invariant of \(h:S^3\to S^2\) equals \(1\). Classical differential topology; sampled linking helpers in the library are Software facts, not substitutes.

**Theorem.** The Hopf fibration is a fiber bundle \(S^1\hookrightarrow S^3\twoheadrightarrow S^2\), the canonical nontrivial principal \(U(1)\)-bundle. Locally it is a product \(U\times S^1\); globally the twisting produces the linking of fibers. The base \(S^2\) is covered by the usual stereographic charts; over each chart there is a local trivialization \(h^{-1}(U)\cong U\times S^1\). Crossing charts changes phase by a \(U(1)\) transition function. That is classical bundle language, not a discrete gauge Model.

**Theorem.** The Hopf map partitions \(S^3\): every unit quaternion lies on exactly one fiber (`book/02_hopf.md` §2.5).

**Theorem.** For unit \(u\), \(q\mapsto uq\) and \(q\mapsto qu\) are isometries of \(S^3\). Left multiplication maps fibers to fibers and induces a rotation of the base. Right multiplication is fiberwise \(U(1)\) only for the structure-group circle (and Hurwitz units that normalize it). General right multiplication by an arbitrary unit **moves fibers**.

Calling Hopf a higher-dimensional “Farey analogue” remains a **Model** metaphor until a discrete adjacency rule is canonical. That metaphor is not a theorem of this section.

---

## 4. Hatcher as method, not reprint

Cite Allen Hatcher, *Topology of Numbers*, free PDF at https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf (AMS edition exists). This note does not reuse Hatcher’s prose, figures, or exercises. Parallel reading: `HATCHER_MAP.md`. Dictionary pointer only: `book/F_hatcher_dictionary.md`.

Hatcher re-grounds elementary number theory in pictures: Farey diagram, continued-fraction zigzags, Conway topographs, linear-fractional symmetries, class groups of quadratic forms. The **lift** used here is

> Farey plane \(\longrightarrow\) \(S^3\) / Hopf,

not a unique mediant rule on a quaternionic lattice.

`TOC.md` already splits the long book: Parts I–II and IV are the geometric/arithmetic spine (theorems plus labeled Models); Part III is flux topographs (Model/OP); Part V isolates Models and Hypotheses. This note is the short form of that split. The unique-mediant question is Open Problem 1 (§5), not a theorem of the lift.

Hatcher opens with Farey geometry *before* forms. QGA inserts Ch. 1–2 (quaternions + Hopf) first so the Farey lift in Ch. 3 is readable (`HATCHER_MAP.md`, structural choice). Readers who already know \(S^3\) and Hopf can skim to §4–5.

Condensed parallel (foundations only; later TN chapters map to Models in the appendix):

| Hatcher TN | This note / book | What is a theorem here |
|------------|------------------|------------------------|
| Ch. 0 Preview | Ch. 1–2 | Four squares; Hopf as classical topology |
| *(no TN counterpart)* | Part I · Ch. 1–2 | \(\mathbb{H}\), Hurwitz 24, \(h:S^3\to S^2\) |
| Ch. 1 Farey diagram | Ch. 3 §3.1, §3.5 | \(\Lambda_0\) as points; adjacency stays Open |
| Ch. 3 Farey symmetries | Ch. 4 §4.2 | Isometries of \(S^3\); LFT parallel is analogy |

TN Ch. 4–8 (forms, classification, representations, class group, quadratic fields) and QGA Parts III–V are **not** theorems of this body. See the appendix.

### 4.1 Hurwitz units as discrete points on \(S^3\)

From `book/03_gauged_hopf_lattice.md` **§3.1 only**. Density-beyond-24 samples and §3.2 adjacency stay in the appendix.

**Theorem.** The 24 Hurwitz units lie on the unit sphere:
\[
\Lambda_0 \;=\; \{ q\in\mathcal{H}: N(q)=1 \} \;=\; \mathcal{H}\cap S^3.
\]
They are the same 24 elements as in §2.4.

**Theorem.** The Hopf image \(h(\Lambda_0)\) consists of the six octahedron poles on \(S^2\) (four units per fiber). That is a fact of the classical map on the 24-cell / \(\Lambda_0\), not an adjacency theorem.

Nested denser samples \(\Lambda_{\mathrm{ang}}\), \(\Lambda_{\mathrm{dyn}}\), and “enough points for Farey-style walks” are design levels for later Models. They are not theorems of \(\Lambda_0\).

### 4.2 Linear fractional transformations as analogy

From `book/04_symmetries.md` **§4.2**.

Hatcher organizes the Farey diagram with linear fractional transformations \(T(z)=(az+b)/(cz+d)\), \(ad-bc=\pm 1\) (\(\mathrm{PGL}(2,\mathbb{Z})\)). Those maps preserve classical Farey adjacency.

On \(S^3\) the analogous organizing actions are left and right multiplications by units. **Theorem:** those maps are isometries of \(S^3\) (`book/04_symmetries.md` §4.1, one sentence). **Not a theorem:** that they play the role of \(\mathrm{PGL}(2,\mathbb{Z})\) on a discrete graph. Left/right unit multiplications are **not** claimed to be \(SL(2,\mathbb{Z})\) or \(\mathrm{PGL}(2,\mathbb{Z})\). Preservation of a candidate adjacency, translations along fibers, glides, and periodic CF analogues remain a **Model** metaphor until OP1 is resolved (`book/04_symmetries.md` §4.2, claim type). That metaphor belongs in the appendix if used at length; here it is only the analogy Hatcher's method licenses.

---

## 5. What stays open

**Open Problem 1 stays Open.** This section is a pointer, not a proof. Home: `book/03_gauged_hopf_lattice.md` **§3.5**. Ledger: `notes/open_problems.md`, `book/B_open_problems.md`.

OP1 asks to prove uniqueness (or classify all reasonable choices) of discrete adjacency / mediant rules on a gauged Hopf lattice such that (`book/03_gauged_hopf_lattice.md` §3.5):

1. The structure **reduces to the classical Farey diagram** under a suitable projection or restriction (a fixed complex line, a parabolic subgroup, or a 2D slice of base coordinates)—in the book wording, an embedding of \(\mathbb{Q}\cup\{\infty\}\).
2. Adjacency is **compatible** with left and right gauge actions (equivariance).
3. The resulting graph admits **continued-fraction paths** (discrete walks that refine approximants), including walks that advance primarily **along fibers**.
4. (Optional.) A Euclidean or greedy algorithm on the lattice recovers shortest paths analogous to Farey mediants.

Current status of the *book*, restated: \(\Lambda_0\) is classical and settled; Hopf projection of discrete sets is implemented; `candidate_adjacency` is numerical experiment, **not** proved canonical; reduction to Farey \(\lvert ad-bc\rvert=1\) is **Open**; equivariant mediant is **Open**. This note does not advance those rows.

Two adjacency **Models** exist. They are not theorems of this note.

- Frozen book default `candidate_adjacency` is a **Software fact** of `lib/hopf_lattice.py`: it is the rule used for book figures and the golden test. It traces the angle-chart \(\xi_2\)-circle, **not** the structure-group \(U(1)\) fiber of §3. Until OP1 is resolved, do not treat that graph as if the base were the Hopf fibration of Chapter 2.
- Model 2 (`structure_group`) is a second construction. It is not canonical. A named slice-A overlap with Gaussian neighbors on \(h(\Lambda_0)\) is a \(\mathbb{P}^1(\mathbb{C})\) picture, **not** \(\mathbb{Q}\cup\{\infty\}\).

Harness JSON, keep-rate tables, and `notes/PIPELINES.md` are the lab notebook. They do **not** enter this body. They do not close OP1.

Public sentence, unchanged: two adjacency Models; OP1 Open.

---

## References (this extract)

- Hatcher, A. *Topology of Numbers*. https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf
- `qga-lab/qga` book: `book/01_quaternions.md`, `book/02_hopf.md`, `book/03_gauged_hopf_lattice.md` §§3.1, 3.5, `book/04_symmetries.md` §4.2, `book/HOW_TO_USE.md`, `HATCHER_MAP.md`, `TOC.md`, `notes/open_problems.md`
- `qga-lab/flux_hopf_lib` tag `v0.3.1` / PyPI `0.3.1`
- Book Release `draft-D` (the long PDF; not this note)

Models and hypotheses: [`appendix_models.md`](appendix_models.md).
