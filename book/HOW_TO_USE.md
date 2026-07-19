# How to Use the Figures and Code

This short front-matter page is the practical companion to the Preface. It fixes the conventions used in every chapter so figures render correctly and labs stay reproducible. For navigation, start with root `TOC.md`; for Hatcher’s book in parallel, use `HATCHER_MAP.md`.

---

## 1. Claim labels

Every major claim in the manuscript is one of four kinds:

| Label | Meaning | Example |
|-------|---------|---------|
| **Theorem** | Proved in this book or classical | Four-square theorem; Hopf linking; Hurwitz class number 1 |
| **Model** | Consistent mathematical or physical construction; not claimed as nature’s unique law | Gauged Hopf lattice adjacency; flux topographs; \(Z\mapsto\) proxy |
| **Hypothesis** | Observational claim needing validation or falsification | Multi-domain \(350/\pi\) as one topological clock |
| **Software fact** | True of the current code or portal implementation | `map_z_to_flywheel` returns `stability_score`; there is **no** `magic_flag` key |

**Rule of thumb.** Geometry and classical algebra → Theorem. Lattice / topograph design choices → Model. Portal numerics about the physical world → Hypothesis. “What this function returns today” → Software fact.

Validation protocols for Hypotheses live in Chapter 10 (Table **T4**) and `lib/validation.py`.

---

## 2. Repository layout

| Path | Role |
|------|------|
| `book/*.md` | Manuscript (Preface, HOW_TO_USE, Chapters 0–10) |
| `book/figures/` | Static figures · `ATTRIBUTION.md` |
| `lib/` | Pedagogical helpers (not a replacement for Kingdom Come) |
| `scripts/generate_chN_figures.py` | Regenerate chapter figures |
| `TOC.md` · `HATCHER_MAP.md` · `notes/open_problems.md` | Navigation and open research edges |
| https://github.com/kinaar8340/qga | Canonical remote for this book |

**Live portal and domain code** (separate repo):

| Resource | Location |
|----------|----------|
| Kingdom Come | `~/Projects/kingdom/` · https://github.com/kinaar8340/kingdom_come |
| Shared Hopf / quaternion core | `flux_hopf_lib` |

---

## 3. Running the labs

### 3.1 Book helpers (`lib/`)

From the repository root:

```bash
cd ~/Projects/qga   # or your clone path
python3 -c "from lib.hopf_lattice import HURWITZ_UNITS; print(len(HURWITZ_UNITS))"
# → 24
```

Chapter labs often use an explicit path insert (adjust if your clone is elsewhere):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "Projects" / "qga"))

