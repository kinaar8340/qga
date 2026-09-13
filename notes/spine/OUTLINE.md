# Outline — QGA Spine Note: Quaternion Orders, Hopf, and the Hatcher Lift

Working title accepted. Home: `qga-lab/qga` / `notes/spine/`.  
This file is the outline only. No body, no LaTeX, no doors, no OP1 status bump.

**This note is not the book.** The book remains *Kingdom Come* (`book/*.md`, Release `draft-D`). This is a 12–20 page extract. It is not a crate. crates.io and OP1 (canonical adjacency) wait on the finished note; they are not this outline.

Pins (one sentence in the note; do not float `main`): `flux_hopf_lib` `v0.3.1` / `0.3.1`, `qga_engine@7e7866b`, `qga_gpu@b9c9994`, book `draft-D`.

---

## Page budget

| Block | Pages | Role |
|-------|-------|------|
| Body §§1–5 | 12–16 | Theorems, classical arithmetic, SoT Software facts |
| Marked appendix | 3–5 | Models, Hypotheses, lab Software facts |
| **Total** | **12–20** | Two-pass PDF later: `notes/spine/QGA_Spine_Note.pdf` ≠ `draft-D` |

---

## Body (theorems)

### §1 Claim labels (~1 p)

Same four labels as `book/HOW_TO_USE.md` §1 and the README table.

| Label | In this note |
|-------|----------------|
| **Theorem** | Geometry or arithmetic already on the spine |
| **Model** | Construction that uses the spine — **appendix only** |
| **Hypothesis** | Observational claim that can fail — **appendix only** |
| **Software fact** | True of current SoT code (`flux_hopf_lib` 0.3.1 listing order, call signatures) |

Cite: `book/HOW_TO_USE.md`, `README.md`.

### §2 Quaternion orders (~3–4 pp)

From `book/01_quaternions.md`.

- \(\mathbb{H}\), conjugate, multiplicative norm (§1.1–1.2).
- \(S^3\subset\mathbb{H}\) (§1.3).
- Lipschitz vs Hurwitz orders (§1.4). Cardinality of the 24 Hurwitz units is a **Theorem**. The listing order of `HURWITZ_UNITS` is a **Software fact** of `flux_hopf_lib==0.3.1` (minus-then-plus axes, then \((\pm1\pm i\pm j\pm k)/2\) in `itertools.product` order). Pedagogical re-export: `lib/hopf_lattice.py`. Not a GPU constant.
- Four-square theorem via the multiplicative norm (§1.5) — **Theorem**.
- Double cover \(\mathrm{Spin}(3)\to SO(3)\) (§1.6) only as much as the Hopf section needs.

**Keep out of the body:** §1.4 “Why prefer Hurwitz later?” (**Model**); portal labs.

Cite: `book/01_quaternions.md` §§1.1–1.5; `flux_hopf_lib` 0.3.1.

### §3 Classical Hopf map (~3–4 pp)

From `book/02_hopf.md`.

- Complex-pair and real four-vector forms (§2.1). Formula as in the book and the lib:

  \[
  y_1=2(x_1 x_3+x_2 x_4),\quad
  y_2=2(x_1 x_4-x_2 x_3),\quad
  y_3=x_1^2+x_2^2-x_3^2-x_4^2.
  \]

- Unit input is **not** re-normalized by \(\|y\|\). SoT: `flux_hopf_lib.hopf.fibration.hopf_map` (alias `hopf_map_classical`). Book helper re-exports it. Do not fork.
- `legacy_portal_map` is **not** Hopf (§2.1).
- Fibers are circles; Hopf invariant \(=1\) as classical topology (§2.2).
- Structure-group \(U(1)\) fiber vs angle-chart \(\xi_2\)-circle (§2.1): the latter is **not** the Hopf fiber. Needed so OP1 Models are not smuggled in as Hopf.

**Keep out of the body:** portal layout (§2.3), gauged-lattice adjacency.

Cite: `book/02_hopf.md` §§2.1–2.2 (and §2.5 only for “one fiber per unit quaternion”); lib `v0.3.1`.

### §4 Hatcher as method, not reprint (~2–3 pp)

