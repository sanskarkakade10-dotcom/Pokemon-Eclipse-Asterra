# Release Process

Pokémon Eclipse releases are distributed as patches/source artifacts rather than the copyrighted FireRed base ROM.

## Development

1. Use a compatible, legally obtained English FireRed v1.0 base.
2. Build the project from source.
3. Produce a `.gba` build locally.
4. Test the `.gba` in mGBA or another standard GBA emulator.
5. Test the same artifact in the project's target browser emulator when possible.
6. Record the build/version in `CHANGELOG.md`.
7. Publish the patch/source release without committing the base ROM.

## Browser compatibility requirement

The finished game must remain a normal GBA ROM so a user can load the `.gba` into a web GBA emulator such as https://gba.44670.org/.

No browser-specific game code should be required.

## Save compatibility

Unless explicitly documented otherwise, major development builds should be treated as requiring a new save file. Release notes must call out save incompatibilities.
