# Appendix — Models and hypotheses

Nothing in this appendix is a QGA theorem. The body is [`spine.md`](spine.md): quaternion orders, the classical Hopf map, Hatcher as method, and Open Problem 1 left **Open**.

Claim labels are those of `book/HOW_TO_USE.md`. **Model** = construction that uses the spine. **Hypothesis** = observational claim that can fail. **Software fact** = true of current code, figures, or pins.

Do not read this file as a status bump for OP1–OP6. Do not feed it into `flux_hopf_lib` or `qga_engine` as if adjacency were canonical.

---

## A.1 Gauged Hopf lattice adjacency (OP1 family)

**Label: Model.** Cite `book/03_gauged_hopf_lattice.md` §§3.2, 3.5; `lib/hopf_lattice.py`.

A **gauged Hopf lattice** is a working tuple \((\Lambda,\, h(\Lambda),\, E_{\parallel},\, E_{\perp},\, \mathcal{G})\): a discrete set in \(S^3\), its Hopf image, along-fiber edges, inter-fiber edges, and a group of left/right unit multiplications. That tuple is a design object. The Hopf map on \(\Lambda_0\) is a theorem of the body; the edge sets are not.

Two lattice points may be declared adjacent along a fiber or between fibers. A mediant-like rule that reduces to Hatcher’s \((a/c)\oplus(b/d)=(a+b)/(c+d)\) is exactly Open Problem 1. No single such rule is proved canonical.

`candidate_adjacency` (book default) recovers rough Hopf angles and treats the \(\xi_2\)-circle as “along.” That circle is **not** the structure-group fiber of the body. Inter-edges use an angular threshold on \(S^2\). **Software fact** of `lib/hopf_lattice.py` for figures and the golden test.

Model 2 (`structure_group_adjacency`) uses consecutive samples on true \(U(1)\) fibers. It is a second Model, not a theorem, not a promotion into the shared library. Slice A (Gaussian neighbors on \(h(\Lambda_0)\)) is a named \(\mathbb{P}^1(\mathbb{C})\) overlap, not \(\mathbb{Q}\cup\{\infty\}\).

Gauge dynamics on `TwoGyroLattice` and first-look flux flywheels (`book/03_gauged_hopf_lattice.md` §§3.3–3.4; `book/04_symmetries.md` §§4.3–4.4) are the same Model family. Linking of Hopf fibers remains a Theorem of the body; existence of flywheels as physical objects does not.

Harness JSON under `notes/op1_runs/` stays in the lab notebook (`notes/PIPELINES.md`). Not cited as evidence that OP1 is closed.

---

## A.2 Flux topographs, Magic Islands, \(Z\mapsto\) flywheel

**Label: Model / Hypothesis.** Cite Ch. 5 §§5.1–5.3 (OP2), Ch. 6 §6.3 (H3 / OP3), Ch. 7 §7.1 (OP4), Ch. 8–9 (OP6).

Hatcher’s topographs of binary quadratic forms are classical. A **flux functional** on a gauged lattice, and the **flux topograph** built from it, are Model choices for Open Problem 2 (`book/05_forms_topographs.md`). Candidate functionals in the book helper (`norm`, `hopf_y1` / `hopf_height`, `phase`, portal stability) are not unique. Separator edges and periodicity scores are experimental diagnostics.

**Magic Islands** are pockets of high `stability_score` in a parameter space (including atomic number \(Z\) in the portal Model). Visual and software properties: Model + Software fact. Correspondence with class number: Open Problem 3 / Hypothesis H3 (`book/06_classification.md` §6.3). Classical reduced forms remain theorems of Hatcher, not of this appendix.

The **\(Z\mapsto\) flywheel** map (`book/07_representations_z_flux.md` §7.1; recap Ch. 10 §10.2) is implemented (`map_z_to_flywheel`, `map_z_to_flywheel_extended`). Reproducible curves: Software fact. Physical emergence of the periodic table, uniqueness up to gauge (OP4), and chemistry-facing / electron-cloud panels (Ch. 7 §§7.3–7.4): Model / Hypothesis. Do not lead with them.

Gauss-style **composition of flywheels** (OP6, Ch. 8–9) is an open lift of classical composition. Sandbox closure in `lib/composition.py` is often low; that failure is a Software fact of the helper, not a theorem that composition does not exist.

OP2–OP4 and OP6 remain Open on `notes/open_problems.md`. This appendix does not write topograph axioms and does not open a class-number proof.

---

## A.3 \(W_g = 350/\pi\)

**Label: Hypothesis.** Cite Ch. 10 §§10.1, 10.5; [`op5`](https://github.com/kinaar8340/op5) campaign `OP5-T4-2026-09-09`.

\[
W_g = \frac{350}{\pi} \approx 111.408
\]
is **not** \(350\pi\). It is not a lattice theorem and not a HUD atmosphere.

Per-domain clustering near this constant is Hypothesis H1a–H1e (OP5), not one bundled clock. Table T4 is the validation protocol (`book/10_observations_emergent.md` §10.5; `book/D_validation_t4.md`).

**Status: Partial result** for campaign `OP5-T4-2026-09-09`. Two frames do not force \(W_g=350/\pi\). H1a–H1e under Table T4 fail to reject coincidence. Cite `op5` / `docs/OP5_RESULT.md`. First-principles derivation remains open. Door 1 (named-7 hunts) is parked. Door 2 (new T4 campaign) is idle — do not reuse H1a–H1e.

Raw portal constants are Software facts of that tree. They do not upgrade the Hypothesis.

---

## A.4 Arena mix

**Label: Model.** Cite `qga` README “Spine vs not”; [`kinaar8340/arena`](https://github.com/kinaar8340/arena).

\[
Q = Q_O + \sigma(Z)\, Q_C
\]
is a labeled Model companion. It is not a QGA theorem and not a second spine. Architecture: SoT for this mix is `arena`, not `flux_hopf_lib`, not `qga/lib`.

---

## A.5 Compatibility pins

**Label: Software fact of the stack.** Not theorems. Do not float `main`. No `v0.1.0` tags on engine or gpu. Do not retag `flux_hopf_lib` `v0.3.1`.

| Artifact | Pin |
|----------|-----|
| Book (citable PDF) | `qga-lab/qga` Release **`draft-D`**. This spine note is not that Release. CI `--fast` PDF is not that Release. |
| Shared math | `flux-hopf-lib==0.3.1`; git `qga-lab/flux_hopf_lib` annotated **`v0.3.1`** |
| Engine | `qga-lab/qga_engine@7e7866b` |
| Renderer | `qga-lab/qga_gpu@b9c9994` |

Discussion #2 (org): clone `flux_hopf_lib` at `v0.3.1`; do not float engine/gpu `main`. Engine `main` may sit ahead of `7e7866b` for CI-only SHAs; that does not move the pin and does not authorize a tag.

`inner_cone` and `shellscan` (notebook) git-pin the same two engine/gpu revs. They are consumers, not theorem sources.
