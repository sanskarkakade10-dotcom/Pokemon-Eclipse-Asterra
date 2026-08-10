#ifndef ASTERRA_STARTER_SETS_H
#define ASTERRA_STARTER_SETS_H

/*
 * Pokémon Eclipse / Asterra v0.2
 * Initial multi-generation starter data.
 *
 * Species IDs use the standard FireRed/BPRE species numbering.
 * The actual script/menu integration will consume this data in the
 * buildable FireRed-derived source tree.
 */

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
    { 1,   4,   7   }, /* Bulbasaur, Charmander, Squirtle */
    { 152, 155, 158 }, /* Chikorita, Cyndaquil, Totodile */
    { 252, 255, 258 }  /* Treecko, Torchic, Mudkip */
};

#endif /* ASTERRA_STARTER_SETS_H */
