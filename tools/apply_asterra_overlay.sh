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

python3 "${ROOT}/tools/patch_starter_scene.py"
python3 "${ROOT}/tools/patch_nova_trainers.py"

# FireRed's trainerbattle command stores its defeat-text reference as a
# 16-bit script relocation. The newly generated Asterra defeat label can sit
# beyond that range in script_data, so use the existing in-range rival victory
# text for the trainerbattle defeat slot. The custom Asterra post-battle text
# remains available through the normal msgbox command, which uses a full
# script pointer.
sed -i 's/PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat/Text_RivalVictory/g' \
    "${BUILD_DIR}/data/maps/PalletTown_ProfessorOaksLab/scripts.inc"

echo "Asterra v0.2 starter core, native starter selection, and Nova battle integration installed against ${UPSTREAM_COMMIT}."
