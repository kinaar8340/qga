# Appendix C — Laboratory Code Reference

Full lab listings moved out of the main chapter flow. Chapters keep short “call” versions and exercises; use this appendix when typing or copying longer scripts.

**Setup (all labs) — one install path.** From the clone root:

```bash
python3 -m pip install -e .
python3 -m pip install -e ".[portal]"   # labs that import kingdom / flux_hopf_lib
```

```python
from lib.hopf_lattice import hopf_map, HURWITZ_UNITS
```

Do not hard-code `~/Projects/...` and do not use a commented `PYTHONPATH` as the official path.

---

## C.1 Chapters 1–2 (foundations)

### Lab 1.A — Multiplication table

```python
from kingdom.core.quaternion import Quaternion

i = Quaternion(0, 1, 0, 0)
j = Quaternion(0, 0, 1, 0)
k = Quaternion(0, 0, 0, 1)
print(i.multiply(j))  # ~ k
print(j.multiply(i))  # ~ -k
print(i.multiply(i))  # ~ -1
```

### Lab 1.B — Norm multiplicativity

```python
import numpy as np
from kingdom.core.quaternion import Quaternion

rng = np.random.default_rng(0)

def rand_q():
    a = rng.normal(size=4)
    return Quaternion(*a)

q1, q2 = rand_q(), rand_q()
prod = q1.multiply(q2)
n1, n2 = q1.norm() ** 2, q2.norm() ** 2
print(abs(prod.norm() ** 2 - n1 * n2))
```

### Lab 1.C — Small Lipschitz norms

```python
from itertools import product

def lipschitz_norms(nmax=3):
    found = {}
    for a, b, c, d in product(range(-nmax, nmax + 1), repeat=4):
        n = a * a + b * b + c * c + d * d
        if 0 < n <= nmax:
            found.setdefault(n, []).append((a, b, c, d))
    return {k: found[k][:8] for k in sorted(found)}

print(lipschitz_norms(3))
```

### Lab 1.D — Double cover

```python
import numpy as np
from kingdom.core.quaternion import Quaternion

q = Quaternion.from_axis_angle(np.array([0.0, 0.0, 1.0]), np.pi / 3)
mq = Quaternion(-q.w, -q.x, -q.y, -q.z)
v = Quaternion(0, 1, 0, 0)
rq = q.multiply(v).multiply(q.inverse())
rm = mq.multiply(v).multiply(mq.inverse())
print(rq, rm)  # same rotation
```

### Lab 2.A–B — Hopf image and structure-group fiber

```python
from lib.hopf_lattice import hopf_map, common_phase, sample_structure_group_fiber
import numpy as np

q = np.array([0.5, 0.5, 0.5, 0.5]); q = q / np.linalg.norm(q)
print(hopf_map(q), np.linalg.norm(hopf_map(q)))
print("h(0,0,1,0) =", hopf_map(np.array([0.0, 0.0, 1.0, 0.0])))

fiber = sample_structure_group_fiber(q, n_points=64)
base = np.stack([fiber["y1"], fiber["y2"], fiber["y3"]], axis=1)
print(np.linalg.norm(np.stack([fiber["x1"], fiber["x2"], fiber["x3"], fiber["x4"]], axis=1), axis=1)[:5])
print("base constant:", np.allclose(base, base[0]))
```

### Lab 2.C — Fiber constancy vs xi2-circle

```python
from lib.hopf_lattice import hopf_map, common_phase, hopf_coordinates
import numpy as np

q = np.array([0.6, 0.3, 0.4, 0.6]); q = q / np.linalg.norm(q)
y0 = hopf_map(q)
print(max(np.linalg.norm(hopf_map(common_phase(q, p)) - y0) for p in np.linspace(0, 2 * np.pi, 12, endpoint=False)))

# ξ2-circle at fixed (η, ξ1) is NOT the structure-group fiber
xi2_pts = np.stack([hopf_coordinates(0.4, 0.3, t) for t in np.linspace(0, 2 * np.pi, 12, endpoint=False)])
xi2_base = np.stack([hopf_map(p) for p in xi2_pts])
print("xi2-circle base spread:", np.max(np.linalg.norm(xi2_base - xi2_base[0], axis=1)))
```

### Lab 2.D — Random unit images

```python
from lib.hopf_lattice import hopf_map
import numpy as np
rng = np.random.default_rng(0)
for _ in range(3):
    q = rng.normal(size=4); q = q / np.linalg.norm(q)
    y = hopf_map(q)
    print(y, np.linalg.norm(y))
```

### Lab 2.E — Structure-group fiber family

```python
from lib.hopf_lattice import sample_structure_group_fiber_family
family = sample_structure_group_fiber_family(n_fibers=8, n_points=64)
print(len(family), family[0]["base_y1"])
```

---

## C.2 Chapters 3–4 (lattice and symmetries)

### Lab 3.A–C — Hurwitz, adjacency, gauge

