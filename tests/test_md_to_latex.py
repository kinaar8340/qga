"""Converter guards: no '?' black-hole, no baked section numbers in \\section."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "md_to_latex", ROOT / "scripts" / "md_to_latex.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


def test_pi_is_not_question_mark():
    out = mod.convert_inline("clock 350/π and π-cycle")
    assert "?" not in out
    assert r"\pi" in out


def test_ch1_overlines_survive():
    src = r"\(N(q)=q\overline{q}\) and \(\overline{q_1 q_2}=\overline{q_2}\,\overline{q_1}\)"
    out = mod.convert_inline(src)
    assert r"\overline{q}" in out
    assert r"\overline{q_1 q_2}" in out
    assert "?" not in out


def test_mapsto_and_overline_unicode():
    out = mod.convert_inline("f ↦ g and a combining " + "\u203e")
    assert "?" not in out
    assert r"\mapsto" in out


def test_strip_baked_section_numbers():
    assert mod.strip_baked_heading_number("2.1 Definition of the Hopf fibration") == (
        "Definition of the Hopf fibration"
    )
    assert mod.strip_baked_heading_number("C.1 Chapters 1–2 (foundations)") == (
        "Chapters 1–2 (foundations)"
    )
    assert mod.strip_baked_heading_number("Chapter 2 — The Hopf Fibration") == (
        "The Hopf Fibration"
    )


def test_listing_does_not_replace_pi_with_question():
    assert "pi" in mod.listing_ascii("350/π")
    assert "?" not in mod.listing_ascii("350/π")


def test_listing_spells_xi_not_codepoint():
    assert mod.listing_ascii("ξ2-circle at fixed (η, ξ1)") == "xi2-circle at fixed (eta, xi1)"
    assert "[U+" not in mod.listing_ascii("ξ2-circle")


def test_bold_wrapping_math_does_not_leave_markdown():
    src = r"traces the **angle-chart \(\xi_2\)-circle**. That is **not** the fiber."
    out = mod.convert_inline(src)
    assert "**" not in out
    assert r"\textbf{" in out
    assert r"\xi_2" in out
    assert r"\textbf{not}" in out


def test_figure_caption_strips_manuscript_number():
    body = mod.figure_caption_text(
        "Figure 0.4 — Flux flywheel scales.",
        "*Figure 0.4.* Nested / multi-scale flywheel imagery.",
    )
    assert not body.lower().startswith("figure")
    assert "Nested" in body
    aux = mod.figure_caption_text(
        "Auxiliary Figure A0.1 — Helium still.",
        r"*Auxiliary Figure A0.1 — Helium (\(Z=2\)).* Flux-flywheel element card.",
    )
    assert ".*" not in aux
    assert "Helium" in aux
    assert "Flux-flywheel" in aux


def test_manuscript_footer_is_dropped():
    tex = mod.convert_file(ROOT / "book" / "00_preface.md", "front", "ch:preface")
    assert "figures/\\allowbreak{}}." not in tex
    assert "Manuscript" not in tex or "Full draft" not in tex


def test_ch2_has_no_leftover_markdown_or_double_caption():
    tex = mod.convert_file(ROOT / "book" / "02_hopf.md", "chapter", "ch:ch02_hopf")
    assert "**angle-chart" not in tex
    assert r"\caption{Figure 2." not in tex
    assert "[U+" not in tex


def test_app_c_listings_spell_xi():
    tex = mod.convert_file(
        ROOT / "book" / "C_lab_code_reference.md", "appendix", "ch:app_c"
    )
    assert "[U+03BE]" not in tex
    assert "[U+03B7]" not in tex
    assert "xi2-circle" in tex
