# GBA Compatibility

Pokémon Eclipse is being developed as a **Game Boy Advance ROM (`.gba`)**. The target is a normal FireRed-compatible GBA image, not a web-only game.

## Browser target

The intended browser test target is the GBA emulator at:

https://gba.44670.org/

The project should therefore preserve standard GBA behavior: no external runtime, no browser APIs inside the game, and no dependence on files outside the ROM while playing.

## Build philosophy

The upstream FireRed decompilation can assemble a `pokefirered.gba` image with `make`; its documented reference build has SHA-1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`. See:

https://github.com/pret/pokefirered

The Eclipse project will ultimately build from source and produce a normal `.gba` artifact. The original base ROM must not be committed to this repository.

## Testing checklist

Every playable release should be checked for:

- Boots to title screen.
- New game starts correctly.
- Save/load works.
- Player can move between maps.
- Text boxes render correctly.
- Pokémon battles start and end correctly.
- Starter selection works.
- No softlocks in the opening sequence.
- Route encounters use valid species IDs.
- ROM can be loaded by a standard GBA emulator.
- Final artifact has a `.gba` extension.

## Release rule

A release should not be labelled `playable` until the resulting `.gba` has been tested in at least one desktop GBA emulator and, preferably, the target browser emulator as well.
