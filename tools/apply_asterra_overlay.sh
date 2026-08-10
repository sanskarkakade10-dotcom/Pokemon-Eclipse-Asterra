#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="${ROOT}/build/pokefirered"
UPSTREAM_COMMIT="c75f352304d529f6ba92d4f74b9cf8b5c3810788"

if [[ ! -d "${BUILD_DIR}" ]]; then
    echo "Expected FireRed source at ${BUILD_DIR}" >&2
    exit 1
fi

actual="$(git -C "${BUILD_DIR}" rev-parse HEAD)"
if [[ "${actual}" != "${UPSTREAM_COMMIT}" ]]; then
    echo "Unexpected FireRed source revision: ${actual}" >&2
    echo "Expected: ${UPSTREAM_COMMIT}" >&2
    exit 1
fi

mkdir -p "${BUILD_DIR}/include/asterra"
cp "${ROOT}/src/starter_system/starter_sets.h" "${BUILD_DIR}/include/asterra/starter_sets.h"
cp "${ROOT}/src/starter_system/rival_logic.h" "${BUILD_DIR}/include/asterra/rival_logic.h"
cp "${ROOT}/src/starter_system/starter_selection.c" "${BUILD_DIR}/src/asterra_starter_selection.c"

# This build gate intentionally does not rewrite FireRed's opening script yet.
# The script/menu integration is being implemented against this pinned source
# revision so that the first playable build is reproducible and reviewable.

echo "Asterra v0.2 source overlay installed against ${UPSTREAM_COMMIT}."
