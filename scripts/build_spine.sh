#!/usr/bin/env bash
# Two-pass LaTeX for the QGA spine note (not the Kingdom Come book).
# Usage from repo root:
#   ./scripts/build_spine.sh
# Does not accept --fast. Does not write book/Kingdom_Come_QGA.pdf.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LATEX="$ROOT/notes/spine/latex"
cd "$ROOT"

if [[ "${1:-}" == "--fast" ]]; then
  echo "ERROR: spine note has no --fast path; two passes are required" >&2
  exit 2
fi

echo "==> Converting notes/spine Markdown → LaTeX"
python3 "$ROOT/scripts/spine_md_to_latex.py"

cd "$LATEX"
ENGINE="${LATEX_ENGINE:-pdflatex}"
FLAGS="-interaction=nonstopmode -halt-on-error -file-line-error"

echo "==> Compiling with $ENGINE (pass 1)"
$ENGINE $FLAGS main.tex
echo "==> Compiling with $ENGINE (pass 2, TOC / refs)"
$ENGINE $FLAGS main.tex

if [[ ! -f main.pdf ]]; then
  echo "ERROR: main.pdf not produced" >&2
  exit 1
fi

SIZE=$(wc -c < main.pdf)
PAGES=$(pdfinfo main.pdf 2>/dev/null | awk '/Pages:/ {print $2}' || echo "?")
cp -f main.pdf "$ROOT/notes/spine/QGA_Spine_Note.pdf"
echo "==> OK: notes/spine/QGA_Spine_Note.pdf  (${SIZE} bytes, pages=${PAGES})"
echo "==> This PDF is not Release draft-D and not book/Kingdom_Come_QGA.pdf"

if [[ "$PAGES" =~ ^[0-9]+$ ]]; then
  if (( PAGES < 12 || PAGES > 20 )); then
    echo "WARNING: page count ${PAGES} is outside the 12–20 budget" >&2
  fi
fi
