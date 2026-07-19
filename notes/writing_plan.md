# Writing plan

## Phase 0 — Done in scaffold

- README, TOC, Hatcher map, synopsis, chapter stubs, sources  

## Phase 1 — Narrative spine

1. ~~Expand Preface + Chapter 0 fully.~~ **Done** (`book/00_preface.md`, `book/00_preview.md`).  
2. ~~Pull figure assets from `kingdom/app/assets/` (cite, do not re-license blindly).~~ **Done** — five main figures + He/Fe aux stills in `book/figures/` (`FIGURES.md`, `ATTRIBUTION.md`).  
3. ~~Feedback polish (mission statement, Ch. 0 forward pointer, aux captions, updated TOC, OP status table).~~ **Done**.  
4. ~~Draft Chapter 1 (quaternions) + figures + labs.~~ **Done** (`book/01_quaternions.md`, `scripts/generate_ch1_figures.py`).  
5. ~~Draft Chapter 2 (Hopf) + rebuild Figs. 0.1–0.3.~~ **Done** (`book/02_hopf.md`, `scripts/generate_ch2_figures.py`).  
6. Short front-matter page: “How to Use the Figures and Code” (patterns from Ch. 0–3 now available).  
7. ~~Part II: Chapter 3 — Gauged Hopf Lattice (OP1).~~ **Done** (`book/03_gauged_hopf_lattice.md`, `lib/hopf_lattice.py`, `scripts/generate_ch3_figures.py`).  
8. ~~Chapter 4 — Symmetries of the Gauged Hopf Lattice.~~ **Done** (`book/04_symmetries.md`, Ch. 4 figures, symmetry helpers in `lib/hopf_lattice.py`).  
9. ~~Part III: Chapter 5 — Flux Topographs (OP2).~~ **Done** (`book/05_forms_topographs.md`, `lib/flux_topograph.py`, Ch. 5 figures).  
10. ~~Chapter 6 — Classification and Magic Islands (OP3).~~ **Done** (`book/06_classification.md`, classification API, Ch. 6 figures).  
11. ~~Chapter 7 — The \(Z\mapsto\) Flux Map (OP4).~~ **Done** (`book/07_representations_z_flux.md`, Ch. 7 figures, `stability_landscape_z` range API).  
12. Part IV: Chapter 8 — Composition and Class Groups (OP6).  

## Phase 2 — Hatcher lift core

4. Chapters 3–6 with parallel reading exercises (“open Hatcher §…, then do …”).  
5. Define flux topograph formally.  

## Phase 3 — Arithmetic + applications

6. Chapters 7–9.  
7. Chapter 10 with strict claim labels + Table T4 validation protocol.  

## Phase 4 — Book production

8. Convert Markdown → LaTeX (`book/latex/` later).  
9. Optional Gradio “Book Mode” page linking sections to live widgets.  
