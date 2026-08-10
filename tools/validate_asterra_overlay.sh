#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="${ROOT}/build/pokefirered"
for f in starter_sets.h rival_logic.h; do
  test -f "${BUILD_DIR}/include/asterra/${f}"
done
test -f "${BUILD_DIR}/src/asterra_starter_selection.c"
grep -q '#include "asterra/starter_sets.h"' "${BUILD_DIR}/src/asterra_starter_selection.c"
grep -q '#include "asterra/rival_logic.h"' "${BUILD_DIR}/src/asterra_starter_selection.c"
echo "Asterra overlay validation passed."
