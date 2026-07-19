# Book figures index

## Chapter 0

| ID | File | Caption (short) | Source (Kingdom Come) |
|----|------|-----------------|------------------------|
| Fig. 0.1 | `figures/fig0_1_hopf_linked_fibers.png` | Linked Hopf fibers, stereographic | `app/assets/home/hopf_linked_fibers.png` |
| Fig. 0.2 | `figures/fig0_2_hopf_stereographic.png` | Stereographic fibration preview | `app/assets/hopf_preview.png` |
| Fig. 0.3 | `figures/fig0_3_hopf_bundle.png` | Bundle: \(S^3\to S^2\) | `app/assets/home/hopf_fibration_bundle.png` |
| Fig. 0.4 | `figures/fig0_4_flux_flywheel_scales.jpg` | Flux flywheel scales | `app/assets/bitcoin_pi/flux_flywheel_scales.jpg` |
| Fig. 0.5 | `figures/fig0_5_hopf_lattice_pi_cycle.jpg` | Lattice + π-cycle motif | `app/assets/bitcoin_pi/hopf_lattice_pi_cycle.jpg` |

### Auxiliary (Z-map stills)

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Aux A0.1 | `figures/aux_z_map_he.png` | Helium \(Z=2\) closed-shell baseline | `z_knowns/frame_0002.png` |
| Aux A0.2 | `figures/aux_z_map_fe.png` | Iron \(Z=26\) mid-table contrast | `z_knowns/frame_0026.png` |

## Chapter 1

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 1.1 | `figures/fig1_1_ijk_multiplication.png` | \(i,j,k\) cycle + mult. table | generated |
| Fig. 1.2 | `figures/fig1_2_s3_unit_quaternions.png` | Unit quaternions as \(S^3\) | generated |
| Fig. 1.3 | `figures/fig1_3_lipschitz_hurwitz.png` | Lipschitz vs Hurwitz | generated |
| Fig. 1.4 | `figures/fig1_4_norm_multiplicativity.png` | Norm multiplicativity | generated |
| Aux A1.1 | `figures/aux1_1_quaternion_rotation.png` | Rotation via conjugation | generated |

Regenerate: `python scripts/generate_ch1_figures.py`.

## Chapter 2

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 2.1 | `figures/fig2_1_hopf_definition.png` | Hopf map \(S^3\to S^2\) | generated |
| Fig. 2.2 | `figures/fig2_2_linked_fibers.png` | Linked fibers (rebuild 0.1) | generated via `sample_fiber_family` |
| Fig. 2.3 | `figures/fig2_3_stereographic_preview.png` | Multi-panel preview (rebuild 0.2) | generated |
| Fig. 2.4 | `figures/fig2_4_bundle_structure.png` | Bundle diagram (rebuild 0.3) | generated |
| Aux A2.1 | `figures/aux2_1_fiber_phase_sweep.png` | Single fiber phase sweep | generated |
| Aux A2.2 | `figures/aux2_2_hopf_charts.png` | Local charts on \(S^2\) | generated |

Regenerate: `python scripts/generate_ch2_figures.py` (requires `flux_hopf_lib` or `kingdom` on path).

## Chapter 3

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 3.1 | `figures/fig3_1_hurwitz_lattice_in_s3.png` | 24 Hurwitz units stereo | generated (`lib/hopf_lattice`) |
| Fig. 3.2 | `figures/fig3_2_hopf_projected_lattice.png` | Angle lattice → \(S^2\) | generated |
| Fig. 3.3 | `figures/fig3_3_adjacency_and_fibers.png` | Candidate adjacency (OP1) | generated |
| Fig. 3.4 | `figures/fig3_4_gauge_action.png` | Left/right gauge actions | generated |
| Fig. 3.5 | `figures/fig3_5_flux_flywheel_schematic.png` | Flywheel schematic | generated |
| Aux A3.1 | `figures/aux3_1_lattice_simulator_still.png` | TwoGyroLattice still | generated via kingdom |

Regenerate: `python scripts/generate_ch3_figures.py` (use kingdom venv for Aux A3.1).

## Chapter 4

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 4.1 | `figures/fig4_1_left_right_symmetries.png` | Left vs right gauge | generated |
| Fig. 4.2 | `figures/fig4_2_periodic_orbit.png` | Combined gauge orbit | generated |
| Fig. 4.3 | `figures/fig4_3_glide_reflection_analogue.png` | Helical glide analogue | generated |
| Fig. 4.4 | `figures/fig4_4_symmetry_on_flywheel.png` | Flywheel equivariance | generated |
| Aux A4.1 | `figures/aux4_1_gauge_group_elements.png` | 24 Hurwitz units | generated |

