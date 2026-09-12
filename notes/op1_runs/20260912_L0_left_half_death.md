# L0 left-half death (Model 2, resnap=exact)

Claim: **Software fact**. `slice_status`: **C-miniature: occupancy not left-invariant on 2T. Full C (other sections) still parked.**. OP1 stays **Open**.

Left half-units do not map occupancy 4-cycles to 4-cycles: each cycle splits 2+2 onto an antipodal pair of poles. along_kept=0 is occupancy failing left-invariance on a 2T-set, not only min_index section sensitivity. Lipschitz 8 maps each 4-cycle to one fiber and keeps all 24 along-edges. Software fact. OP1 stays Open.

## Lipschitz 8 (contrast)

| unit | along_kept | inter_kept | each 4-cycle lands on |
|---|---|---|---|
| -1 | 1 | 1 | inf→inf, 0→0, 1→1, -i→-i, i→i, -1→-1 |
| 1 | 1 | 1 | inf→inf, 0→0, 1→1, -i→-i, i→i, -1→-1 |
| -i | 1 | 1 | inf→inf, 0→0, 1→1, -i→-i, i→i, -1→-1 |
| i | 1 | 1 | inf→inf, 0→0, 1→1, -i→-i, i→i, -1→-1 |
| -j | 1 | 1 | inf→0, 0→inf, 1→-1, -i→i, i→-i, -1→1 |
| j | 1 | 1 | inf→0, 0→inf, 1→-1, -i→i, i→-i, -1→1 |
| -k | 1 | 1 | inf→0, 0→inf, 1→-1, -i→i, i→-i, -1→1 |
| k | 1 | 1 | inf→0, 0→inf, 1→-1, -i→i, i→-i, -1→1 |

## Left half-units (16)

| left half-unit | image of each 4-cycle | along recovered | 5 surviving octahedron edges |
|---|---|---|---|
| half_---- | inf→{1, -1} 2+2; 0→{1, -1} 2+2; 1→{i, -i} 2+2; -i→{0, inf} 2+2; i→{0, inf} 2+2; -1→{i, -i} 2+2 | 0/24 | inf–1, inf–-i, inf–i, 1–-i, 1–i |
| half_---+ | inf→{i, -i} 2+2; 0→{i, -i} 2+2; 1→{0, inf} 2+2; -i→{1, -1} 2+2; i→{1, -1} 2+2; -1→{0, inf} 2+2 | 0/24 | inf–1, inf–-i, inf–-1, 1–-i, -1–-i |
| half_--+- | inf→{i, -i} 2+2; 0→{i, -i} 2+2; 1→{0, inf} 2+2; -i→{1, -1} 2+2; i→{1, -1} 2+2; -1→{0, inf} 2+2 | 0/24 | inf–1, inf–-i, inf–-1, 1–-i, -1–-i |
| half_--++ | inf→{1, -1} 2+2; 0→{1, -1} 2+2; 1→{i, -i} 2+2; -i→{0, inf} 2+2; i→{0, inf} 2+2; -1→{i, -i} 2+2 | 0/24 | inf–1, inf–-i, inf–i, 1–-i, 1–i |
| half_-+-- | inf→{i, -i} 2+2; 0→{i, -i} 2+2; 1→{0, inf} 2+2; -i→{1, -1} 2+2; i→{1, -1} 2+2; -1→{0, inf} 2+2 | 0/24 | inf–1, inf–-i, inf–-1, 1–-i, -1–-i |
| half_-+-+ | inf→{1, -1} 2+2; 0→{1, -1} 2+2; 1→{i, -i} 2+2; -i→{0, inf} 2+2; i→{0, inf} 2+2; -1→{i, -i} 2+2 | 0/24 | inf–1, inf–-i, inf–i, 1–-i, 1–i |
| half_-++- | inf→{1, -1} 2+2; 0→{1, -1} 2+2; 1→{i, -i} 2+2; -i→{0, inf} 2+2; i→{0, inf} 2+2; -1→{i, -i} 2+2 | 0/24 | inf–1, inf–-i, inf–i, 1–-i, 1–i |
| half_-+++ | inf→{i, -i} 2+2; 0→{i, -i} 2+2; 1→{0, inf} 2+2; -i→{1, -1} 2+2; i→{1, -1} 2+2; -1→{0, inf} 2+2 | 0/24 | inf–1, inf–-i, inf–-1, 1–-i, -1–-i |
| half_+--- | inf→{i, -i} 2+2; 0→{i, -i} 2+2; 1→{0, inf} 2+2; -i→{1, -1} 2+2; i→{1, -1} 2+2; -1→{0, inf} 2+2 | 0/24 | inf–1, inf–-i, inf–-1, 1–-i, -1–-i |
| half_+--+ | inf→{1, -1} 2+2; 0→{1, -1} 2+2; 1→{i, -i} 2+2; -i→{0, inf} 2+2; i→{0, inf} 2+2; -1→{i, -i} 2+2 | 0/24 | inf–1, inf–-i, inf–i, 1–-i, 1–i |
| half_+-+- | inf→{1, -1} 2+2; 0→{1, -1} 2+2; 1→{i, -i} 2+2; -i→{0, inf} 2+2; i→{0, inf} 2+2; -1→{i, -i} 2+2 | 0/24 | inf–1, inf–-i, inf–i, 1–-i, 1–i |
| half_+-++ | inf→{i, -i} 2+2; 0→{i, -i} 2+2; 1→{0, inf} 2+2; -i→{1, -1} 2+2; i→{1, -1} 2+2; -1→{0, inf} 2+2 | 0/24 | inf–1, inf–-i, inf–-1, 1–-i, -1–-i |
| half_++-- | inf→{1, -1} 2+2; 0→{1, -1} 2+2; 1→{i, -i} 2+2; -i→{0, inf} 2+2; i→{0, inf} 2+2; -1→{i, -i} 2+2 | 0/24 | inf–1, inf–-i, inf–i, 1–-i, 1–i |
| half_++-+ | inf→{i, -i} 2+2; 0→{i, -i} 2+2; 1→{0, inf} 2+2; -i→{1, -1} 2+2; i→{1, -1} 2+2; -1→{0, inf} 2+2 | 0/24 | inf–1, inf–-i, inf–-1, 1–-i, -1–-i |
| half_+++- | inf→{i, -i} 2+2; 0→{i, -i} 2+2; 1→{0, inf} 2+2; -i→{1, -1} 2+2; i→{1, -1} 2+2; -1→{0, inf} 2+2 | 0/24 | inf–1, inf–-i, inf–-1, 1–-i, -1–-i |
| half_++++ | inf→{1, -1} 2+2; 0→{1, -1} 2+2; 1→{i, -i} 2+2; -i→{0, inf} 2+2; i→{0, inf} 2+2; -1→{i, -i} 2+2 | 0/24 | inf–1, inf–-i, inf–i, 1–-i, 1–i |
