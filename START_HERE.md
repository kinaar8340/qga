# Start here (20 minutes)

This is the door into the QGA stack. Dense vision docs come second.

Spine: `qga` — manuscript + pedagogical Python  
Shared math: [`flux_hopf_lib`](https://github.com/qga-lab/flux_hopf_lib)  
Engine: [`qga_engine`](https://github.com/qga-lab/qga_engine) (scenes, Rust math) · [`qga_gpu`](https://github.com/qga-lab/qga_gpu) (frame)  
This repo: the book. Not a GPU runtime and not an empirical attack.

## 1. Claim labels (5 min)

| Label | Meaning |
|-------|---------|
| **Theorem** | Geometry or arithmetic already on this spine |
| **Model** | Dynamics or construction that *uses* the spine |
| **Hypothesis** | Observational claim that can fail |
| **Software fact** | True of current code or figures |

Full table: [book/HOW_TO_USE.md](book/HOW_TO_USE.md). Account map: [kinaar8340](https://github.com/kinaar8340/kinaar8340).

## 2. The book (5 min)

Skim [TOC.md](TOC.md) and [SYNOPSIS.md](SYNOPSIS.md), or build the PDF:

```bash
python3 -m pip install -e ".[dev]"
./scripts/build_latex.sh
# → book/latex/main.pdf
```

Public PDF: [Release draft D](https://github.com/qga-lab/qga/releases/tag/draft-D) (`Kingdom_Come_QGA.pdf`). That is the book. It is not `qga_engine` / `qga_gpu` `v0.1.0`.

Short note: [`notes/spine/`](notes/spine/) (`QGA_Spine_Note.pdf`). The book remains Release `draft-D`.

Hatcher is the geometric backbone, cited separately from Kingdom Come models: [HATCHER_MAP.md](HATCHER_MAP.md).

## 3. Python labs: Hurwitz 24 and the Hopf map (5 min)

`lib/` is pedagogical. `HURWITZ_UNITS` is a re-export of `flux_hopf_lib`. Do not treat this package as a second math core.

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest tests/test_hopf_map.py tests/test_hurwitz_fixtures.py tests/test_ch1_lock.py -q
```

## 4. One picture (5 min)

Either the public GPU demo or the tiny sculpture. Both are **Software fact**, not proofs of OP1–OP6.

```bash
git clone https://github.com/qga-lab/qga_gpu
cd qga_gpu
make demo          # windowed; Esc prints UploadStats
# or, no window / small box:
make demo-tiny
```

Pin `qga_engine@7e7866b`, `qga_gpu@b9c9994`, and `flux_hopf_lib 0.3.1`. There are no `qga_gpu` / `qga_engine` `v0.1.0` tags yet. Do not float `main`. Do not make a tag sentence true from a visuals sha.

## 5. Only then

- [`arena`](https://github.com/kinaar8340/arena) — Model `Q = Q_O + σ(Z) Q_C`, not a second spine
- [`op5`](https://github.com/kinaar8340/op5) — Appendix B empirical attack; campaign `OP5-T4-2026-09-09`
- Research harness (not this door): [notes/PIPELINES.md](notes/PIPELINES.md). Shares vertices and `hopf_map` with the book. Does **not** share a graph. OP1 stays **Open**.

Geometry libraries are MIT. Several VQC repos are PolyForm Noncommercial plus patent notice US 63/913,110. This repo is MIT.
