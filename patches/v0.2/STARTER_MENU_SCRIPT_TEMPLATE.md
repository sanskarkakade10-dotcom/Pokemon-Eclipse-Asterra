# v0.2 Starter Menu Integration Template

This template defines the exact native FireRed script flow that the implementation should wire into the starter-lab scene.

## Flow

```text
Choose Starter Scene
  -> Choose Generation (I / II / III)
  -> Set generation variable
  -> Choose Partner (three species for selected generation)
  -> Set starter-choice variable
  -> Resolve species through Asterra starter data
  -> Give Pokémon to player
  -> Set Nova's starter from the same generation
  -> Start Nova battle
```

## Native script requirements

The implementation should use FireRed's existing script commands and menu infrastructure rather than introducing a custom runtime.

Required state:

- selected generation
- selected starter index
- resolved player species
- resolved Nova species
- starter-confirmed flag

## Safety requirements

- Invalid menu results must return to a safe menu state.
- Cancel/back must not grant a Pokémon.
- The player must receive exactly one starter.
- Nova's species must match the selected generation.
- The script must not proceed to the rival battle until the player's party contains the selected starter.
- A fresh save must not inherit starter-selection state from an old save.

## Implementation note

This file is a specification/template. It intentionally does not pretend to be compiled game script until it is applied against the pinned FireRed source tree and verified by the build/test pipeline.
