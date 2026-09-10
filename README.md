# Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics

Spine: this repo — manuscript + pedagogical Python  
Shared math: [`flux_hopf_lib`](https://github.com/kinaar8340/flux_hopf_lib) — SoT for Hopf / quaternion / Hurwitz 24  
Engine: [`qga_engine`](https://github.com/kinaar8340/qga_engine) (scenes, Rust math) · [`qga_gpu`](https://github.com/kinaar8340/qga_gpu) (frame)  
This repo: the book. Not a GPU runtime and not an empirical attack.

**Start here:** [START_HERE.md](START_HERE.md)

**Title:** *Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics*  
**Short name:** QGA

**Mission.** Lift Hatcher’s visual, diagrammatic number theory from the Farey plane and binary quadratic forms to unit quaternions, the Hopf fibration, and gauged flux lattices—keeping pure geometry and arithmetic defensible, and isolating physical models and observational hypotheses so they never masquerade as theorems.

## How to read claims

| Label | Meaning | Here |
|-------|---------|------|
| **Theorem** | Geometry or arithmetic already on this spine | Quaternion orders, Hopf facts, Hatcher lift |
| **Model** | Dynamics or construction that *uses* the spine | Flux flywheels, gauged-lattice adjacency, flux topographs, \(Z\mapsto\) map, arena mix \(Q = Q_O + \sigma(Z) Q_C\) |
| **Hypothesis** | Observational claim that can fail | \(350/\pi\) (H1a–H1e); not a theorem |
| **Software fact** | True of current code or figures | What a helper or portal function returns today |

**Hatcher map.** Parallel reading: [HATCHER_MAP.md](HATCHER_MAP.md) · Hatcher’s *Topology of Numbers* ([PDF](https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf)).

**Spine vs not.** This repo is the manuscript spine. Quaternion orders, Hopf, and the Hatcher lift stay theorems. Flux flywheels, flux topographs, the \(Z\mapsto\) map, \(350/\pi\), and the arena mix are Model or Hypothesis. [arena](https://github.com/kinaar8340/arena) is a labeled Model companion; it is not a second spine.

## What this is

An original book and research project that **maps** Allen Hatcher’s geometric number theory (*Topology of Numbers*) onto unit quaternions \(S^3\), the Hopf fibration \(S^3 \to S^2\), and gauged flux lattices.

It is **not** a modified reprint of Hatcher’s PDF. Hatcher is free to read and AMS-published; this is a **companion extension** in the same visual, diagrammatic spirit.

| Source | Role |
|--------|------|
| [Hatcher, *Topology of Numbers*](https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf) | Geometric backbone: Farey diagram, continued fractions, topographs, class groups |
| [flux_hopf_lib](https://github.com/kinaar8340/flux_hopf_lib) | Shared Hopf / quaternion / conduit primitives |
| [kingdom_come](https://github.com/kinaar8340/kingdom_come) | Portal and figures for models and observations — not a theorem source |

## Core thesis (one paragraph)

Hatcher shows that elementary number theory is spatial: mediants, zigzag paths, topographs, and \(SL(2,\mathbb{Z})\) symmetries make integers visible. This book develops the lift: quaternionic norms and Hurwitz integers as the four-square upgrade of sums of two squares; Hopf fibers as the higher-dimensional analogue of Farey edges; flux topographs as Conway topographs on a gauged lattice. Flywheels, the \(Z\mapsto\) map, and Magic Islands are labeled **Models**. Speculative observational claims (e.g. \(350/\pi\)) are **Hypotheses** with explicit validation criteria.

## Project layout

```
qga/
├── README.md
├── TOC.md
├── HATCHER_MAP.md
├── SYNOPSIS.md
├── book/                     # manuscript (Markdown)
│   ├── *.md                  # chapters 0–10, preface, HOW_TO_USE
│   ├── figures/              # static figures
│   ├── latex/                # PDF production (main.tex + generated chapters)
│   └── Kingdom_Come_QGA.pdf  # latest build (also book/latex/main.pdf)
├── START_HERE.md             # 20-minute door
├── lib/                      # pedagogical-only; not a second SoT; not on PyPI
├── scripts/                  # figure generators + md_to_latex + build_latex
├── refs/
└── notes/
```

### Build the PDF

```bash
python3 -m pip install -e .
python3 -m pip install -e ".[portal]"   # flux-hopf-lib (PyPI) + kingdom-come (git pin)
./scripts/build_latex.sh
# → book/latex/main.pdf  and  book/Kingdom_Come_QGA.pdf
```

See `book/latex/README.md` for details.

## Status

- **Scaffold + TOC + mapping:** done
- **Manuscript body:** **Complete draft Parts I–V (Ch. 0–10)**
- **Code/figures:** pedagogical `lib/` (not a competing package) + figure generators under `book/figures/`
- **GitHub:** https://github.com/kinaar8340/qga

## Quick links

- [Table of Contents](TOC.md)
- [How to Use the Figures and Code](book/HOW_TO_USE.md)
- [Hatcher mapping](HATCHER_MAP.md)
- [Synopsis & assessment](SYNOPSIS.md)
- Hatcher TN: https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf
- Shared primitives: https://github.com/kinaar8340/flux_hopf_lib
- Portal: https://github.com/kinaar8340/kingdom_come
- This book: https://github.com/kinaar8340/qga

X: [@kinaar8340](https://x.com/kinaar8340)

Geometry libraries are MIT. Several VQC repos are PolyForm Noncommercial plus patent notice US 63/913,110. This repo is MIT.
