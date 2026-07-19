# Chapter 0 — A Preview

This chapter is a guided tour, not a full development. By the end you should see a single chain of ideas:

\[
\text{Pythagorean triples}
\;\longrightarrow\;
\text{sums of two squares}
\;\longrightarrow\;
\text{four squares / quaternions}
\;\longrightarrow\;
S^3
\;\longrightarrow\;
\text{Hopf fibration}
\;\longrightarrow\;
\text{gauged lattice \& flux flywheels}
\;\longrightarrow\;
\text{\(Z\mapsto\) flux map (model)}
\]

and know which links are classical mathematics and which are working models or hypotheses from Kingdom Come.

**Learning goals**

1. Recall why geometry already sits inside elementary number theory.  
2. Meet unit quaternions as \(S^3\) and the Hopf map \(S^3\to S^2\).  
3. Glimpse flux flywheels and the \(Z\)-to-flux idea without full machinery.  
4. Spot the \(350/\pi\) signature as a **Hypothesis**, not a theorem.  
5. Own a visual roadmap for the rest of the book.

**Figures in this chapter** (all from Kingdom Come assets; paths relative to this file)

| Tag | File | Role |
|-----|------|------|
| Fig. 0.1 | `figures/fig0_1_hopf_linked_fibers.png` | Linked Hopf fibers in stereographic view |
| Fig. 0.2 | `figures/fig0_2_hopf_stereographic.png` | Stereographic preview of the fibration |
| Fig. 0.3 | `figures/fig0_3_hopf_bundle.png` | Bundle picture: total space \(\to\) base |
| Fig. 0.4 | `figures/fig0_4_flux_flywheel_scales.jpg` | Flux flywheel scales / nested structure |
| Fig. 0.5 | `figures/fig0_5_hopf_lattice_pi_cycle.jpg` | Gauged lattice meets \(350/\pi\) cycle motif |

| Aux A0.1 | `figures/aux_z_map_he.png` | Helium \(Z=2\) flux-flywheel still (closed-shell baseline) |
| Aux A0.2 | `figures/aux_z_map_fe.png` | Iron \(Z=26\) flux-flywheel still (mid-table contrast) |

---

## 0.1 From Pythagorean triples to sums of two squares

A **Pythagorean triple** is a triple of positive integers \((a,b,c)\) with
\[
a^2 + b^2 = c^2.
\]
The triple \((3,4,5)\) is the smallest; infinitely many others exist. Already geometry and arithmetic talk: the equation is the integer-point condition on a circle of radius \(c\), or the norm condition \(N(a+bi)=c^2\) in the Gaussian integers \(\mathbb{Z}[i]\).

Hatcher’s *Topology of Numbers* opens by pushing this geometric instinct further. Rational slopes, mediants
\[
\frac{a}{c}\oplus\frac{b}{d} \;=\; \frac{a+b}{c+d},
\]
and the **Farey diagram** organize which fractions “touch” which others. Continued fractions become zigzag paths on that diagram. Binary quadratic forms
\[
f(x,y) = ax^2 + bxy + cy^2
\]
acquire **topographs**—value landscapes on the dual of the Farey triangulation—whose periodic separator lines encode Pell-type infinitude and classification.

We will not rebuild that plane geometry here (read Hatcher Chapters 0–4 for the full story). We only need the moral:

> Elementary number theory is already a theory of **pictures**: adjacency, paths, periods, and symmetries of integer data.

The present book asks what happens when those pictures are lifted from two variables and the rational/hyperbolic plane to **four real coordinates** organized by quaternion multiplication and a celebrated fiber bundle.

---

## 0.2 Four squares and the birth of quaternions