```python
from lib.hopf_lattice import (
    HURWITZ_UNITS, hopf_project_points, sample_angle_lattice,
    candidate_adjacency, left_multiply, right_multiply, rounded_point_set,
)
import numpy as np

print(len(HURWITZ_UNITS), np.allclose(np.sum(HURWITZ_UNITS**2, axis=1), 1.0))
base = hopf_project_points(HURWITZ_UNITS)
print("distinct base ~", len(np.unique(np.round(base, 5), axis=0)))

pts = sample_angle_lattice(n_eta=3, n_xi1=8, n_xi2=8)
along, inter = candidate_adjacency(pts, base_angle_thresh=0.5)
print(len(pts), len(along), len(inter))

i = np.array([0.0, 1.0, 0.0, 0.0])
moved = left_multiply(HURWITZ_UNITS, i)
base0, baseL = hopf_project_points(HURWITZ_UNITS), hopf_project_points(moved)
same_set = rounded_point_set(base0) == rounded_point_set(baseL)
print("base set invariant:", same_set)
print("total-space moved:", not np.allclose(moved, HURWITZ_UNITS))
```

### Lab 3.D — Two-gyro dynamics

```python
from kingdom.core.lattice import LatticeConfig
from kingdom.simulations.lattice import TwoGyroLattice, run_lattice_comparison

stable, chaotic = run_lattice_comparison(frames=80, n_sites=48)
print(stable.stability_score, stable.total_bursts, chaotic.total_bursts)
```

### Lab 4.A–B — Gauge sequences and orbits

```python
from lib.hopf_lattice import (
    HURWITZ_UNITS, permutes_hurwitz_units, left_multiply,
    hopf_project_points, orbit_of_point, phase_unit,
)
import numpy as np

i = np.array([0.0, 1.0, 0.0, 0.0])
print(permutes_hurwitz_units(i, side="L"))
seq = [("R", phase_unit(np.pi / 3)), ("L", i)]
orbit = orbit_of_point(HURWITZ_UNITS[3], seq, max_periods=24, tol=1e-6)
print(len(orbit), np.linalg.norm(orbit[-1] - orbit[0]))
```

### Lab 4.C — Identity preservation (portal extra)

```python
from kingdom.core.lattice import LatticeConfig
from kingdom.simulations.lattice import run_lattice_comparison
stable, chaotic = run_lattice_comparison(frames=40, n_sites=32)
print("stable", stable.identity_preservation if hasattr(stable, "identity_preservation") else stable.stability_score)
print("chaotic bursts", chaotic.total_bursts)
```

### Lab 4.D — Flux push-forward from the left action of \(i\) (OP1 diagnostic)

```python
from lib.hopf_lattice import (
    sample_angle_lattice, candidate_adjacency, discrete_flux_cycle,
    left_multiply, transform_flux, adjacency_equivariance_score,
    nearest_index_map, HURWITZ_UNITS,
)
import numpy as np

pts = HURWITZ_UNITS
along, inter = candidate_adjacency(pts, base_angle_thresh=0.55, fiber_phase_bins=8)
edges = along[:8] if along else inter[:8]
Phi = discrete_flux_cycle(edges, value=1)
i = np.array([0.0, 1.0, 0.0, 0.0])
moved = left_multiply(pts, i)
imap = nearest_index_map(moved, pts)  # permutation induced by left action of i
print("imap unique", len(set(imap.values())), "of", len(pts))
print(len(transform_flux(Phi, imap)) // 2)
eq = adjacency_equivariance_score(pts, i, side="L", base_angle_thresh=0.55, fiber_phase_bins=8)
print(eq)  # OP1 diagnostic — not a theorem of equivariance
```

---

## C.3 Chapters 5–7 (topographs, classification, Z-map)

### Lab 5.A–D — Topographs

```python
from lib.hopf_lattice import sample_angle_lattice, candidate_adjacency, phase_unit
from lib.flux_topograph import (
    build_flux_topograph, detect_separators, arithmetic_progression_residuals,
    periodicity_score, separator_equivariance_score,
)
import numpy as np

pts = sample_angle_lattice(4, 12, 12)
along, inter = candidate_adjacency(pts, base_angle_thresh=0.5, fiber_phase_bins=12)
topo = build_flux_topograph(pts, edges=along + inter, functional="hopf_height")
seps = detect_separators(topo, mode="sign")
print(len(seps), sum(len(c) for c in seps), arithmetic_progression_residuals(topo))

i = np.array([0.0, 1.0, 0.0, 0.0])
print(periodicity_score(topo, [("L", i), ("R", phase_unit(np.pi / 2))], max_periods=8))
print(separator_equivariance_score(topo, [("L", i)]))
```

### Lab 6.A–D — Classification

