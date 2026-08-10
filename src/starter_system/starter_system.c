#include "asterra/starter_sets.h"
#include "asterra/rival_logic.h"

/*
 * v0.2 starter-system core.
 *
 * This file deliberately contains engine-neutral logic first. The next
 * integration step connects these functions to the FireRed field-script
 * engine and menu callbacks. Keeping the data/decision layer independent
 * makes the eventual GBA integration easier to test.
 */

AsterraSpecies AsterraGetPlayerStarter(
    unsigned char generation,
    unsigned char starterIndex)
{
    if (generation >= ASTERRA_STARTER_GENERATION_COUNT || starterIndex >= 3)
        return 0;

    return (&gAsterraStarterSets[generation].first)[starterIndex];
}

AsterraSpecies AsterraGetNovaStarter(
    unsigned char generation,
    unsigned char playerStarterIndex)
{
    return AsterraGetRivalStarter(
        (enum AsterraStarterGeneration)generation,
        playerStarterIndex);
}