Lagrange’s four-square theorem asserts that every natural number is a sum of four integer squares:
\[
n = a^2 + b^2 + c^2 + d^2.
\]
There is a classical algebraic home for this statement: the **quaternions**
\[
\mathbb{H} = \{ \, q = a + bi + cj + dk \mid a,b,c,d\in\mathbb{R} \, \},
\]
with
\[
i^2=j^2=k^2=ijk=-1.
\]
The multiplicative **norm**
\[
N(q) = a^2+b^2+c^2+d^2 = q\,\overline{q}
\]
satisfies \(N(q_1 q_2)=N(q_1)N(q_2)\). Integer quaternions (Lipschitz \(\mathbb{Z}[i,j,k]\), better still the **Hurwitz order**) turn the four-square theorem into an arithmetic fact about norms—just as Gaussian integers turn two-square questions into unique factorization and primes congruent to \(1\bmod 4\).

**Claim type:** four-square theorem and the norm identity are **Theorems** (classical). Their use as the *algebraic backbone* of Kingdom Come’s geometry is a **Model** choice we make explicit.

Chapter 1 develops multiplication, conjugation, unit quaternions, and the Lipschitz/Hurwitz orders in full. For the preview, one geometric fact is enough:

\[
\{ q\in\mathbb{H} : N(q)=1 \} \;=\; S^3 \subset \mathbb{R}^4.
\]

The unit sphere in four dimensions is not an ornament. It is the total space of the map we study next.

---

## 0.3 Circles and spheres as number-theoretic objects

In Hatcher’s world, the circle \(S^1\) already appears indirectly: slopes, rotations in the plane of a binary form, and periodic topograph orbits. The two-sphere \(S^2\) is less prominent in elementary texts, but it is the natural **base** once we pass to unit quaternions.

Write a unit quaternion as a pair of complex numbers (up to the usual identification)
\[
q \;\longleftrightarrow\; (z_1,z_2)\in\mathbb{C}^2,\qquad |z_1|^2+|z_2|^2=1.
\]
The classical **Hopf map** sends \(q\) to a point on \(S^2\). One real-coordinate form used in Kingdom Come’s documentation is
\begin{align*}
y_1 &= x_1^2 - x_2^2,\\
y_2 &= 2 x_1 x_2,\\
y_3 &= 2(x_3 x_4 + x_1 x_2),
\end{align*}
for a unit 4-vector \((x_1,x_2,x_3,x_4)\in S^3\) (see `kingdom` theory notes and `flux_hopf_lib`). Equivalent complex forms identify the base point with a ratio \([z_1:z_2]\in\mathbb{CP}^1\cong S^2\).

**Fiber intuition.** Over each base point sits a **circle’s worth** of unit quaternions—the fiber—obtained by rotating a phase along that circle. Distinct fibers are **linked**: any two are linked once (Hopf invariant \(1\)). Stereographic projection \(S^3\setminus\{\mathrm{pt}\}\to\mathbb{R}^3\) displays those fibers as linked Villarceau circles on nested tori.

![Figure 0.1 — Linked Hopf fibers (stereographic view). Source: Kingdom Come `app/assets/home/hopf_linked_fibers.png`.](figures/fig0_1_hopf_linked_fibers.png)

*Figure 0.1.* Two (or more) fibers of the Hopf fibration after stereographic projection to \(\mathbb{R}^3\). Linking is the topological signature that will later underwrite **protection** of flux configurations: you cannot unlink fibers by continuous deformation without cutting.

![Figure 0.2 — Stereographic Hopf preview. Source: Kingdom Come `app/assets/hopf_preview.png`.](figures/fig0_2_hopf_stereographic.png)

*Figure 0.2.* A portal-style stereographic preview of the fibration: the same total space seen as a single composed picture rather than isolated fibers. In the Gradio app this is the “Hopf Visualizer” family of views (2D projections are preferred on CPU-only hosts).

Hatcher’s Farey diagram arranges **rational slopes** so that adjacency and mediants are visible. Hopf arranges **circle fibers** over a sphere so that linking and phase are visible. The analogy is not identity of objects; it is identity of **method**: a picture that makes the right discrete or continuous relationships obvious.

**Forward pointer.** Calling Hopf a “Farey analogue” is a **Model** metaphor only. **Chapter 3 will turn this metaphor into precise discrete definitions**—adjacency, mediants, and gauge data on a lattice in \(S^3\)—so that the analogy becomes a construction rather than a slogan.