```python
from lib.flux_topograph import (
    build_flux_topograph, classify_topograph_type, enumerate_reduced,
    class_number_analogue, equivalence_distance, apply_gauge_to_topograph,
)
from lib.hopf_lattice import sample_angle_lattice, candidate_adjacency
import numpy as np

pts = sample_angle_lattice(3, 10, 10)
along, inter = candidate_adjacency(pts, base_angle_thresh=0.5, fiber_phase_bins=10)
topo = build_flux_topograph(pts, edges=along + inter, functional="hopf_height")
print(classify_topograph_type(topo))
print("n reduced", len(enumerate_reduced(topo, dedup_tol=0.05)))
print(class_number_analogue(topo, dedup_tol=0.05)["class_number_analogue"])
i = np.array([0.0, 1.0, 0.0, 0.0])
print(equivalence_distance(topo, apply_gauge_to_topograph(topo, [("L", i)])))
```

### Lab 7.A–E — Z-map with H2 ablation (not findings)

```python
from kingdom.core.flux_flywheel import map_z_to_flywheel
from lib.validation import h2_ablation_table

rows = [map_z_to_flywheel(z) for z in range(1, 51)]
report = h2_ablation_table(rows, high_threshold=7.5, seed=0)
print(report["disclaimer"])
print("alignment with bonus", report["alignment_with_bonus"])
print("alignment ablated   ", report["alignment_ablated"])
print("null (shuffled labels)", report["null_alignment_ablated"])
# Do not print noble-gas bonuses as findings. Compare ablated alignment to the null.
```

---

## C.4 Chapters 8–10 (composition, algebras, validation)

### Lab 8.A–D — Composition

```python
from lib.hopf_lattice import sample_angle_lattice, candidate_adjacency
from lib.flux_topograph import build_flux_topograph, class_number_analogue
from lib.composition import (
    compose_flywheels, reduce_composition, composition_table,
    class_group_analogue, is_associative_up_to_equivalence,
)

pts = sample_angle_lattice(2, 6, 6)
along, inter = candidate_adjacency(pts, base_angle_thresh=0.55, fiber_phase_bins=6)
edges = along + inter
t1 = build_flux_topograph(pts, edges=edges, functional="hopf_height")
t2 = build_flux_topograph(pts, edges=edges, functional="hopf_y1")
print(reduce_composition(compose_flywheels(t1, t2, method="value_sum"))["classification"]["type"])

cg = class_group_analogue(t1, dedup_tol=0.1, samples=10)
print(cg["order"], cg["structure"], cg["associativity"])
reps = cg["representatives"]
print(composition_table(reps, dedup_tol=0.1)["closure_fraction"])
print(is_associative_up_to_equivalence(reps, samples=20, tol=0.1))
```

### Lab 9.A–E — Quaternion algebras

```python
from lib.quaternion_algebra import (
    QuaternionAlgebra, HurwitzOrder, LipschitzOrder,
    left_ideal_class_set, two_sided_class_group, hilbert_symbol,
)

A = QuaternionAlgebra(-1, -1)
print(A.presentation(), A.ramified_places(), A.is_definite())
O = HurwitzOrder()
print(O.n_units(), O.is_euclidean(), O.is_maximal())
print(left_ideal_class_set(O).cardinality, left_ideal_class_set(O).method)
print(two_sided_class_group(O).order, two_sided_class_group(O).method)
```

### Lab 9.F — Hilbert symbols (own number)

```python
from lib.quaternion_algebra import hilbert_symbol
print({p: hilbert_symbol(-1, -1, p) for p in [2, 3, 5, "inf"]})
```

### Lab 10.B-style — Table T4 demo

```python
from lib.validation import (
    run_table_t4_demo, combine_p_values_fisher, bonferroni_threshold,
    proximity_to_wg, WG_350_OVER_PI, default_hypotheses, table_t4_checklist,
)

print("W_g", WG_350_OVER_PI)
print(len(table_t4_checklist()), [h.name for h in default_hypotheses()])
demo = run_table_t4_demo(seed=1, alpha=0.01)
print(demo["bonferroni_threshold"], demo["decision"], demo["disclaimer"])
print(proximity_to_wg([111.4, 111.5, 110.0, 111.408]))
```

### Lab 10.A — OP research proposal (hand)

Choose OP1, OP2, or OP6 from Appendix B. Write sandbox, diagnostic, and success criterion (one page). This listing is the prompt, not a script.

---

## C.5 Common pitfalls

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: lib` | `python3 -m pip install -e .` from the clone root |
| `ModuleNotFoundError: kingdom` | `python3 -m pip install -e ".[portal]"` (not a `PYTHONPATH` to `~/Projects`) |
| `magic_flag` KeyError | Use `stability_score` / `is_noble_gas` |
| `step` AttributeError | Use `step_frame()` |
| Slow `enumerate_reduced` | Smaller lattices (`n_eta≤3`, `n_xi≤10`) |

---

*Manuscript · Appendix C · Laboratory Code Reference.*
