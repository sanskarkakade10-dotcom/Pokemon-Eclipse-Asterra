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
    exit 1
fi

mkdir -p "${BUILD_DIR}/include/asterra"
cp "${ROOT}/src/starter_system/starter_sets.h" "${BUILD_DIR}/include/asterra/starter_sets.h"
cp "${ROOT}/src/starter_system/rival_logic.h" "${BUILD_DIR}/include/asterra/rival_logic.h"
cp "${ROOT}/src/starter_system/starter_selection.c" "${BUILD_DIR}/src/asterra_starter_selection.c"

# The native field-script replacement is intentionally gated until its exact
# script-command implementation is validated against this pinned source.
# Do not apply a placeholder patch to the ROM build.

echo "Asterra v0.2 starter core installed against ${UPSTREAM_COMMIT}."
echo "Native field-script integration remains a required v0.2 build gate."
