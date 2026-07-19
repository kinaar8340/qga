#!/usr/bin/env bash
# Build the QGA book PDF from Markdown sources.
# Usage (from repo root or this script's location):
#   ./scripts/build_latex.sh
#   ./scripts/build_latex.sh --fast    # single pdflatex pass
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LATEX="$ROOT/book/latex"
cd "$ROOT"

echo "==> Converting Markdown → LaTeX"
python3 "$ROOT/scripts/md_to_latex.py"

# Ensure figures are visible to the compiler
if [[ ! -e "$LATEX/figures" ]]; then
  ln -sfn "$ROOT/book/figures" "$LATEX/figures"
fi

cd "$LATEX"
ENGINE="${LATEX_ENGINE:-pdflatex}"
FLAGS="-interaction=nonstopmode -halt-on-error -file-line-error"

echo "==> Compiling with $ENGINE"
$ENGINE $FLAGS main.tex

if [[ "${1:-}" != "--fast" ]]; then
  echo "==> Second pass (TOC / refs)"
  $ENGINE $FLAGS main.tex
fi

if [[ -f main.pdf ]]; then
  SIZE=$(wc -c < main.pdf)
  PAGES=$(pdfinfo main.pdf 2>/dev/null | awk '/Pages/ {print $2}' || echo "?")
  echo "==> OK: $LATEX/main.pdf  (${SIZE} bytes, pages=${PAGES})"
  # Convenience copy at book/
  cp -f main.pdf "$ROOT/book/Kingdom_Come_QGA.pdf"
  echo "==> Copied to book/Kingdom_Come_QGA.pdf"
else
  echo "ERROR: main.pdf not produced" >&2
  exit 1
fi
