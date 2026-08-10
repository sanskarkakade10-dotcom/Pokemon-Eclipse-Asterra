#ifndef ASTERRA_STARTER_SETS_H
#define ASTERRA_STARTER_SETS_H

typedef unsigned short AsterraSpecies;

typedef struct
{
    AsterraSpecies first;
    AsterraSpecies second;
    AsterraSpecies third;
} AsterraStarterSet;

enum AsterraStarterGeneration
{
    ASTERRA_GEN_I = 0,
    ASTERRA_GEN_II,
    ASTERRA_GEN_III,
    ASTERRA_STARTER_GENERATION_COUNT
};

static const AsterraStarterSet gAsterraStarterSets[ASTERRA_STARTER_GENERATION_COUNT] =
{
    { 1,   4,   7   },
    { 152, 155, 158 },
    { 252, 255, 258 }
};

#endif
