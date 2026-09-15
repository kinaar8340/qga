# Two QGA pipelines

They share vertices and `hopf_map`. They do not share a graph.
OAM 2×2 tiles are **not** a step in either pipeline.

OP1 stays **Open**. Do not flatten the stack.

## A. Manuscript (what GitHub documents)

Door: [START_HERE.md](../START_HERE.md) · [TOC.md](../TOC.md) · [HATCHER_MAP.md](../HATCHER_MAP.md).

```text
START_HERE / TOC / HATCHER_MAP
        ↓
book/*.md  (Ch. 0–10, claim labels)
        ↓
scripts/build_latex.sh
        ↓
book/Kingdom_Come_QGA.pdf
```

```bash
python3 -m pip install -e ".[dev]"
./scripts/build_latex.sh
# → book/latex/main.pdf  and  book/Kingdom_Come_QGA.pdf
```

`lib/hopf_lattice.py` is pedagogical support for Ch. 3–4. Every adjacency rule there is a **Model candidate for OP1**, not SoT. `candidate_adjacency` is the \(\xi_2\)-circle, **not** structure-group \(U(1)\). Use `sample_structure_group_fiber` when the object must be a Hopf fiber.

This is the public how-to. A clone that only wants the book can stop here.

## B. Research harness (lab notebook)

Not the README lead. Commands as they run in this tree. Pin first.

### 0 Pin

```bash
python3 -c "from flux_hopf_lib.hopf.fibration import hopf_map; from flux_hopf_lib.quaternion.hurwitz import HURWITZ_UNITS
print(__import__('importlib.metadata', fromlist=['version']).version('flux-hopf-lib'))
print(tuple(float(c) for c in hopf_map(0.0, 0.0, 1.0, 0.0)), len(HURWITZ_UNITS))"
# need 0.3.1 and (0.0, 0.0, -1.0) and 24
```

Fail → stop.

### 1 INIT — control exists

`candidate_adjacency` on the sample. Frozen book default. Do not delete `tests/data/op1_L0_left_i_book_default.json`.

### 2 GATE — analysis channel

```bash
python3 scripts/op1_adjacency/run.py --set Lsg --rule structure_group --no-edges
python3 scripts/op1_adjacency/run.py --set L0  --rule structure_group --no-edges
```

`--rule candidate` or mixed along/inter in one topograph → refuse.

### 3 CENSUS

The OP1 JSON row: bases × multiplicity + `along_kind`. No row → no downstream.

### 4 ATTACH

```bash
python3 scripts/op2_topograph/run.py --set Lsg --rule structure_group \
  --attach notes/op1_runs/20260911_Lsg_book_default_none_structure_group.json
```

Missing attach or wrong `kind`/`rule` → refuse.

### 5 SUPPORT

`build_flux_topograph` Kirchhoff \(\max\|r\|=0\). Residue → fix the builder.

### 6 CUT / PERIOD

Strict-sign separators. L0 may be `undefined_or_vacuous`. Inventing crossings is illegal.

### 6b EQUIVARIANCE LEDGER

```bash
python3 scripts/op2_topograph/run.py --matrix --rule structure_group
```

Assembles `notes/op2_runs/20260913_equivariance_matrix.json` from scored OP2 JSON. Not a new graph. L0 empty cut stays `undefined_or_vacuous`, not keep-rate 1.0. Do not call Model 2 gauge-equivariant. Do not open OP3.

```bash
python3 scripts/op2_topograph/run.py --matrix-right --rule structure_group
```

Sibling right-gauge ledger: `notes/op2_runs/20260913_equivariance_matrix_right.json`. Same Model 2 graphs. Not averaged with left. L0 empty cut still vacuous.

### 7 SLICE A

```bash
python3 scripts/op1_adjacency/farey_slice.py --set L0 --rule structure_group \
  --attach notes/op1_runs/20260911_L0_book_default_exact_structure_group_graph.json
```

8/12 Gaussian-Farey on \(h(\Lambda_0)\). Calling it \(\mathbb{Q}\)-Farey → fail.

### 8 SLICE B

Index the existing 24×2 tables: `notes/op1_runs/20260911_slice_B_keep_rate.md`.
Rerunning the same matrix → noise.

Left-half death on L0 sits **after** the gate as a diagnostic (`20260912_L0_left_half_death.json`): occupancy 4-cycles split 2+2 onto antipodal poles. It does not reroute the pipe. It only forbids “Model 2 is 2T-equivariant.”

### 8b SECTION C (same L0 graph)

```bash
python3 scripts/op1_adjacency/section_c.py --set L0 --rule structure_group \
  --attach notes/op1_runs/20260911_L0_book_default_exact_structure_group_graph.json
```

`notes/op1_runs/20260913_L0_section_C.json`. min_index / max_index / max_real. No third graph. 8/12 overlap invariant; inter lifts move; max_real left-half `inter_kept` mixed.

### 9 WITNESS

```bash
python3 scripts/op1_adjacency/run.py --set Lsg --rule structure_group --dump-graph
python3 scripts/op1_adjacency/run.py --set L0  --rule structure_group --dump-graph
python3 scripts/op1_adjacency/run.py --set Lang --rule structure_group --dump-graph --no-edges
```

`kind=qga_adjacency_graph_v1`, no `fibers[]`. Explorer file-picker: red along / blue inter. Putting `fibers[]` on that file → schema mix. Lang dump is a witness of the 20260911 row (256/256/90), not a new adjacency and not slice A/C.

### 10 ENGINE

```bash
cd ~/Projects/qga_engine
cargo test -p qga-math hopf_hurwitz
cargo test -p qga-math hurwitz
cargo test -p qga-math op1_l0
```

Census integers + Hurwitz 24 + classical `hopf_map`. Delaunay in Rust → no.

### Decision graph

```text
sample Λ
   ├─ Model 1 → figures, golden, INIT only
   └─ Model 2 → GATE
                 ├─ fail (wrong circle / mixed / no attach) → STOP
                 └─ pass → census → OP2 sandbox → slices A/B → C (same L0) → equivariance ledger
                              └─ still Open; no OP3
```

Parked off the belt: OP3, Model 2 in `flux_hopf_lib`.

## C. Stack around it (do not flatten)

| Crate | Role in the pipe | Must not do |
|---|---|---|
| `flux_hopf_lib` 0.3.1 | SoT maps + Hurwitz 24 | own adjacency |
| `qga/lib` | book labs + both rules | pretend OP1 closed |
| `qga/scripts/op1_*` `op2_*` | this harness | write Ch. 5 axioms |
| `flux_hopf_explorer` | fiber demo **or** graph witness | new physics |
| `qga_engine` | replay census integers | implement Model 2 |
| `kingdom_come` portal | Book Mode / Hopf viz / flywheel **Model** | eat harness JSON as theorem |
| `shellscan` / occupancy 256 | frozen faceplate | same graph as OP1 |

## Tests (harness)

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest tests/test_op1_adjacency.py tests/test_op1_farey_slice.py \
  tests/test_op1_slice_b.py tests/test_op1_left_half_death.py \
  tests/test_op2_topograph.py -q
```