---

## 0.4 The Hopf fibration as a higher-dimensional Farey analogue

We state the comparison carefully so it does not pretend to be a theorem of uniqueness.

| Farey diagram (Hatcher) | Hopf geometry (this book) |
|-------------------------|---------------------------|
| Vertices: rationals / cusps | Points of a discrete set in \(S^3\) (or in \(\mathbb{H}\)) |
| Edges: adjacency of fractions | Fiber segments / lattice bonds projecting under Hopf |
| Mediant of two fractions | Quaternionic (or lattice) combination rule, **to be axiomatized in Ch. 3** |
| Paths: continued fractions | Phase winding along fibers; walks on the gauged lattice |
| Symmetries: linear fractional maps | Left/right multiplication by unit quaternions; gauge actions |

![Figure 0.3 — Hopf fibration as a bundle. Source: Kingdom Come `app/assets/home/hopf_fibration_bundle.png`.](figures/fig0_3_hopf_bundle.png)

*Figure 0.3.* Conceptual bundle picture: total space \(S^3\), base \(S^2\), fibers circles. In Part II we **discretize** this picture—placing a lattice in the total space, projecting to the base, and defining adjacency—so that Farey-like combinatorial operations become available again.

**Claim type:** Hopf fibration, linking, and the double cover \(\mathrm{Spin}(3)\to SO(3)\) via unit quaternions are **Theorems** of classical topology/geometry. Calling Hopf a “Farey analogue” remains a **Model** metaphor until Chapter 3 supplies the discrete axioms (see also Open Problem 1: *canonical quaternionic Farey structure*).

---

## 0.5 First sight of the gauged Hopf lattice and flux flywheels

Kingdom Come’s physical **Model** (not yet a theorem of nature) can be stated in one paragraph:

> Physics emerges from **topologically protected flux structures** on a **gauged Hopf lattice** embedded in a **porous vacuum**. The Hopf fibration supplies the geometric backbone; quaternions supply the algebra; stable rotating configurations—**flux flywheels**—anchor emergent matter. Observer-linked phase holonomy between fibers damps toward synchrony with a coupling scale \(\kappa\).

A **flux flywheel**, for preview purposes, is a lattice-supported circulating flux whose topology (linking, winding, charge) obstructs continuous decay to a trivial configuration. In Hatcher’s topographs, **periodicity** of separator lines produces infinite families of representations (Pell). Here, **periodicity of a flywheel** is the dynamical counterpart: a closed orbit of gauge and phase that refuses to unwind.

![Figure 0.4 — Flux flywheel scales. Source: Kingdom Come `app/assets/bitcoin_pi/flux_flywheel_scales.jpg`.](figures/fig0_4_flux_flywheel_scales.jpg)

*Figure 0.4.* Nested / multi-scale flywheel imagery from the Kingdom Come observation assets. Read it as a **visual metaphor plus design sketch** for the lattice construction of Chapters 3–5: concentric scales, rotational identity, and coupling between levels. Formal definitions of lattice sites, gauge fields, and topological charge come later.

In code, lattice and flywheel experiments live under:

- `kingdom.core.lattice` — gauged lattice dynamics and stability comparisons  
- `kingdom.core.flux_flywheel` — `map_z_to_flywheel`, `map_z_to_flywheel_extended`  
- Gradio tabs: **Lattice Simulator**, **Flux Flywheel**

Chapter 5 will introduce **flux topographs**: value landscapes for quaternionic (or lattice flux) functionals, the direct conceptual child of Conway topographs.

---

## 0.6 A first \(Z\)-to-flux sketch and the \(350/\pi\) signature

### The \(Z\)-map (**Model**)

Kingdom Come implements a map from atomic number \(Z\) to a flywheel configuration and a bundle of stability / chemistry-facing metrics:
\[
Z \;\longmapsto\; \bigl(\text{flywheel state},\;\text{stability score},\;\text{shell-like descriptors},\;\ldots\bigr).
\]
Primary entry points: `map_z_to_flywheel` and `map_z_to_flywheel_extended` in `kingdom.core.flux_flywheel`. Detuning parameters (frequency offset, gauge strength, depth/layers) select **stability islands** in parameter space—**Magic Islands**—including a documented ultra-stable lock used as a noble-gas-like template.

