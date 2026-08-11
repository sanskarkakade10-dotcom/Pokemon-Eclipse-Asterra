#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "pokefirered"
OPPONENTS = BUILD / "include/constants/opponents.h"
PARTY_FILE = BUILD / "src/data/trainer_parties.h"
TRAINERS = BUILD / "src/data/trainers.h"
SCRIPTS = BUILD / "data/maps/PalletTown_ProfessorOaksLab/scripts.inc"

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

# Add nine dedicated Nova trainers in the unused trainer-ID range immediately
# after the upstream NUM_TRAINERS value (743 -> 752).
opp = OPPONENTS.read_text()
if "TRAINER_ASTERRA_NOVA_SQUIRTLE" not in opp:
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
    opp = opp.replace(marker, additions)
    OPPONENTS.write_text(opp)

party_text = PARTY_FILE.read_text()
if "sParty_AsterraNovaSquirtle" not in party_text:
    marker = "// Start of actual trainer data"
    blocks = []
    for name, party_name in PARTY_NAMES.items():
        blocks.append(
            f"static const struct TrainerMonNoItemDefaultMoves {party_name}[] = {{\n"
            "    {\n"
            "        .iv = 0,\n"
            "        .lvl = 5,\n"
            f"        .species = {SPECIES[name]},\n"
            "    },\n"
            "};\n\n"
        )
    party_text = party_text.replace(marker, "// Asterra v0.2: Nova's generation-aware level-5 counter parties.\n" + "".join(blocks) + marker)
    PARTY_FILE.write_text(party_text)

trainer_text = TRAINERS.read_text()
if "TRAINER_ASTERRA_NOVA_SQUIRTLE" not in trainer_text:
    entries = []
    for name, party_name in PARTY_NAMES.items():
        entries.append(
            f"    [{TRAINER_NAMES[name]}] = {{\n"
            "        .trainerClass = TRAINER_CLASS_RIVAL,\n"
            "        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_RIVAL,\n"
            "        .trainerPic = TRAINER_PIC_RIVAL,\n"
            "        .trainerName = _(\"NOVA\"),\n"
            "        .items = {},\n"
            "        .doubleBattle = FALSE,\n"
            "        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE,\n"
            f"        .party = NO_ITEM_DEFAULT_MOVES({party_name}),\n"
            "    },\n"
        )
    last = trainer_text.rfind("\n};")
    if last < 0:
        raise SystemExit("Could not find gTrainers array terminator")
    trainer_text = trainer_text[:last] + "\n" + "".join(entries) + trainer_text[last:]
    TRAINERS.write_text(trainer_text)

scripts = SCRIPTS.read_text()
if "AsterraNovaBattle" not in scripts:
    marker = "PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived::\n"
    start = scripts.index(marker)
    end = scripts.index("\n\n", start)
    current = scripts[start:end]
    replacement = current.replace(
        "\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraStarterReceived\n",
        "\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraStarterReceived\n\tcall PalletTown_ProfessorOaksLab_EventScript_AsterraNovaBattle\n",
    )
    scripts = scripts[:start] + replacement + scripts[end:]

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
    scripts += battle_block
    SCRIPTS.write_text(scripts)

print("Asterra v0.2 Nova trainer parties and native opening battle integration applied.")
