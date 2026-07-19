# Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics

**Title:** *Kingdom Come: A Quaternionic Geometric Approach to Number Theory and Physics*  
**Short name:** QGA  
**Local root:** `~/Projects/qga/`

**Mission.** Lift Hatcher’s visual, diagrammatic number theory from the Farey plane and binary quadratic forms to unit quaternions, the Hopf fibration, and gauged flux lattices—keeping pure geometry and arithmetic defensible, and isolating physical models and observational hypotheses so they never masquerade as theorems.

## What this is

An original book and research project that **maps** Allen Hatcher’s geometric number theory (*Topology of Numbers*) onto the **quaternionic / Hopf-fibration** framework developed in [Kingdom Come](https://github.com/kinaar8340/kingdom_come).

It is **not** a modified reprint of Hatcher’s PDF. Hatcher is free to read and AMS-published; we honor that by writing a **companion extension**: same visual, diagrammatic spirit, lifted from the Farey plane and binary quadratic forms to unit quaternions \(S^3\), the Hopf fibration \(S^3 \to S^2\), and gauged flux lattices with topologically protected flywheels.

| Source | Role |
|--------|------|
| [Hatcher, *Topology of Numbers*](https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf) | Geometric backbone: Farey diagram, continued fractions, topographs, class groups |
| [Kingdom Come](https://github.com/kinaar8340/kingdom_come) | Quaternion algebra, Hopf maps, flux flywheels, Z→flux mapping, 350/π observations, Gradio viz |
| Supporting stack | `flux_hopf_lib`, `oam_flux`, `qvpic`, `hfb`, `invariant_hunt`, [`vortex_math`](https://github.com/kinaar8340/vortex_math) (Ch. 9 §9.5 · `lib/vortex_math/`) |

## Core thesis (one paragraph)

Hatcher shows that elementary number theory is spatial: mediants, zigzag paths, topographs, and \(SL(2,\mathbb{Z})\) symmetries make integers visible. Kingdom Come shows that unit quaternions and the Hopf fibration make **flux**, **stability**, and **linked periodic structure** visible in the same spirit. This book develops the lift—quaternionic norms and Hurwitz integers as the four-square upgrade of sums of two squares; Hopf fibers as the higher-dimensional analogue of Farey edges; flux topographs as Conway topographs on the gauged lattice; and the Z→flywheel map plus Magic Islands as a physical representation theory. Speculative observational claims (e.g. \(350/\pi\)) are isolated as hypotheses with explicit validation criteria.

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
├── lib/                      # pedagogical helpers
├── scripts/                  # figure generators + md_to_latex + build_latex
├── refs/
└── notes/
```

### Build the PDF

```bash
./scripts/build_latex.sh
# → book/latex/main.pdf  and  book/Kingdom_Come_QGA.pdf
```

See `book/latex/README.md` for details.

## Status

- **Scaffold + TOC + mapping:** done  
- **Manuscript body:** **Complete draft Parts I–V (Ch. 0–10)**  
- **Code/figures:** pedagogical `lib/` + figure generators under `book/figures/`  
- **GitHub:** https://github.com/kinaar8340/qga  

## Quick links

- [Table of Contents](TOC.md)
- [How to Use the Figures and Code](book/HOW_TO_USE.md)  
- [Hatcher mapping](HATCHER_MAP.md)  
- [Synopsis & assessment](SYNOPSIS.md)  
- Hatcher TN: https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf  
- Kingdom Come: https://github.com/kinaar8340/kingdom_come  
- This book: https://github.com/kinaar8340/qga  

