#ifndef ASTERRA_NOVA_TRAINERS_H
#define ASTERRA_NOVA_TRAINERS_H

#include "starter_sets.h"

/*
 * Nova's opening teams for the first three supported generations.
 * The battle layer can resolve the selected generation + player choice
 * through AsterraGetNovaStarter().
 */
typedef struct
{
    AsterraSpecies species;
    unsigned char level;
} AsterraNovaOpeningMon;

static const AsterraNovaOpeningMon gAsterraNovaOpeningTeams[ASTERRA_STARTER_GENERATION_COUNT][3] =
{
    {
        { 7, 5 }, { 1, 5 }, { 4, 5 }
    },
    {
        { 158, 5 }, { 152, 5 }, { 155, 5 }
    },
    {
        { 258, 5 }, { 252, 5 }, { 255, 5 }
    }
};

static inline AsterraNovaOpeningMon AsterraGetNovaOpeningMon(
    unsigned char generation,
    unsigned char playerChoice)
{
    AsterraNovaOpeningMon invalid = { 0, 0 };
    if (generation >= ASTERRA_STARTER_GENERATION_COUNT || playerChoice >= 3)
        return invalid;

    return gAsterraNovaOpeningTeams[generation][playerChoice];
}

#endif /* ASTERRA_NOVA_TRAINERS_H */
