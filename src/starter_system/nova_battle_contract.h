#ifndef ASTERRA_NOVA_BATTLE_CONTRACT_H
#define ASTERRA_NOVA_BATTLE_CONTRACT_H

#include "nova_trainers.h"

/*
 * Native FireRed battle integration contract.
 *
 * The field-script layer should:
 *   1. Resolve the player's generation and starter index.
 *   2. Call AsterraGetNovaOpeningMon().
 *   3. Create the corresponding native trainer/party entry.
 *   4. Start the standard trainer battle script.
 *
 * This header deliberately does not invent a new battle engine. The final
 * integration must use FireRed's existing trainer battle infrastructure.
 */

enum AsterraNovaBattleResult
{
    ASTERRA_NOVA_BATTLE_READY = 0,
    ASTERRA_NOVA_BATTLE_INVALID_SELECTION
};

static inline enum AsterraNovaBattleResult AsterraPrepareNovaBattle(
    unsigned char generation,
    unsigned char playerChoice,
    AsterraNovaOpeningMon *outMon)
{
    AsterraNovaOpeningMon mon = AsterraGetNovaOpeningMon(generation, playerChoice);
    if (mon.species == 0 || mon.level == 0)
        return ASTERRA_NOVA_BATTLE_INVALID_SELECTION;

    *outMon = mon;
    return ASTERRA_NOVA_BATTLE_READY;
}

#endif /* ASTERRA_NOVA_BATTLE_CONTRACT_H */
