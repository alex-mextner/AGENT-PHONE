#!/usr/bin/env bash
# Build and check actual inert wearable exports; never submit a printer job.
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"
THREED="${THREED:-3d}"
ROOT=prototype/wearable-mockup
"$PYTHON" "$ROOT/generate.py" > "$ROOT/qa/generation.txt"
"$PYTHON" -m unittest tests.test_wearable_mockup -v > "$ROOT/qa/tests.txt" 2>&1
: > "$ROOT/qa/mesh.txt"
for part in "$ROOT"/parts/*.stl; do
  echo "FILE $part" >> "$ROOT/qa/mesh.txt"
  "$THREED" mesh "$part" >> "$ROOT/qa/mesh.txt" 2>&1
done
"$THREED" printability "$ROOT"/parts/*.stl > "$ROOT/qa/printability.txt" 2>&1
"$THREED" arrange "$ROOT/parts/tray.stl" "$ROOT/parts/lid.stl" "$ROOT/parts/base.stl" \
  --bed 220 --gap 6 --margin 8 --min-volume 0 -o "$ROOT/plates/rigid-parts" --json > "$ROOT/qa/rigid-plate.json"
"$THREED" arrange "$ROOT"/parts/fit_gauge_*.stl \
  --bed 220 --gap 6 --margin 8 --min-volume 0 -o "$ROOT/plates/fit-gauges-TPU-first" --json > "$ROOT/qa/gauge-plate.json"
for profile in slim average large; do
  "$THREED" arrange "$ROOT/parts/cuff_left_${profile}.stl" "$ROOT/parts/cuff_right_${profile}.stl" "$ROOT/parts/dorsal_pad.stl" \
    --bed 220 --gap 6 --margin 8 --min-volume 0 -o "$ROOT/plates/cuffs-${profile}-TPU" --json > "$ROOT/qa/${profile}-plate.json"
done
for plate in "$ROOT"/plates/*.3mf; do
  echo "SLICING $plate"
  "$THREED" slice-check "$plate" --no-slice --plates 1 --timeout 180 > "$ROOT/qa/$(basename "$plate" .3mf)-open.txt" 2>&1
done
"$PYTHON" "$ROOT/prepare_3mf.py"
for plate in "$ROOT"/plates/snapmaker-u1/*.3mf; do
  "$THREED" slice-check "$plate" --plates 1 --timeout 180 > "$ROOT/qa/U1-$(basename "$plate" .3mf)-slice.txt" 2>&1
done
echo 'WEARABLE CAD, MESH, PRINTABILITY, PLATES AND SLICING CHECKS PASSED'