Regenerate: `python scripts/generate_ch4_figures.py`.

## Chapter 5

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 5.1 | `figures/fig5_1_flux_topograph_schematic.png` | Value landscape | generated |
| Fig. 5.2 | `figures/fig5_2_separator_structure.png` | Separators | generated |
| Fig. 5.3 | `figures/fig5_3_magic_island.png` | Magic Island + Z scores | generated (+ kingdom if available) |
| Fig. 5.4 | `figures/fig5_4_symmetry_on_topograph.png` | Gauge on topograph | generated |
| Aux A5.1 | `figures/aux5_1_topograph_evolution.png` | Phase evolution | generated |

Regenerate: `python scripts/generate_ch5_figures.py`.

## Chapter 6

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 6.1 | `figures/fig6_1_four_types.png` | Four topograph types | generated |
| Fig. 6.2 | `figures/fig6_2_reduced_config.png` | Reduced representative | generated |
| Fig. 6.3 | `figures/fig6_3_class_number_analogue.png` | Class-number analogue | generated |
| Fig. 6.4 | `figures/fig6_4_equivalence.png` | Gauge equivalence | generated |
| Aux A6.1 | `figures/aux6_1_island_sweep.png` | Z stability sweep | generated (+ kingdom) |

Regenerate: `python scripts/generate_ch6_figures.py`.

## Chapter 7

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 7.1 | `figures/fig7_1_z_to_flywheel.png` | Z-map pipeline | generated |
| Fig. 7.2 | `figures/fig7_2_magic_island_periodic_table.png` | Scores on table | generated (+ portal scores) |
| Fig. 7.3 | `figures/fig7_3_stability_vs_z.png` | Score vs Z | generated (+ portal) |
| Fig. 7.4 | `figures/fig7_4_electron_cloud_flux.png` | Cloud schematic | generated |
| Aux A7.1 | `figures/aux7_1_he_fe_au_stills.png` | He/Fe/Au stills | kingdom `z_knowns` |

Regenerate: `python scripts/generate_ch7_figures.py` (prefer kingdom venv).

## Chapter 8

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 8.1 | `figures/fig8_1_gauss_composition.png` | Classical Gauss composition | generated |
| Fig. 8.2 | `figures/fig8_2_flywheel_composition.png` | Flywheel/topograph composition | generated |
| Fig. 8.3 | `figures/fig8_3_class_group_analogue.png` | Class-group analogue | generated |
| Fig. 8.4 | `figures/fig8_4_island_from_class.png` | Island from class data | generated |
| Aux A8.1 | `figures/aux8_1_composition_table.png` | Composition table | generated |

Regenerate: `python scripts/generate_ch8_figures.py`.

## Chapter 9

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 9.1 | `figures/fig9_1_quaternion_algebra.png` | Ramification diagram | generated |
| Fig. 9.2 | `figures/fig9_2_hurwitz_order.png` | Hurwitz units / orders | generated |
| Fig. 9.3 | `figures/fig9_3_ideal_class_group.png` | Ideal class group | generated |
| Fig. 9.4 | `figures/fig9_4_ideal_to_flywheel.png` | Ideal → flywheel bridge | generated |
| Fig. 9.5 | `figures/fig9_5_modulus_invariants.png` | Three-layer modulus invariants | from `vortex_math` |
| Aux A9.1 | `figures/aux9_1_ramification_table.png` | Hilbert symbol table | generated |

Regenerate: `python scripts/generate_ch9_figures.py` (Fig. 9.5 copied from `vortex_math` book figure).

## Chapter 10

| ID | File | Caption (short) | Source |
|----|------|-----------------|--------|
| Fig. 10.1 | `figures/fig10_1_350_over_pi_domains.png` | Multi-domain \(350/\pi\) | generated |
| Fig. 10.2 | `figures/fig10_2_z_map_correlation.png` | Score vs IE proxy | generated (+ portal) |
| Fig. 10.3 | `figures/fig10_3_magic_island_validation.png` | Islands vs specialness | generated |
| Fig. 10.4 | `figures/fig10_4_validation_flowchart.png` | Table T4 flowchart | generated |
| Aux A10.1 | `figures/aux10_1_pulsar_bitcoin_overlay.png` | Observation assets | kingdom assets |

Regenerate: `python scripts/generate_ch10_figures.py`.

Full license note: `figures/ATTRIBUTION.md`.
