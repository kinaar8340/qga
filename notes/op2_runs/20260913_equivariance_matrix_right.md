# OP2 equivariance matrix (ledger)

Recorded as an OP2 **ledger increment**. No axiom, no new graph, OP3 not entered.

## Claim lock

- The equivariance matrix is a **ledger**, not an axiom.
- Model 2 is **not** gauge-equivariant.
- This increment does **not** open OP3. The research problem OP3 remains **Open**; the gate is “do not enter it here.”
- No new graph. Candidate edges stay refused.
- Right-\(i\) / right-\(j\) are not averaged, and not averaged with the left ledger.

Claim type: **Software fact**. OP2 status: **Open**.
Not Ch. 5 axioms. Do **not** call Model 2 gauge-equivariant.

Right-gauge columns on the same Model 2 graphs. Not averaged with left.

- `Lsg`: `notes/op2_runs/20260911_Lsg_structure_group.json` ← `notes/op1_runs/20260911_Lsg_book_default_none_structure_group.json`
- `L0`: `notes/op2_runs/20260911_L0_structure_group.json` ← `notes/op1_runs/20260911_L0_book_default_exact_structure_group.json`
- `Lang`: `notes/op2_runs/20260911_Lang_structure_group.json` ← `notes/op1_runs/20260911_Lang_book_default_none_structure_group.json`

Empty cut stays `undefined_or_vacuous` under gauge, **not** keep-rate 1.0.

## hopf_height (n_components before→after)

| | right-i | right-j |
|---|---|---|
| Lsg | `4→4` `changed` | `4→5` `changed` |
| L0 | `undefined_or_vacuous` | `undefined_or_vacuous` |
| Lang | `1→1` `unchanged` | `1→1` `unchanged` |

## hopf_y1 (n_components before→after)

| | right-i | right-j |
|---|---|---|
| Lsg | `undefined_or_vacuous` | `undefined_or_vacuous` |
| L0 | `undefined_or_vacuous` | `undefined_or_vacuous` |
| Lang | `8→9` `changed` | `8→9` `changed` |

## OP1 inter_kept (right, not averaged)

| | right-i | right-j |
|---|---|---|
| Lsg | 1.0 | 1.0 |
| L0 | 1.0 | 1.0 |
| Lang | 0.8111111111111111 | 0.8333333333333334 |

L0 `inter_kept = 1` on Lipschitz \(i,j\) is a **different object** from the empty strict-sign cut. That cell is not keep-rate 1.0. Lang right `inter_kept` is not averaged with left or with i/j.

## What this forbids

Do not write OP2 axioms from these cells. Do not average with the left ledger. Do not fold the two files. Matching component integers (Lsg height j 4→5, Lang y1 8→9) and matching edge moves on those cuts (Lsg j 5→7, Lang y1 j 37→38) do not identify the ledgers. Lang inter_kept already differs (left 0.944/0.811 vs right 0.811/0.833). L0 stays vacuous because zeros are levels, not crossings. That is the content of the ledger. It is not invariance.
