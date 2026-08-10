#ifndef ASTERRA_RIVAL_LOGIC_H
#define ASTERRA_RIVAL_LOGIC_H

#include "starter_sets.h"

static inline unsigned char AsterraGetRivalStarterIndex(unsigned char playerIndex)
{
    return (unsigned char)((playerIndex + 2) % 3);
}

static inline AsterraSpecies AsterraGetRivalStarter(
    enum AsterraStarterGeneration generation,
    unsigned char playerIndex)
{
    if (generation >= ASTERRA_STARTER_GENERATION_COUNT || playerIndex >= 3)
        return 0;
    return (&gAsterraStarterSets[generation].first)[AsterraGetRivalStarterIndex(playerIndex)];
}

#endif