The portal’s element tour renders each \(Z\) with shell clouds and a flux ring. Two static stills from that tour are kept beside the main figures:

![Auxiliary Figure A0.1 — Helium (\(Z=2\)) flux-flywheel still: closed-shell archetype with high model stability. Source: Kingdom Come `z_knowns/frame_0002.png`.](figures/aux_z_map_he.png)

*Auxiliary Figure A0.1 — Helium (\(Z=2\)).* Flux-flywheel element card from the portal tour: noble-gas closed shell, high stability score in the working model, and a simple shell/flux-ring visualization. Use this as the “quiet baseline” when comparing later \(Z\) values. Source: `z_knowns/frame_0002.png`.

![Auxiliary Figure A0.2 — Iron (\(Z=26\)) flux-flywheel still: mid-table nuclear/chemical specialness meets a richer flywheel profile. Source: Kingdom Come `z_knowns/frame_0026.png`.](figures/aux_z_map_fe.png)

*Auxiliary Figure A0.2 — Iron (\(Z=26\)).* Same tour format at iron: a mid-table configuration where real-world nuclear and chemical specialness can later be checked against model metrics (stability, ionization-energy anchors, magnetic-moment proxies in Chapters 7 and 10). Source: `z_knowns/frame_0026.png`.

**Claim type:** the existence of a coded map \(Z\mapsto\) configuration is a **Software fact**. Interpreting it as *the* emergence mechanism of the periodic table is a **Model**. Quantitative alignment with experiment is an empirical research program (Chapters 7 and 10), not a free theorem.

### The \(350/\pi\) signature (**Hypothesis**)

Kingdom Come’s constants module records a topological clock scale
\[
W_g \;=\; \frac{350}{\pi} \;\approx\; 111.408
\]
(`WG_FROM_350_OVER_PI`, with a documented lock value \(W_{g,\mathrm{lock}}\) in `flux_hopf_lib` / `kingdom.core.constants`). The same numerical motif appears in several **observation tracks** of the portal: Bitcoin Pi Cycle narratives, TLS tree branch bursts, cuprate superconductor sketches, pulsar-timing numerics, and related notes.

![Figure 0.5 — Hopf lattice and Pi-cycle motif. Source: Kingdom Come `app/assets/bitcoin_pi/hopf_lattice_pi_cycle.jpg`.](figures/fig0_5_hopf_lattice_pi_cycle.jpg)

*Figure 0.5.* Asset bridging the **gauged Hopf lattice** picture with the \(\pi\)-cycle / \(350/\pi\) observational storyline. In this book it marks the boundary between geometry (Parts I–IV) and the hypothesis layer (Part V).

**Claim type: Hypothesis.** Recurrence of \(350/\pi\) across domains is **not** proved from first principles in this chapter. Chapter 10 will:

1. list each domain with source and method,  
2. require a statistical validation checklist,  
3. state what would **confirm, refine, or falsify** the hypothesis.

Until then, treat \(W_g=350/\pi\) as a **named constant of the working model**, not as a theorem of number theory.

---

## 0.7 Visual roadmap: Hatcher diagrams meet Hopf and Gradio

Think of the book as five floors of the same building:

```text
Part V   Ch. 10     Observations & validation     ← Hypothesis & Model
Part IV  Ch. 8–9    Class groups & algebras       ← Hatcher Ch. 7–8 lift
Part III Ch. 5–7    Forms, topographs, Z-map      ← Hatcher Ch. 4–6 lift
Part II  Ch. 3–4    Gauged lattice (Farey lift)   ← Hatcher Ch. 1–3 lift
Part I   Ch. 1–2    Quaternions & Hopf            ← foundations (new floor)
         Ch. 0      This preview
```

**How the five main figures will reappear**

