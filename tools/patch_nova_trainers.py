#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "pokefirered"
OPPONENTS_FILE = BUILD / "include/constants/opponents.h"
PARTY_FILE = BUILD / "src/data/trainer_parties.h"
TRAINERS_FILE = BUILD / "src/data/trainers.h"
SCRIPTS_FILE = BUILD / "data/maps/PalletTown_ProfessorOaksLab/scripts.inc"

PARTY_NAMES = {
    "SQUIRTLE": "sParty_AsterraNovaSquirtle",
    "BULBASAUR": "sParty_AsterraNovaBulbasaur",
    "CHARMANDER": "sParty_AsterraNovaCharmander",
    "TOTODILE": "sParty_AsterraNovaTotodile",
    "CHIKORITA": "sParty_AsterraNovaChikorita",
    "CYNDAQUIL": "sParty_AsterraNovaCyndaquil",
    "MUDKIP": "sParty_AsterraNovaMudkip",
    "TREECKO": "sParty_AsterraNovaTreecko",
    "TORCHIC": "sParty_AsterraNovaTorchic",
}

SPECIES = {
    "SQUIRTLE": "SPECIES_SQUIRTLE",
    "BULBASAUR": "SPECIES_BULBASAUR",
    "CHARMANDER": "SPECIES_CHARMANDER",
    "TOTODILE": "SPECIES_TOTODILE",
    "CHIKORITA": "SPECIES_CHIKORITA",
    "CYNDAQUIL": "SPECIES_CYNDAQUIL",
    "MUDKIP": "SPECIES_MUDKIP",
    "TREECKO": "SPECIES_TREECKO",
    "TORCHIC": "SPECIES_TORCHIC",
}

TRAINER_NAMES = {
    "SQUIRTLE": "TRAINER_ASTERRA_NOVA_SQUIRTLE",
    "BULBASAUR": "TRAINER_ASTERRA_NOVA_BULBASAUR",
    "CHARMANDER": "TRAINER_ASTERRA_NOVA_CHARMANDER",
    "TOTODILE": "TRAINER_ASTERRA_NOVA_TOTODILE",
    "CHIKORITA": "TRAINER_ASTERRA_NOVA_CHIKORITA",
    "CYNDAQUIL": "TRAINER_ASTERRA_NOVA_CYNDAQUIL",
    "MUDKIP": "TRAINER_ASTERRA_NOVA_MUDKIP",
    "TREECKO": "TRAINER_ASTERRA_NOVA_TREECKO",
    "TORCHIC": "TRAINER_ASTERRA_NOVA_TORCHIC",
}

# Keep every filesystem path as a Path object. Do not reuse these names for
# dictionaries or generated text; this makes the overlay safe to re-run.
for required_file in (OPPONENTS_FILE, PARTY_FILE, TRAINERS_FILE, SCRIPTS_FILE):
    if not required_file.is_file():
        raise SystemExit(f"Missing expected FireRed file: {required_file}")

opponents_text = OPPONENTS_FILE.read_text()
if "TRAINER_ASTERRA_NOVA_SQUIRTLE" not in opponents_text:
    marker = "#define NUM_TRAINERS                             743"
    additions = """#define TRAINER_ASTERRA_NOVA_SQUIRTLE           743
#define TRAINER_ASTERRA_NOVA_BULBASAUR          744
#define TRAINER_ASTERRA_NOVA_CHARMANDER         745
#define TRAINER_ASTERRA_NOVA_TOTODILE           746
#define TRAINER_ASTERRA_NOVA_CHIKORITA          747
#define TRAINER_ASTERRA_NOVA_CYNDAQUIL          748
#define TRAINER_ASTERRA_NOVA_MUDKIP             749
#define TRAINER_ASTERRA_NOVA_TREECKO            750
#define TRAINER_ASTERRA_NOVA_TORCHIC            751

#define NUM_TRAINERS                             752"""
    if marker not in opponents_text:
        raise SystemExit("Unexpected upstream opponents.h: NUM_TRAINERS marker not found")
    OPPONENTS_FILE.write_text(opponents_text.replace(marker, additions))

party_text = PARTY_FILE.read_text()
if "sParty_AsterraNovaSquirtle" not in party_text:
    marker = "// Start of actual trainer data"
    party_blocks = []
    for name, party_name in PARTY_NAMES.items():
        party_blocks.append(
            f"static const struct TrainerMonNoItemDefaultMoves {party_name}[] = {{\n"
            "    {\n"
            "        .iv = 0,\n"
            "        .lvl = 5,\n"
            f"        .species = {SPECIES[name]},\n"
            "    },\n"
            "};\n\n"
        )
    if marker not in party_text:
        raise SystemExit("Unexpected upstream trainer_parties.h: insertion marker not found")
    PARTY_FILE.write_text(
        party_text.replace(
            marker,
            "// Asterra v0.2: Nova's generation-aware level-5 counter parties.\n"
            + "".join(party_blocks)
            + marker,
        )
    )