from lib.hopf_lattice import HURWITZ_UNITS, sample_angle_lattice
from lib.flux_topograph import build_flux_topograph
from lib.composition import compose_flywheels
from lib.quaternion_algebra import HurwitzOrder
from lib.validation import table_t4_checklist, run_table_t4_demo
```

| Package | Chapters | Purpose |
|---------|----------|---------|
| `lib.hopf_lattice` | 3–4 | Hurwitz units, angle lattice, adjacency (OP1), gauge sequences |
| `lib.flux_topograph` | 5–7 | Topographs, separators, classification, Magic Island scores |
| `lib.composition` | 8 | Flywheel composition, class-group analogue (OP6) |
| `lib.quaternion_algebra` | 9 | Quaternion algebras, Hurwitz order, toy class number |
| `lib.validation` | 10 | Table T4 checklist, Fisher combine, \(W_g\) diagnostics |

### 3.2 Kingdom Come / portal modules

```bash
export PYTHONPATH=~/Projects/kingdom/src:~/Projects/flux_hopf_lib/src
# recommended: kingdom venv
~/Projects/kingdom/.venv/bin/python -c "from kingdom.core.hopf import sample_fiber; print('ok')"
```

| Chapter | Primary modules |
|---------|-----------------|
| 1 | `kingdom.core.quaternion` |
| 2 | `kingdom.core.hopf`, `kingdom.viz.hopf_plotly` |
| 3–4 | `lib.hopf_lattice`, `kingdom.simulations.lattice.TwoGyroLattice` |
| 5–6 | `lib.flux_topograph` |
| 7 | `kingdom.core.flux_flywheel` · `lib.flux_topograph.stability_landscape_z` |
| 8 | `lib.composition` |
| 9 | `lib.quaternion_algebra` |
| 10 | `lib.validation` |

### 3.3 API honesty (read once, save time)

These mismatch the sketch names that appear in early brainstorms; the manuscript and labs follow the **live** APIs:

| Do use | Do not assume |
|--------|----------------|
| `stability_score`, `stability_class`, `is_noble_gas` | `magic_flag` |
| `TwoGyroLattice.step_frame()` | `.step()` |
| `hopf_map(x1,x2,x3,x4)`, `hopf_map_quaternion`, `Quaternion.hopf_image()` | `hopf_map(q)` as a Quaternion object |
| `sample_fiber(...)` → **dict** of arrays | bare list of quaternions |
| `map_z_to_flywheel` / `map_z_to_flywheel_extended` | undocumented extra keys |

---

## 4. Figures

1. **Paths.** In chapter markdown, figure paths are relative to `book/`:  
   `figures/fig0_1_hopf_linked_fibers.png`.
2. **Index.** Full figure list: `book/FIGURES.md`.  
3. **Attribution.** Sources and regenerate commands: `book/figures/ATTRIBUTION.md`.  
4. **Regenerate.** From repo root:
   ```bash
   python3 scripts/generate_ch1_figures.py   # example
   # Chapters 7 and 10 may need the kingdom venv for live stability scores:
   ~/Projects/kingdom/.venv/bin/python scripts/generate_ch7_figures.py
   ```
5. **Origins.** Chapter 0 partly vendors Kingdom Come assets; later chapters are mostly generated by the scripts above.

Naming pattern: `fig{N}_{k}_…` for main figures, `aux{N}_{k}_…` for auxiliary figures, `aux_z_map_*.png` for Z-map stills.

---

## 5. Notation (minimal sheet)

| Symbol | Meaning |
|--------|---------|
| \(\mathbb{H}\), \(S^3\) | Quaternions; unit quaternions |
| \(h:S^3\to S^2\) | Hopf map |
| \(\Lambda_0\) | 24 Hurwitz units on \(S^3\) |
| \(\Lambda_{\mathrm{ang}}\) | Angle-sampled lattice (visualization density) |
| \(\Lambda_{\mathrm{dyn}}\) | Dynamical two-gyro sites (portal) |
| \(W_g\) | \(350/\pi\) topological clock (**Hypothesis** layer; Ch. 10) |
| OP1–OP6 | Open problems · `notes/open_problems.md` |

---

## 6. Gradio portal ↔ book

| Portal tab | Primary chapters |
|------------|------------------|
| Hopf Visualizer | 0, 2 |
| Lattice Simulator | 3–4 |
| Flux Flywheel | 0, 5–7, 10 |
| Observations | 10 |
| The Model / theory | Preface, 0 |

---

## 7. Parallel reading with Hatcher

Keep *Topology of Numbers* open beside this book. Full map: root `HATCHER_MAP.md`.

| Hatcher TN | This book |
|------------|-----------|
| Ch. 0 Preview | Ch. 0 |
| Ch. 1–3 Farey, CF, symmetries | Ch. 3–4 (after Ch. 1–2 foundations) |
| Ch. 4–6 Forms, classification, representations | Ch. 5–7 |
| Ch. 7–8 Class group, quadratic fields | Ch. 8–9 |
| *(no TN counterpart)* | Ch. 1–2 foundations; Ch. 10 observations |

---

## 8. Appendices (expanded back matter)

Long listings and reference material live in appendices so the main chapters stay readable:

| App | Content |
|-----|---------|
| **A** | Terminology and notation |
| **B** | Open Problems OP1–OP6 (full statements) |
| **C** | Laboratory code reference (full listings) |
| **D** | Table T4 validation protocols (full) |
| **E** | Figure atlas |
| **F** | Hatcher parallel dictionary |

Chapters keep short lab “calls” and point here for copy-paste scripts.

---

## 9. Suggested first hour

1. Read the Preface and this page.  
2. Open Chapter 0; confirm figures render under `book/figures/`.  
3. Run `from lib.hopf_lattice import HURWITZ_UNITS` (expect 24).  
4. Optionally open the Gradio Hopf Visualizer and match panels to Figures 0.1–0.3 / Chapter 2.  
5. When ready for research edges, skim **Appendix B** (or `notes/open_problems.md`).

---

*Manuscript · Front matter · How to Use the Figures and Code.*