- Cite Hatcher’s *Topology of Numbers* (free PDF). No Hatcher prose, figures, or exercises.
- The lift is **Farey plane → \(S^3\) / Hopf**, not a unique mediant rule. TOC: Parts I–II and IV are the geometric/arithmetic spine; that split is the point of this note.
- Hurwitz lattice inside \(S^3\) as discrete points on the theorem side: `book/03_gauged_hopf_lattice.md` **§3.1 only** (24-cell / \(\Lambda_0\); Hopf image of \(\Lambda_0\) is the octahedron poles — Theorem). Density-beyond-24 and §3.2 adjacency stay out.
- Comparison with Hatcher’s LFTs as **analogy**: `book/04_symmetries.md` **§4.2**. Left/right unit multiplications are not claimed to be \(SL(2,\mathbb{Z})\).

Cite: `HATCHER_MAP.md`; `TOC.md` architecture table; `book/03_gauged_hopf_lattice.md` §3.1; `book/04_symmetries.md` §4.2; `book/F_hatcher_dictionary.md` as pointer only.

### §5 What stays open (~1–2 pp)

OP1 stays **Open**. Pointer, not a proof.

- Home: Ch. 3 **§3.5** (`book/03_gauged_hopf_lattice.md`). Ledger: `notes/open_problems.md`, `book/B_open_problems.md`.
- Two adjacency **Models** exist. Frozen book default `candidate_adjacency` is a **Software fact** of `lib/hopf_lattice.py` (figures, golden test), not a theorem. Model 2 (`structure_group`) is not canonical. Slice A is a named \(\mathbb{P}^1(\mathbb{C})\) overlap, not \(\mathbb{Q}\cup\{\infty\}\).
- Harness JSON and keep-rate tables do **not** enter this body. `notes/PIPELINES.md` is the lab notebook, not this paper.

Cite: `book/03_gauged_hopf_lattice.md` §3.5; `notes/open_problems.md` OP1 row.

---

## Marked appendix (Models / Hypotheses)

Header must say **Appendix — Models and hypotheses**. Nothing here is a QGA theorem.

| App. § | Content | Cite | Label |
|--------|---------|------|-------|
| A.1 | Gauged Hopf lattice adjacency family (OP1) | Ch. 3 §3.2, §3.5; `lib/hopf_lattice.py` | Model |
| A.2 | Flux topographs, Magic Islands, \(Z\mapsto\) flywheel | Ch. 5 §§5.1–5.3 (OP2); Ch. 6 §6.3 (H3/OP3); Ch. 7 §7.1 (OP4); Ch. 8–9 (OP6) | Model / Hypothesis |
| A.3 | \(W_g=350/\pi\) | Ch. 10 §10.1, §10.5; `op5` campaign `OP5-T4-2026-09-09` | Hypothesis; **Partial result**, not a lattice theorem |
| A.4 | Arena mix \(Q=Q_O+\sigma(Z)Q_C\) | `kinaar8340/arena`; README “Spine vs not” | Model |
| A.5 | Compatibility pins | engine `7e7866b`, gpu `b9c9994`, lib `0.3.1`, book `draft-D` | Software fact of the stack |

Ch. 3 §3.3–3.4 (gauge dynamics, flywheels), Ch. 4 §4.3–4.4, Ch. 7 §7.3–7.4 chemistry/electron clouds: appendix or omit. Do not lead.

---

## Forbidden in the body

- Model as Theorem (adjacency, topographs, flywheels, \(Z\mapsto\), \(W_g\), arena mix)
- Harness JSON (`notes/op1_runs/`, `notes/op2_runs/`) or closing OP1
- Hatcher reprint or copied figures
- Leading with toe / mystery / hfb / invariant_hunt
- New Parts of the book; this PDF as `draft-D`; `--fast` CI artifact as this note
- crates.io; engine/gpu `v0.1.0`; retag `v0.3.1`; float `main`

---

## Next turn (after this outline is accepted)

`notes/spine/spine.md` + `notes/spine/appendix_models.md` only. Still no LaTeX until those exist. Still no `START_HERE` / README door sentence until the markdown exists.
