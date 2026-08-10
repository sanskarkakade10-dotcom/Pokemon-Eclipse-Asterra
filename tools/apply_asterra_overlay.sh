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

# Native FireRed script integration.
# Keep the upstream script available as a reference and install the Asterra
# starter-lab replacement as an explicit patch artifact. The build workflow
# applies this patch only after verifying the pinned upstream revision.
PATCH="${ROOT}/patches/v0.2/starter_lab_integration.patch"
if [[ ! -f "${PATCH}" ]]; then
    echo "Missing starter-lab integration patch: ${PATCH}" >&2
    exit 1
fi

patch -d "${BUILD_DIR}" -p1 --forward < "${PATCH}"

echo "Asterra v0.2 native starter overlay installed against ${UPSTREAM_COMMIT}."
