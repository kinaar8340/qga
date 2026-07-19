# Appendix A — Terminology and Notation

Nonstandard terms and the minimal notation sheet used throughout the book. (Expanded from the Preface and `HOW_TO_USE.md`.)

---

## A.1 Claim labels

| Label | Meaning |
|-------|---------|
| **Theorem** | Proved here or classical |
| **Model** | Consistent construction; not claimed as nature’s unique law |
| **Hypothesis** | Observational claim needing validation or falsification |
| **Software fact** | True of the current code or portal implementation |

---

## A.2 Nonstandard terminology

| Term | Working meaning |
|------|-----------------|
| **Gauged Hopf lattice** | Discrete point set in \(S^3\) (or dynamics on site quaternions) with Hopf projection, adjacency, and left/right gauge actions |
| **Flux flywheel** | Closed, topologically protected circulating flux configuration on the lattice |
| **Flux topograph** | Value landscape of a flux functional on lattice sites/edges, with separators (lift of Conway topographs) |
| **Magic Island** | Region of enhanced stability / periodicity in parameter or \(Z\) space (Model) |
| **Porous vacuum** | Informal name for incomplete / gauge-flexible ambient lattice substrate |
| **Separator structure** | Locus where a flux functional changes sign or crosses a threshold |
| **Class-group analogue** | Equivalence classes of reduced topographs/flywheels with a candidate composition law (Model; OP6) |
| **Class-number analogue** | Count of inequivalent reduced representatives (`class_number_analogue`) |
| **\(Z\mapsto\) map** | Portal map from atomic number to flywheel metrics (`map_z_to_flywheel`) |
| **Table T4** | Pre-registered validation checklist for Hypotheses (Ch. 10, Appendix D) |
| **QVPIC** | Quaternion vortex persistent identity (related Kingdom Come / QVPIC work; optional cross-reference) |
| **\(W_g\)** | Working topological clock \(350/\pi \approx 111.408\) (Hypothesis layer) |

---

## A.3 Notation sheet

| Symbol | Meaning |
|--------|---------|
| \(\mathbb{H}\) | Hamilton quaternions |
| \(S^3\) | Unit quaternions |
| \(h:S^3\to S^2\) | Hopf map |
| \(N(q)=q\overline{q}\) | Multiplicative (squared) norm |
| \(\mathcal{H}\) | Hurwitz order |
| \(L=\mathbb{Z}[i,j,k]\) | Lipschitz order |
| \(\Lambda_0\) | \(\mathcal{H}\cap S^3\) (24 units) |
| \(\Lambda_{\mathrm{ang}}\) | Angle-sampled lattice |
| \(\Lambda_{\mathrm{dyn}}\) | Two-gyro dynamical sites |
| \(E_\parallel, E_\perp\) | Along-fiber / inter-fiber edges |
| \(\bigl(\frac{a,b}{\mathbb{Q}}\bigr)\) | Quaternion algebra over \(\mathbb{Q}\) |
| OP1–OP6 | Open problems (Appendix B) |

---

## A.4 Software path cheat sheet

| Path | Role |
|------|------|
| `lib/hopf_lattice.py` | Lattice, adjacency (OP1), gauge sequences |
| `lib/flux_topograph.py` | Topographs, classification (OP2–OP3) |
| `lib/composition.py` | Composition, class-group analogue (OP6) |
| `lib/quaternion_algebra.py` | Algebras, Hurwitz, toy class number |
| `lib/validation.py` | Table T4, OP5 diagnostics |
| `kingdom.core.*` | Live portal modules |
| `kingdom.simulations.lattice` | `TwoGyroLattice` |

---

*Manuscript · Appendix A · Terminology and Notation.*
