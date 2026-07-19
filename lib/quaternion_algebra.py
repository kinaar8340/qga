"""Quaternion algebras and orders for Kingdom Come / QGA Chapter 9.

Pedagogical helpers for classical facts about quaternion algebras over Q,
the Hurwitz order, and *toy* ideal-class diagnostics. Not a full CAS for
quaternion arithmetic (Open Problem 6 / rigorous ideal theory remains open).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Iterable

import numpy as np

from .hopf_lattice import HURWITZ_UNITS, q_mult, q_norm2, q_normalize

Array = np.ndarray


# ---------------------------------------------------------------------------
# Hilbert symbol / ramification (over Q, elementary)
# ---------------------------------------------------------------------------


def _legendre(a: int, p: int) -> int:
    """Legendre symbol (a/p) for odd prime p."""
    a %= p
    if a == 0:
        return 0
    return pow(a, (p - 1) // 2, p) if pow(a, (p - 1) // 2, p) in (0, 1) else -1


def _valuation(n: int, p: int) -> int:
    if n == 0:
        return 10**9
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def hilbert_symbol(a: int, b: int, p: int | str) -> int:
    r"""Hilbert symbol (a,b)_p ∈ {±1} for p prime or '∞'.

    Elementary implementation sufficient for small square-free a,b.
    """
    if p == "inf" or p == "∞" or p == -1:
        # (a,b)_∞ = -1 iff a<0 and b<0
        return -1 if (a < 0 and b < 0) else 1

    p = int(p)
    if p == 2:
        # (a,b)_2 = (-1)^ε(a)ε(b) * (-1)^ω(a)ω(b) with ε=(x²-1)/8, ω=(x-1)/2 mod 2
        def odd_part(x: int) -> int:
            x = abs(x)
            while x % 2 == 0:
                x //= 2
            return x

        aa, bb = odd_part(a), odd_part(b)
        # simplify using valuations
        va, vb = _valuation(abs(a) if a != 0 else 1, 2), _valuation(abs(b) if b != 0 else 1, 2)
        # standard formula for 2-adic Hilbert symbol
        e = lambda x: ((x % 8) ** 2 - 1) // 8 % 2
        o = lambda x: ((x % 8) - 1) // 2 % 2
        # use odd parts of a,b after removing 2-powers carefully
        a_odd = odd_part(a if a != 0 else 1) * (1 if a >= 0 else -1)
        b_odd = odd_part(b if b != 0 else 1) * (1 if b >= 0 else -1)
        # signs
        if a < 0:
            a_odd = -abs(a_odd)
        if b < 0:
            b_odd = -abs(b_odd)
        exp = (e(a_odd) * e(b_odd) + o(a_odd) * o(b_odd)) % 2
        # factor of 2: (2,u)_2 = (-1)^((u²-1)/8)
        if va % 2 == 1:
            exp = (exp + e(b_odd)) % 2
        if vb % 2 == 1:
            exp = (exp + e(a_odd)) % 2
        return -1 if exp else 1

    # odd prime
    va, vb = _valuation(abs(a) if a else 1, p), _valuation(abs(b) if b else 1, p)
    a0 = a // (p**va) if a else 1
    b0 = b // (p**vb) if b else 1
    # (a,b)_p = (a0/p)^{vb} (b0/p)^{va} (-1)^{va vb (p-1)/2}
    s = 1
    if vb % 2:
        s *= _legendre(a0, p)
    if va % 2:
        s *= _legendre(b0, p)
    if (va % 2) and (vb % 2) and ((p - 1) // 2 % 2):
        s *= -1
    return 1 if s >= 0 else -1


def is_square_free(n: int) -> bool:
    n = abs(n)
    if n == 0:
        return False
    p = 2
    x = n
    while p * p <= x:
        c = 0
        while x % p == 0:
            x //= p
            c += 1
            if c >= 2:
                return False
        p += 1 if p == 2 else 2
    return True


@dataclass
class QuaternionAlgebra:
    """Quaternion algebra (a,b / Q) with i²=a, j²=b, ij=-ji.

    Classical theory cited; methods are pedagogical.
    """

    a: int
    b: int

    def __post_init__(self) -> None:
        if self.a == 0 or self.b == 0:
            raise ValueError("a and b must be nonzero")

    def __repr__(self) -> str:
        return f"QuaternionAlgebra({self.a}, {self.b})"

    def presentation(self) -> str:
        return rf"({self.a},{self.b}/Q): i^2={self.a}, j^2={self.b}, ij=-ji"

    def hilbert_at(self, p: int | str) -> int:
        return hilbert_symbol(self.a, self.b, p)

    def ramified_places(
        self,
        primes: Iterable[int] | None = None,
        *,
        include_infinite: bool = True,
        prime_bound: int = 50,
    ) -> list[int | str]:
        """Return places p where (a,b)_p = -1.

        Finite primes checked among factors of 2ab and small primes up to bound.
        """
        candidates: set[int] = {2}
        n = abs(self.a * self.b) * 2
        d = 2
        x = n
        while d * d <= x:
            if x % d == 0:
                candidates.add(d)
                while x % d == 0:
                    x //= d
            d += 1 if d == 2 else 2
        if x > 1:
            candidates.add(x)
        if primes is not None:
            candidates |= set(int(p) for p in primes)
        else:
            # sieve small primes
            sieve = [True] * (prime_bound + 1)
            sieve[0] = sieve[1] = False
            for i in range(2, int(prime_bound**0.5) + 1):
                if sieve[i]:
                    for j in range(i * i, prime_bound + 1, i):
                        sieve[j] = False
            candidates |= {i for i in range(2, prime_bound + 1) if sieve[i]}

        ram: list[int | str] = []
        for p in sorted(candidates):
            if self.hilbert_at(p) == -1:
                ram.append(p)
        if include_infinite and self.hilbert_at("inf") == -1:
            ram.append("∞")
        return ram

    def is_definite(self) -> bool:
        """Definite over R iff ramified at ∞ (division algebra over R)."""
        return self.hilbert_at("inf") == -1

    def is_matrix_algebra_over_r(self) -> bool:
        return not self.is_definite()

    def element(self, w: float, x: float, y: float, z: float) -> Array:
        """Return (w,x,y,z) as coefficient vector for w + x i + y j + z ij."""
        return np.array([w, x, y, z], dtype=float)

    def multiply_coeffs(self, u: Array, v: Array) -> Array:
        """Multiply two elements in this algebra (general a,b)."""
        w1, x1, y1, z1 = u
        w2, x2, y2, z2 = v
        a, b = float(self.a), float(self.b)
        # (w1 + x1 i + y1 j + z1 ij)(w2 + x2 i + y2 j + z2 ij)
        w = w1 * w2 + a * x1 * x2 + b * y1 * y2 - a * b * z1 * z2
        x = w1 * x2 + x1 * w2 + b * y1 * z2 - b * z1 * y2
        y = w1 * y2 - a * x1 * z2 + y1 * w2 + a * z1 * x2
        z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
        return np.array([w, x, y, z], dtype=float)

    def reduced_norm(self, u: Array) -> float:
        w, x, y, z = u
        return float(w * w - self.a * x * x - self.b * y * y + self.a * self.b * z * z)


# ---------------------------------------------------------------------------
# Hurwitz / Lipschitz orders in Hamilton quaternions H = (-1,-1 / R) over Q
# ---------------------------------------------------------------------------


@dataclass
class LipschitzOrder:
    """Lipschitz order Z[i,j,k] inside Hamilton quaternions."""

    def contains(self, q: Array, tol: float = 1e-9) -> bool:
        return bool(np.all(np.abs(np.asarray(q) - np.round(q)) <= tol))

    @property
    def units(self) -> Array:
        units = []
        for i in range(4):
            for s in (-1.0, 1.0):
                v = np.zeros(4)
                v[i] = s
                units.append(v)
        return np.array(units)

    def is_euclidean(self) -> bool:
        # Lipschitz is not Euclidean for the usual quaternion norm
        return False

    def n_units(self) -> int:
        return 8


@dataclass
class HurwitzOrder:
    """Hurwitz maximal order in Hamilton quaternions (over Q-form of H)."""

    @property
    def units(self) -> Array:
        return HURWITZ_UNITS.copy()

    def n_units(self) -> int:
        return len(self.units)

    def is_euclidean(self) -> bool:
        """Classical fact: Hurwitz order is Euclidean for the reduced norm."""
        return True

    def is_maximal(self) -> bool:
        """Classical fact for the Hamilton algebra over Q (definite at ∞)."""
        return True

    def contains(self, q: Array, tol: float = 1e-9) -> bool:
        q = np.asarray(q, dtype=float)
        # all integer or all half-integer
        r = np.round(q)
        if np.all(np.abs(q - r) <= tol):
            return True
        h = np.round(q * 2) / 2
        if np.all(np.abs(q - h) <= tol):
            # all coords half-integer (odd half)
            return bool(np.all(np.abs(np.abs(q) * 2 % 2 - 1) < 1e-6 + tol))
        return False

    def multiply(self, u: Array, v: Array) -> Array:
        return q_mult(u, v)

    def norm(self, u: Array) -> float:
        return q_norm2(u)

    def reduce_mod_units(self, q: Array) -> Array:
        """Return unit * q with max real part among left unit multiplies (toy)."""
        best = q_normalize(np.asarray(q, dtype=float))
        best_w = best[0]
        for u in self.units:
            cand = q_normalize(q_mult(u, best))
            if cand[0] > best_w + 1e-12:
                best, best_w = cand, cand[0]
        return best


# ---------------------------------------------------------------------------
# Toy left-ideal / class-number diagnostics (not full ideal arithmetic)
# ---------------------------------------------------------------------------


@dataclass
class IdealClassGroupResult:
    order: int
    method: str
    notes: str
    sample_norms: list[int] = field(default_factory=list)
    representatives: list[Array] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"IdealClassGroupResult(order={self.order}, method={self.method!r})"


def left_ideal_class_group(
    order: HurwitzOrder | LipschitzOrder | None = None,
    *,
    bound: int = 100,
) -> IdealClassGroupResult:
    """Toy class-number diagnostic for Hurwitz / Lipschitz.

    Classical fact used: the Hurwitz order in the Hamilton quaternion algebra
    has **class number 1** (every left ideal is principal). This function
    verifies a finite sample of small-norm generators and returns order=1 for
    Hurwitz, while Lipschitz is reported as non-maximal (class number not 1
    in the same sense — we return a placeholder with notes).

    Parameters
    ----------
    bound :
        Max integer norm of sample elements checked for principality sketch.
    """
    if order is None:
        order = HurwitzOrder()

    if isinstance(order, HurwitzOrder):
        # Sample Lipschitz/Hurwitz integer quaternions of small norm
        samples = []
        for coords in product(range(-3, 4), repeat=4):
            q = np.array(coords, dtype=float)
            n = int(round(q_norm2(q)))
            if 0 < n <= min(bound, 9):
                samples.append((n, q))
        # For class number 1, every ideal is principal — we only *cite* this
        # and check that units have norm 1 and sample norms are integers.
        unit_norms = [int(round(order.norm(u))) for u in order.units]
        assert all(n == 1 for n in unit_norms)
        return IdealClassGroupResult(
            order=1,
            method="classical_hurwitz_class_number_one",
            notes=(
                "Classical theorem: left ideal class number of the Hurwitz order "
                f"is 1. Sampled {len(samples)} elements with norm ≤{min(bound, 9)}; "
                "not a full ideal enumeration."
            ),
            sample_norms=sorted({n for n, _ in samples})[:20],
            representatives=[np.array([1.0, 0.0, 0.0, 0.0])],
        )

    # Lipschitz: not maximal; class number of the order is not the same story
    return IdealClassGroupResult(
        order=-1,
        method="lipschitz_non_maximal",
        notes=(
            "Lipschitz order is not maximal; full left ideal class number is "
            "not computed here. Prefer HurwitzOrder for Euclidean arithmetic."
        ),
        sample_norms=[],
        representatives=[],
    )


def form_ideal_dictionary_entry() -> dict[str, str]:
    """Static Model dictionary (Ch. 9.4) for documentation / labs."""
    return {
        "Ideal in a quaternion order": "Flux configuration / supporting cycle on the gauged Hopf lattice",
        "Ideal class": "Equivalence class of reduced flux topographs",
        "Ideal class group": "Class-group analogue of Chapter 8",
        "Norm of an ideal": "Stability score or magic_island_score",
        "Ideal multiplication": "Composition of flywheels (when defined — OP6)",
    }
