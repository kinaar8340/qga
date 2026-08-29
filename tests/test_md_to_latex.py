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
