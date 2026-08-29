"""Lock Chapter 1 conjugate formulas. Do not rewrite the algebra."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CH1 = (ROOT / "book" / "01_quaternions.md").read_text(encoding="utf-8")


def test_norm_is_q_conjugate_not_qq():
    assert r"N(q) \;:=\; q\,\overline{q}" in CH1
    assert "N(q) = qq" not in CH1.replace(r"q\,\overline{q}", "")


def test_rho_uses_conjugate():
    assert r"\rho_q(v) \;:=\; q\, v\, q^{-1} = q\, v\, \overline{q}" in CH1


def test_exercise_1b_is_order_reversal_not_commutativity():
    assert r"\overline{q_1 q_2}=\overline{q_2}\,\overline{q_1}" in CH1
    # 1.B must not claim H is commutative
    ex_b = CH1.split("**1.B (hand).**")[1].split("**1.C")[0]
    assert "commutative" not in ex_b.lower()
    assert "order reversal" in CH1.lower() or "reversal" in CH1.lower()
