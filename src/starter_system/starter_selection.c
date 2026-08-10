#include "starter_sets.h"
#include "rival_logic.h"

/*
 * Pure game-data layer for the v0.2 selection flow.
 * The native FireRed script layer should call these functions when wiring
 * the menu and party/battle operations into the ROM.
 */
AsterraSpecies AsterraGetStarter(unsigned char generation, unsigned char choice)
{
    if (generation >= ASTERRA_STARTER_GENERATION_COUNT || choice >= 3)
        return 0;

    return (&gAsterraStarterSets[generation].first)[choice];
}

AsterraSpecies AsterraGetNovaStarter(unsigned char generation, unsigned char playerChoice)
{
    return AsterraGetRivalStarter(
        (enum AsterraStarterGeneration)generation,
        playerChoice
    );
}