trainer_text = TRAINERS_FILE.read_text()
if "TRAINER_ASTERRA_NOVA_SQUIRTLE" not in trainer_text:
    trainer_entries = []
    for name, party_name in PARTY_NAMES.items():
        trainer_entries.append(
            f"    [{TRAINER_NAMES[name]}] = {{\n"
            "        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,\n"
            "        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,\n"
            "        .trainerPic = TRAINER_PIC_RIVAL_EARLY,\n"
            "        .trainerName = _(\"NOVA\"),\n"
            "        .items = {},\n"
            "        .doubleBattle = FALSE,\n"
            "        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,\n"
            f"        .party = NO_ITEM_DEFAULT_MOVES({party_name}),\n"
            "    },\n"
        )
    trainer_array_end = trainer_text.rfind("\n};")
    if trainer_array_end < 0:
        raise SystemExit("Could not find gTrainers array terminator")
    TRAINERS_FILE.write_text(
        trainer_text[:trainer_array_end]
        + "\n"
        + "".join(trainer_entries)
        + trainer_text[trainer_array_end:]
    )

scripts_text = SCRIPTS_FILE.read_text()
if "AsterraNovaBattle" not in scripts_text:
    marker = "PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived::\n"
    if marker not in scripts_text:
        raise SystemExit("Starter received event was not found in Pallet Town lab scripts")
    start = scripts_text.index(marker)
    end = scripts_text.find("\n\n", start)
    if end < 0:
        raise SystemExit("Could not find end of starter received event")
    current_event = scripts_text[start:end]
    if "AsterraNovaBattle" not in current_event:
        current_event = current_event.replace(
            "\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraStarterReceived\n",
            "\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraStarterReceived\n\tcall PalletTown_ProfessorOaksLab_EventScript_AsterraNovaBattle\n",
        )
    scripts_text = scripts_text[:start] + current_event + scripts_text[end:]

    battle_block = r'''

PalletTown_ProfessorOaksLab_EventScript_AsterraNovaBattle::
	playbgm MUS_ENCOUNTER_RIVAL, 0
	call_if_eq VAR_TEMP_1, 0, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaGenI
	call_if_eq VAR_TEMP_1, 1, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaGenII
	call_if_eq VAR_TEMP_1, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaGenIII
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraNovaAfterBattle
	return

PalletTown_ProfessorOaksLab_EventScript_AsterraNovaGenI::
	call_if_eq VAR_TEMP_2, 0, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaSquirtle
	call_if_eq VAR_TEMP_2, 1, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaBulbasaur
	call_if_eq VAR_TEMP_2, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaCharmander
	return

PalletTown_ProfessorOaksLab_EventScript_AsterraNovaGenII::
	call_if_eq VAR_TEMP_2, 0, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaTotodile
	call_if_eq VAR_TEMP_2, 1, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaChikorita
	call_if_eq VAR_TEMP_2, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaCyndaquil
	return

PalletTown_ProfessorOaksLab_EventScript_AsterraNovaGenIII::
	call_if_eq VAR_TEMP_2, 0, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaMudkip
	call_if_eq VAR_TEMP_2, 1, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaTreecko
	call_if_eq VAR_TEMP_2, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraNovaTorchic
	return

PalletTown_ProfessorOaksLab_EventScript_AsterraNovaSquirtle::
	trainerbattle TRAINER_ASTERRA_NOVA_SQUIRTLE, 0, PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat, Text_RivalVictory
	return
PalletTown_ProfessorOaksLab_EventScript_AsterraNovaBulbasaur::
	trainerbattle TRAINER_ASTERRA_NOVA_BULBASAUR, 0, PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat, Text_RivalVictory
	return
PalletTown_ProfessorOaksLab_EventScript_AsterraNovaCharmander::
	trainerbattle TRAINER_ASTERRA_NOVA_CHARMANDER, 0, PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat, Text_RivalVictory
	return
PalletTown_ProfessorOaksLab_EventScript_AsterraNovaTotodile::
	trainerbattle TRAINER_ASTERRA_NOVA_TOTODILE, 0, PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat, Text_RivalVictory
	return
PalletTown_ProfessorOaksLab_EventScript_AsterraNovaChikorita::
	trainerbattle TRAINER_ASTERRA_NOVA_CHIKORITA, 0, PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat, Text_RivalVictory
	return
PalletTown_ProfessorOaksLab_EventScript_AsterraNovaCyndaquil::
	trainerbattle TRAINER_ASTERRA_NOVA_CYNDAQUIL, 0, PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat, Text_RivalVictory
	return
PalletTown_ProfessorOaksLab_EventScript_AsterraNovaMudkip::
	trainerbattle TRAINER_ASTERRA_NOVA_MUDKIP, 0, PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat, Text_RivalVictory
	return
PalletTown_ProfessorOaksLab_EventScript_AsterraNovaTreecko::
	trainerbattle TRAINER_ASTERRA_NOVA_TREECKO, 0, PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat, Text_RivalVictory
	return
PalletTown_ProfessorOaksLab_EventScript_AsterraNovaTorchic::
	trainerbattle TRAINER_ASTERRA_NOVA_TORCHIC, 0, PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat, Text_RivalVictory
	return

PalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat::
	.string "NOVA: Not bad, {PLAYER}!$"

PalletTown_ProfessorOaksLab_Text_AsterraNovaAfterBattle::
	.string "NOVA: This is only the beginning.\\nLet's see what Asterra has in store!$"
'''
    SCRIPTS_FILE.write_text(scripts_text + battle_block)

print("Asterra v0.2 Nova trainer parties and native opening battle integration applied.")
