# Starter System — v0.2 Specification

## Goal

At the beginning of Pokémon Eclipse, the player should be able to keep the original Kanto starter trio while also choosing a starter from another generation.

The system must be a real in-game selection flow, not a cosmetic rename.

## Planned flow

1. Professor Lyra introduces the Eclipse phenomenon.
2. The player reaches the starter laboratory.
3. A generation-selection menu appears.
4. The player chooses a generation.
5. The three starters from that generation are shown.
6. The player chooses one Pokémon.
7. The chosen Pokémon is given to the player.
8. Nova receives an appropriate rival choice based on the player's starter.
9. The story continues into Aster Haven / the first Asterra route.

## Initial supported generations

The first implementation target is:

- Generation I — Bulbasaur / Charmander / Squirtle
- Generation II — Chikorita / Cyndaquil / Totodile
- Generation III — Treecko / Torchic / Mudkip

Later builds can extend the same data-driven system to Generations IV onward.

## Technical constraints

- Must remain a standard GBA `.gba` build.
- Must not require an external program while playing.
- Species, moves, starter data and rival selection should be data-driven where possible.
- The feature must work in standard GBA emulators, including the project's browser-emulator target.
- The original FireRed starter flow should be replaced cleanly rather than leaving unreachable or conflicting scripts.

## Rival logic

Nova should choose a Pokémon that creates a sensible matchup against the player's choice. The exact difficulty curve will be finalized during implementation and testing.

## Acceptance criteria

v0.2 is complete when a fresh save can:

- enter the new starter scene;
- select Generation I, II or III;
- select one of the three starters in that generation;
- receive the correct Pokémon;
- trigger Nova's correct corresponding choice;
- save and reload without corrupting the party;
- continue into the opening route without a softlock.
