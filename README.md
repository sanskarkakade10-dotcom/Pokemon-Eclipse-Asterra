# Pokémon Eclipse — Asterra

**Version 0.1 — Foundation Build**

Pokémon Eclipse is an original FireRed-based ROM-hack project set in the new **Asterra** region.

> This repository contains project documentation, source/data work, tools, and patches. It does **not** contain the original Pokémon FireRed ROM.

## Current status

### v0.1 Foundation

- Asterra project identity established.
- Opening concept introduced.
- First town renamed to **Aster Haven**.
- Rival concept established as **Nova**.
- **Bulbasaur, Charmander, and Squirtle remain the classic starter trio.**
- Route 1 is being used as the first bridge into a multi-generation Pokémon ecosystem.
- Route 1 encounter design currently showcases Pokémon from Generations I–III.

### Core story

Asterra is experiencing a mysterious phenomenon known as the **Eclipse Cycle**. During a rare event called the **Black Eclipse**, Pokémon begin displaying strange changes that appear connected to ancient forces beneath the region.

The player and rival **Nova** become involved after the phenomenon reaches their home. A new professor, **Lyra**, begins investigating the event while the mysterious organization **Team Umbra** attempts to exploit it.

## Design pillars

- A genuinely new region and adventure rather than a retelling of Kanto.
- Strong exploration and environmental storytelling.
- A modernized Pokémon selection while preserving the classic Kanto starters.
- Original towns, routes, characters, events, gyms, Elite Four and post-game content.
- Quality-of-life improvements while retaining the feel of a Generation III Pokémon game.

## Repository layout

```text
├── README.md
├── CHANGELOG.md
├── .gitignore
├── docs/
│   ├── GAME_DESIGN.md
│   ├── ASTERRA_REGION.md
│   ├── STORY.md
│   ├── CHARACTERS.md
│   └── DEVELOPMENT_ROADMAP.md
├── data/
│   ├── pokemon/
│   ├── encounters/
│   ├── trainers/
│   └── maps/
├── graphics/
│   ├── pokemon/
│   ├── trainers/
│   ├── overworld/
│   ├── maps/
│   └── ui/
├── scripts/
├── src/
├── tools/
└── patches/
    └── v0.1/
```

## Base ROM

Development targets the **English Pokémon FireRed v1.0 (BPRE)** base. The original ROM is not distributed in this repository. Builds/patches are intended to be applied to the user's own legally obtained compatible base ROM.

## Asset policy

Pokémon Eclipse may use Pokémon-related references/assets during development where appropriate, but the repository should avoid redistributing the original copyrighted FireRed ROM. PokéSprite is planned as a reference/source for sprite work; see its licensing/copyright notices at https://msikma.github.io/pokesprite/.

## Development roadmap

1. **v0.1** — Foundation and first-route prototype
2. **v0.2** — Real multi-generation starter-selection system
3. **v0.3** — Asterra opening and first original town
4. **v0.4** — Route 1 and first major exploration area
5. **v0.5** — Team Umbra introduction and first major story event
6. **v0.6+** — Gyms, expanded region, Eclipse storyline, Elite Four, Champion and post-game

## Development principle

Every major feature should be implemented as an actual game-system change where possible—not merely a text or cosmetic replacement.
