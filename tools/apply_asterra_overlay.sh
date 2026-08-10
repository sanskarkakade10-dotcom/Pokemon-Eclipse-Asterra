#!/usr/bin/env bash
set -euo pipefail

# This script is the bridge between the Asterra repository and the upstream
# FireRed decompilation checkout used by the GBA build workflow.
#
# v0.2 currently validates the starter data layer. Gameplay-script integration
# is intentionally kept separate until the complete FireRed source tree is
# present in the project build workspace.

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="${ROOT}/build/pokefirered"

if [[ ! -d "${BUILD_DIR}" ]]; then
    echo "Expected FireRed source at ${BUILD_DIR}" >&2
    exit 1
fi

mkdir -p "${BUILD_DIR}/include/asterra"
cp "${ROOT}/src/starter_system/starter_sets.h" "${BUILD_DIR}/include/asterra/starter_sets.h"
cp "${ROOT}/src/starter_system/rival_logic.h" "${BUILD_DIR}/include/asterra/rival_logic.h"

echo "Asterra v0.2 starter data overlay installed."
