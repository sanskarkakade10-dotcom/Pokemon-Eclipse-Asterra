#ifndef ASTERRA_RIVAL_LOGIC_H
#define ASTERRA_RIVAL_LOGIC_H

#include "starter_sets.h"

/*
 * Counter choices are represented by starter index rather than hard-coded
 * species so the rival system can remain compatible with future generations.
 *
 * Index 0 beats the player's index 2.
 * Index 1 beats the player's index 0.
 * Index 2 beats the player's index 1.
 */
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

#endif /* ASTERRA_RIVAL_LOGIC_H */
