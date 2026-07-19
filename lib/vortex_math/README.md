# `vortex_math` (supporting stack pointer)

Active development of the modulus-invariants experiment lives in the sibling repository:

**https://github.com/kinaar8340/vortex_math**  
Local path (typical): `~/Projects/vortex_math`

This directory is a **book-side pointer**, not a full vendored copy of the Python package. Keep experiments and visualizations there; cite results from Kingdom Come / QGA Chapter 9 §9.5.

## What it supports in this book

| Layer | Book home | Role |
|-------|-----------|------|
| Algebraic \(\times 2\) on \(\mathbb{Z}/m\mathbb{Z}\) | Ch. 9 §9.5 | Cleanest long cycle at \(m=37\) |
| Sequential label progression under \(m/\pi\) | Ch. 9 §9.5 | Often strongest at \(m=111\) |
| Angle–label lock (exNMI) | Ch. 9 §9.5 | Positive only for `angle_bin` control under step-index geometry |
| Research note | [`notes/RESEARCH_NOTE_moduli.md`](../../notes/RESEARCH_NOTE_moduli.md) | Full metrics and controls |
| Book figure | [`book/figures/fig9_5_modulus_invariants.png`](../../book/figures/fig9_5_modulus_invariants.png) | Fig. 9.5 |

## Quick labs (from `vortex_math` root)

```bash
cd ~/Projects/vortex_math
source .venv/bin/activate   # if present
python src/main.py --family-37 --num-steps 200
python src/main.py --resonance-scan --method step_index --num-steps 600
python src/main.py --resonance-scan --method angle_bin --num-steps 600
```

## Claim discipline

Results reported in the book as **Model** (controlled experimental separation) + **Software fact** (implementation). Not classical theorems of Hatcher *Topology of Numbers*.

Optional future work: git submodule or stable snapshot pinned here if the book build must freeze a revision.
