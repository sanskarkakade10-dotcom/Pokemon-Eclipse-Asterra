#include <assert.h>
#include "starter_selection.c"

int main(void)
{
    /* Gen I */
    assert(AsterraGetStarter(ASTERRA_GEN_I, 0) == 1);
    assert(AsterraGetStarter(ASTERRA_GEN_I, 1) == 4);
    assert(AsterraGetStarter(ASTERRA_GEN_I, 2) == 7);

    /* Gen II */
    assert(AsterraGetStarter(ASTERRA_GEN_II, 0) == 152);
    assert(AsterraGetStarter(ASTERRA_GEN_II, 1) == 155);
    assert(AsterraGetStarter(ASTERRA_GEN_II, 2) == 158);

    /* Gen III */
    assert(AsterraGetStarter(ASTERRA_GEN_III, 0) == 252);
    assert(AsterraGetStarter(ASTERRA_GEN_III, 1) == 255);
    assert(AsterraGetStarter(ASTERRA_GEN_III, 2) == 258);

    /* Nova's counters */
    assert(AsterraGetNovaStarter(ASTERRA_GEN_I, 0) == 7);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_I, 1) == 1);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_I, 2) == 4);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_II, 0) == 158);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_II, 1) == 152);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_II, 2) == 155);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_III, 0) == 258);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_III, 1) == 252);
    assert(AsterraGetNovaStarter(ASTERRA_GEN_III, 2) == 255);

    /* Invalid input must never resolve to a real species. */
    assert(AsterraGetStarter(99, 0) == 0);
    assert(AsterraGetStarter(ASTERRA_GEN_I, 99) == 0);

    return 0;
}
