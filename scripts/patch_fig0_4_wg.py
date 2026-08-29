#!/usr/bin/env python3
"""Redraw Fig. 0.4 so the glyph is W_g = 350/π, not 350π.

Overpaints the old serif formula on the flywheel still and composites
matplotlib mathtext. Exact glyph, not an image-model rewrite.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import numpy as np
from matplotlib.mathtext import math_to_image
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "book" / "figures" / "fig0_4_flux_flywheel_scales.jpg"
KINGDOM = (
    Path.home()
    / "Projects"
    / "kingdom"
    / "app"
    / "assets"
    / "bitcoin_pi"
    / "flux_flywheel_scales.jpg"
)

# Cream matching the original serif; dark fill from the surrounding field.
_TEXT = (255, 234, 221)
_FORMULA = r"$W_g = 350/\pi$"


def _fill_band(arr: np.ndarray, y0: int, y1: int, x0: int, x1: int) -> None:
    """Paint a smooth field over the old formula so no glyph ghosts remain."""
    below = arr[min(arr.shape[0] - 1, y1 + 8) : min(arr.shape[0], y1 + 24), x0:x1]
    above = arr[max(0, y0 - 18) : max(1, y0 - 6), x0:x1]
    fill = below.mean(axis=(0, 1)) if below.size else above.mean(axis=(0, 1))
    # Soft horizontal vignette so the patch meets the dark field
    width = x1 - x0
    height = y1 - y0
    xs = np.linspace(-1.0, 1.0, width)
    edge = np.clip((np.abs(xs) - 0.82) / 0.18, 0.0, 1.0)
    for i in range(height):
        src = arr[y0 + i, x0:x1].astype(np.float32)
        mixed = src * edge[:, None] + fill * (1.0 - edge)[:, None]
        arr[y0 + i, x0:x1] = mixed.astype(np.uint8)


def _mathtext_rgba(expr: str, fontsize: int = 28) -> Image.Image:
    tmp = ROOT / "book" / "figures" / ".fig0_4_glyph.png"
    math_to_image(expr, str(tmp), prop=None, dpi=160, format="png")
    # math_to_image writes its own figure; colorize onto transparent RGBA
    glyph = Image.open(tmp).convert("L")
    tmp.unlink(missing_ok=True)
    g = np.array(glyph)
    # mathtext is black on white; invert to cream on transparent
    alpha = (255 - g).astype(np.uint8)
    rgba = np.zeros((g.shape[0], g.shape[1], 4), dtype=np.uint8)
    rgba[..., 0] = _TEXT[0]
    rgba[..., 1] = _TEXT[1]
    rgba[..., 2] = _TEXT[2]
    rgba[..., 3] = alpha
    return Image.fromarray(rgba, "RGBA")


def patch(path: Path) -> None:
    im = Image.open(path).convert("RGB")
    arr = np.array(im)
    # Formula lives just under the tick bar (y ≈ 590–629, centered).
    _fill_band(arr, 585, 648, 260, 764)
    base = Image.fromarray(arr, "RGB").convert("RGBA")
    glyph = _mathtext_rgba(_FORMULA)
    # Scale glyph to ~38% of image width
    target_w = int(base.width * 0.38)
    scale = target_w / glyph.width
    target_h = max(1, int(glyph.height * scale))
    glyph = glyph.resize((target_w, target_h), Image.Resampling.LANCZOS)
    x = (base.width - glyph.width) // 2
    y = 592
    base.alpha_composite(glyph, (x, y))
    out = base.convert("RGB")
    out.save(path, quality=95, subsampling=0)
    print(f"wrote {path} ({out.size[0]}x{out.size[1]})")


def main() -> int:
    patch(SRC)
    if KINGDOM.exists():
        patch(KINGDOM)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
