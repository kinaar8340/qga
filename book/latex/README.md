# LaTeX build for *Kingdom Come* (QGA)

Professional book PDF generated from the Markdown manuscript in `book/*.md`.

## Requirements

- TeX Live with `pdflatex` (or `lualatex`)
- Packages: `book`, `amsmath`, `hyperref`, `graphicx`, `booktabs`, `listings`, `fancyhdr`, `cleveref`, …
  (standard `texlive-latex-recommended` + `texlive-latex-extra` on Debian/Ubuntu)
- Python 3 (for `scripts/md_to_latex.py`)

## Quick build

From the **repository root**:

```bash
./scripts/build_latex.sh
```

Outputs:

| File | Description |
|------|-------------|
| `book/latex/main.pdf` | Primary PDF |
| `book/Kingdom_Come_QGA.pdf` | Convenience copy |

Single-pass (no TOC refresh):

```bash
./scripts/build_latex.sh --fast
```

## Workflow

1. **Edit Markdown** in `book/*.md` (source of truth).
2. **Regenerate TeX chapters**: `python3 scripts/md_to_latex.py`  
   Writes `book/latex/chapters/*.tex` (auto-generated — do not hand-edit).
3. **Compile**: `pdflatex main.tex` twice from `book/latex/`.

Figures are resolved via `figures/` → symlink to `book/figures/`.

## Structure

```
book/latex/
├── main.tex          # Master document (parts, includes, appendices)
├── preamble.tex      # Packages, macros, listings style
├── chapters/         # Generated chapter + appendix .tex files
├── figures/          # Symlink → ../figures
├── main.pdf          # Build product
└── README.md         # This file
```

Appendices A–F are generated from `book/A_*.md` … `book/F_*.md` (terminology, open problems, lab code, Table T4, figure atlas, Hatcher dictionary).

## Cross-references

- Each chapter file gets `\label{ch:…}` (e.g.\ `ch:ch01_quaternions`).
- Sections get `\label{ch:…:section-slug}`.
- Figures get `\label{fig:filename-stem}`.
- Use `\ref{…}` / `\cref{…}` (cleveref) in hand-written TeX appendices.

Regenerating from Markdown overwrites chapter files; keep custom TeX only in
`main.tex`, `preamble.tex`, or new non-generated inputs.

## Engines

Default engine is `pdflatex`. For LuaLaTeX:

```bash
LATEX_ENGINE=lualatex ./scripts/build_latex.sh
```

(You may need to adjust font setup in `preamble.tex` for pure LuaLaTeX fonts.)

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Missing figures | `ln -sfn ../figures figures` inside `book/latex/` |
| TOC empty / wrong | Run `pdflatex` twice |
| Unicode errors | Prefer ASCII math; or switch to `lualatex` + fontspec |
| `listings` chokes on code | Escape rare characters in source fences, or re-run converter |

## Relation to Markdown draft

| Layer | Role |
|-------|------|
| `book/*.md` | Authoring / GitHub readability |
| `book/latex/` | Print / PDF production |
| `lib/` + Gradio | Executable labs and portal |
