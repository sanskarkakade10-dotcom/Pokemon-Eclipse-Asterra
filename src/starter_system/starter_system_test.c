#include <assert.h>
#include "starter_system.c"

int main(void)
{
    assert(AsterraGetPlayerStarter(ASTERRA_GEN_I, 0) == 1);
    assert(AsterraGetPlayerStarter(ASTERRA_GEN_I, 1) == 4);
    assert(AsterraGetPlayerStarter(ASTERRA_GEN_I, 2) == 7);

    assert(AsterraGetPlayerStarter(ASTERRA_GEN_II, 0) == 152);
    assert(AsterraGetPlayerStarter(ASTERRA_GEN_II, 1) == 155);
    assert(AsterraGetPlayerStarter(ASTERRA_GEN_II, 2) == 158);

    assert(AsterraGetPlayerStarter(ASTERRA_GEN_III, 0) == 252);
    assert(AsterraGetPlayerStarter(ASTERRA_GEN_III, 1) == 255);
    assert(AsterraGetPlayerStarter(ASTERRA_GEN_III, 2) == 258);

    /* Nova takes the cyclic counter starter. */
    assert(AsterraGetNovaStarter(ASTERRA_GEN_I, 0) == 7);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_I, 1) == 1);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_I, 2) == 4);

    /* Invalid selections must never produce a Pokémon. */
    assert(AsterraGetPlayerStarter(99, 0) == 0);
    assert(AsterraGetPlayerStarter(ASTERRA_GEN_I, 99) == 0);
    assert(AsterraGetNovaStarter(99, 0) == 0);

    return 0;
}
