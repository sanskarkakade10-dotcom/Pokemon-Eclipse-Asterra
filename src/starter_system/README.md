# v0.2 Starter System Integration

This directory contains the data-driven core for the Asterra multi-generation starter system.

## Integration contract

The FireRed-derived game layer should call these operations from its opening field script:

1. `AsterraGetStarter(generation, choice)` — resolve the selected species.
2. `AsterraGetRivalStarter(generation, choice)` — resolve Nova's counter.
3. Store the selected generation and choice in game variables/save data.
4. Give the selected species to the player's party.
5. Build Nova's opening party from the rival species.

The first supported generation set is I–III. The API is intentionally generation-indexed so later generations can be added without changing the field-script flow.

## GBA safety

The integration must use FireRed's native party, variables, script, task and battle systems. Do not implement the feature through browser JavaScript or an external runtime.
