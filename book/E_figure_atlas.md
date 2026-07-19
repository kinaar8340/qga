# Appendix E — Figure Atlas

Index of main and auxiliary figures. Paths are relative to `book/figures/`. Full attribution: `figures/ATTRIBUTION.md`. Regenerate with `scripts/generate_chN_figures.py`.

---

## E.1 By chapter

### Chapter 0
| ID | File |
|----|------|
| Fig. 0.1–0.5 | `fig0_1_…` … `fig0_5_…` |
| Aux A0.1–A0.2 | `aux_z_map_he.png`, `aux_z_map_fe.png` |

### Chapters 1–2
| ID | File |
|----|------|
| Fig. 1.1–1.4, Aux A1.1 | `fig1_*`, `aux1_1_*` |
| Fig. 2.1–2.4, Aux A2.1–A2.2 | `fig2_*`, `aux2_*` |

### Chapters 3–4
| ID | File |
|----|------|
| Fig. 3.1–3.5, Aux A3.1 | `fig3_*`, `aux3_1_*` |
| Fig. 4.1–4.4, Aux A4.1 | `fig4_*`, `aux4_1_*` |

### Chapters 5–7
| ID | File |
|----|------|
| Fig. 5.1–5.4, Aux A5.1 | `fig5_*`, `aux5_1_*` |
| Fig. 6.1–6.4, Aux A6.1 | `fig6_*`, `aux6_1_*` |
| Fig. 7.1–7.4, Aux A7.1 | `fig7_*`, `aux7_1_*`, `aux_z_map_au.png` |

### Chapters 8–10
| ID | File |
|----|------|
| Fig. 8.1–8.4, Aux A8.1 | `fig8_*`, `aux8_1_*` |
| Fig. 9.1–9.5, Aux A9.1 | `fig9_*`, `aux9_1_*` |
| Fig. 10.1–10.4, Aux A10.1 | `fig10_*`, `aux10_1_*` |

---

## E.2 Naming conventions

- Main figures: `fig{N}_{k}_descriptive_name.png`  
- Auxiliary: `aux{N}_{k}_…` or `aux_z_map_*.png`  
- In LaTeX: `\includegraphics{…}` with `graphicspath` → `figures/`  
- Labels: `\label{fig:filename-stem}`

---

## E.3 Portal sources (selected)

| Book figure | Kingdom Come source (if vendored) |
|-------------|-----------------------------------|
| Fig. 0.1 | `app/assets/home/hopf_linked_fibers.png` |
| Fig. 0.2 | `app/assets/hopf_preview.png` |
| Fig. 0.3 | `app/assets/home/hopf_fibration_bundle.png` |
| Fig. 0.4–0.5 | `app/assets/bitcoin_pi/…` |
| Aux A10.1 | `app/assets/pulsars/…`, `app/assets/bitcoin_pi/…` |
| Aux A7.1 | `z_knowns/frame_*.png` |

Generated diagrams (most of Ch. 1–10) are produced by `scripts/generate_chN_figures.py`.

---

*Manuscript · Appendix E · Figure Atlas.*
