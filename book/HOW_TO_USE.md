# How to Use the Figures and Code

This front-matter page is the practical companion to the Preface. It fixes conventions used in every chapter so labs and figures stay reproducible.

---

## Claim labels

| Label | Meaning | Example |
|-------|---------|---------|
| **Theorem** | Proved in this book or classical | Four-square theorem; Hopf linking; Hurwitz class number 1 |
| **Model** | Consistent mathematical/physical construction; not claimed as nature’s unique law | Gauged Hopf lattice adjacency; flux topographs; \(Z\mapsto\) proxy |
| **Hypothesis** | Observational claim needing validation or falsification | Multi-domain \(350/\pi\) as one topological clock |
| **Software fact** | True of the current code/portal implementation | `map_z_to_flywheel` returns `stability_score`; no `magic_flag` key |

When in doubt: geometry and classical algebra → Theorem; lattice/topograph design → Model; portal numerics about nature → Hypothesis; “what the function returns” → **Software fact**.

---

## Repository layout

| Path | Role |
|------|------|
| `book/*.md` | Manuscript chapters |
| `book/figures/` | Static figures (see `ATTRIBUTION.md`) |
| `lib/` | Pedagogical helpers (not a full Kingdom Come replacement) |
| `scripts/generate_chN_figures.py` | Regenerate chapter figures |
| `TOC.md`, `HATCHER_MAP.md`, `notes/open_problems.md` | Navigation and research edges |
| https://github.com/kinaar8340/qga | Canonical remote |

Kingdom Come (live portal and domain code): `~/Projects/kingdom/` · https://github.com/kinaar8340/kingdom_come

---

## Running labs

### Book helpers (`lib/`)

From the repository root:

```bash
cd ~/Projects/qga
python3 -c "from lib.hopf_lattice import HURWITZ_UNITS; print(len(HURWITZ_UNITS))"
```

In chapter labs you will often see:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "Projects" / "qga"))

from lib.hopf_lattice import ...
from lib.flux_topograph import ...
from lib.composition import ...
from lib.quaternion_algebra import ...
from lib.validation import ...
```

Adjust the path if your clone is not under `~/Projects/qga`.

### Kingdom Come / portal modules

```bash
# typical local setup
export PYTHONPATH=~/Projects/kingdom/src:~/Projects/flux_hopf_lib/src
# or use kingdom's venv
~/Projects/kingdom/.venv/bin/python -c "from kingdom.core.hopf import sample_fiber; print('ok')"
```

| Chapter | Primary modules |
|---------|-----------------|
| 1 | `kingdom.core.quaternion` |
| 2 | `kingdom.core.hopf`, `kingdom.viz.hopf_plotly` |
| 3–4 | `lib/hopf_lattice`, `kingdom.simulations.lattice.TwoGyroLattice` |
| 5–6 | `lib/flux_topograph` |
| 7 | `kingdom.core.flux_flywheel`, `lib.validation` / `stability_landscape_z` |
| 8 | `lib/composition` |
| 9 | `lib/quaternion_algebra` |
| 10 | `lib/validation` (Table T4) |

### API honesty (recurring)

- Prefer `stability_score`, `stability_class`, `is_noble_gas` — there is **no** `magic_flag`.  
- Lattice dynamics: `TwoGyroLattice.step_frame()` (not `.step()`).  
- Hopf map: component-wise `hopf_map(x1,…)` / `hopf_map_quaternion` / `Quaternion.hopf_image()`.  
- `sample_fiber` returns a **dict** of arrays, not a bare list of quaternions.

---

## Figures

- Relative paths in markdown are from the `book/` directory: `figures/fig0_1_….png`.  
- Regenerate: `python scripts/generate_chN_figures.py` (Ch. 7/10 may need the kingdom venv for live scores).  
- Attribution and licenses: `book/figures/ATTRIBUTION.md`.  
- Chapter 0 figures partly vendor Kingdom Come assets; later chapters are mostly generated.

---

## Notation (minimal)

| Symbol | Meaning |
|--------|---------|
| \(\mathbb{H}\), \(S^3\) | Quaternions; unit quaternions |
| \(h: S^3\to S^2\) | Hopf map |
| \(\Lambda_0\) | 24 Hurwitz units |
| \(\Lambda_{\mathrm{ang}}\) | Angle-sampled lattice (visualization) |
| \(\Lambda_{\mathrm{dyn}}\) | Dynamical two-gyro sites (portal) |
| \(W_g\) | \(350/\pi\) topological clock constant (Hypothesis layer) |
| OP1–OP6 | Open problems (`notes/open_problems.md`) |

---

## Gradio portal ↔ book

| Portal tab | Chapters |
|------------|----------|
| Hopf Visualizer | 0, 2 |
| Lattice Simulator | 3–4 |
| Flux Flywheel | 0, 5–7, 10 |
| Observations | 10 |
| The Model / theory | 0, Preface |

---

## Parallel reading with Hatcher

Use root `HATCHER_MAP.md`. Short map: TN Ch. 1–3 → book Ch. 3–4; TN Ch. 4–6 → book Ch. 5–7; TN Ch. 7–8 → book Ch. 8–9; book Ch. 1–2 and 10 have no direct TN counterpart.

---

*Manuscript · Front matter · How to Use the Figures and Code.*
