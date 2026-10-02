#!/usr/bin/env bash
# Blender masks Python failures unless --python-exit-code precedes --python.
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"
if [[ -z "${BLENDER:-}" ]]; then
  if command -v blender >/dev/null 2>&1; then
    BLENDER="$(command -v blender)"
  elif [[ -x /Applications/Blender.app/Contents/MacOS/Blender ]]; then
    BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
  else
    echo 'Set BLENDER to a Blender executable.' >&2
    exit 2
  fi
fi
"$PYTHON" -m unittest discover -v
"$PYTHON" -m py_compile blender/*.py
for test in blender/test_*_runtime.py; do
  echo "CHECK $test"
  "$BLENDER" --background --python-exit-code 1 --python "$test"
done
"$BLENDER" --background --python-exit-code 1 --python blender/validate_scene.py
git diff --check
echo 'ALL CHECKS PASSED'