| Figure | Returns in |
|--------|------------|
| 0.1 Linked fibers | Ch. 2 (definition, Hopf invariant); Ch. 4 (symmetry orbits) |
| 0.2 Stereographic preview | Ch. 1–2 (coordinates, charts); Gradio labs |
| 0.3 Bundle diagram | Ch. 2–3 (discrete total space / base) |
| 0.4 Flywheel scales | Ch. 3, 5, 7 (lattice, topographs, \(Z\)-map) |
| 0.5 Lattice / \(\pi\)-cycle | Ch. 3 (lattice); Ch. 10 (observations) |

**Portal ↔ chapter cheat sheet**

| Gradio / module | First serious chapter |
|-----------------|----------------------|
| Hopf Visualizer · `core.hopf` · `viz.hopf_plotly` | 2 |
| Quaternion helpers · `core.quaternion` | 1 |
| Lattice Simulator · `core.lattice` | 3–4 |
| Flux Flywheel slider · `core.flux_flywheel` | 5–7 |
| Magic Island · `viz.magic_island` | 6 |
| Observations tabs · `constants.WG_FROM_350_OVER_PI` | 10 |

---

## 0.8 Reading plan for the rest of the book

1. **Part I (Ch. 1–2)** makes quaternions algebraic and geometric, then defines the Hopf fibration carefully and rebuilds Figures 0.1–0.3 from first principles.  
2. **Part II (Ch. 3–4)** constructs the gauged Hopf lattice and its symmetries—the Farey lift (Open Problem 1).  
3. **Part III (Ch. 5–7)** develops forms, flux topographs, Magic Islands, and the \(Z\)-map as representation theory (Open Problems 2–4).  
4. **Part IV (Ch. 8–9)** treats composition, class groups, and quaternion algebras (Open Problem 6).  
5. **Part V (Ch. 10)** collects multi-domain observations (\(350/\pi\), \(Z\mapsto\) correlations, Magic Islands), states validation protocols (Table T4), and summarizes Open Problems OP1–OP6 (Open Problem 5).

If you are impatient for physics, read 0 → 2 → 3 (flywheel sections) → 7 → 10, then return to fill the arithmetic spine. If you are a number theorist first, read 0–9 with Hatcher open, and treat Chapter 10 as a speculative appendix until the checklists are green.

---

## Exercises (preview level)

**0.A.** Verify \(N(q_1 q_2)=N(q_1)N(q_2)\) for two random integer quaternions by hand or with `kingdom.core.quaternion`.  

**0.B.** In the Gradio Hopf Visualizer, load **Classic Hopf** and identify which panel corresponds most closely to Figure 0.1 versus Figure 0.2.  

**0.C.** Run `map_z_to_flywheel` for \(Z\in\{2,10,26,79\}\). Record stability scores; do **not** yet interpret them as chemical truth—only as model outputs.  

**0.D.** Write one paragraph distinguishing **Theorem / Model / Hypothesis** for: (i) four-square theorem, (ii) Hopf linking, (iii) \(W_g=350/\pi\) as a multi-domain constant.  

**0.E.** Open Hatcher TN Chapter 0 and list three pictures you expect to have quaternionic or Hopf analogues by the end of our Chapter 5.

---

## Code and asset pointers

```text
kingdom.core.quaternion      # Quaternion, from_hopf_coords, hopf_image
kingdom.core.hopf            # sample_fiber, sample_fiber_family
kingdom.core.lattice         # gauged lattice simulations
kingdom.core.flux_flywheel   # map_z_to_flywheel[_extended]
kingdom.core.constants       # WG_FROM_350_OVER_PI, W_G_LOCK, κ defaults
kingdom.viz.hopf_plotly      # portal-style multi-panel figures
```

**Figure sources (Kingdom Come):** see `figures/ATTRIBUTION.md`.

**Parallel reading:** Hatcher, *Topology of Numbers*, Chapter 0; project file `HATCHER_MAP.md`.

---

*Manuscript · Chapter 0 · Preview · Figures in `book/figures/`.*
