#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "pokefirered"
OPPONENTS = BUILD / "include/constants/opponents.h"
PARTIES = BUILD / "src/data/trainer_parties.h"
TRAINERS = BUILD / "src/data/trainers.h"
SCRIPTS = BUILD / "data/maps/PalletTown_ProfessorOaksLab/scripts.inc"

TRAINER_IDS = {
    "SQUIRTLE": 743,
    "BULBASAUR": 744,
    "CHARMANDER": 745,
    "TOTODILE": 746,
    "CHIKORITA": 747,
    "CYNDAQUIL": 748,
    "MUDKIP": 749,
    "TREECKO": 750,
    "TORCHIC": 751,
}

PARTIES = {
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

# Add nine dedicated Nova trainers in the unused trainer-ID range immediately
# after the upstream NUM_TRAINERS value (743 -> 752).
opp = OPPONENTS.read_text()
if "TRAINER_ASTERRA_NOVA_SQUIRTLE" not in opp:
    marker = "#define NUM_TRAINERS                             743"
    additions = """#define TRAINER_ASTERRA_NOVA_SQUIRTLE           743\n#define TRAINER_ASTERRA_NOVA_BULBASAUR          744\n#define TRAINER_ASTERRA_NOVA_CHARMANDER         745\n#define TRAINER_ASTERRA_NOVA_TOTODILE           746\n#define TRAINER_ASTERRA_NOVA_CHIKORITA          747\n#define TRAINER_ASTERRA_NOVA_CYNDAQUIL          748\n#define TRAINER_ASTERRA_NOVA_MUDKIP             749\n#define TRAINER_ASTERRA_NOVA_TREECKO            750\n#define TRAINER_ASTERRA_NOVA_TORCHIC            751\n\n#define NUM_TRAINERS                             752"""
    opp = opp.replace(marker, additions)
    OPPONENTS.write_text(opp)

# Add simple level-5 parties before the actual trainer-party section.
party_text = PARTIES.read_text()
if "sParty_AsterraNovaSquirtle" not in party_text:
    marker = "// Start of actual trainer data"
    block = "\n".join(
        [
            "// Asterra v0.2: Nova's generation-aware level-5 counter parties.",
        ]
        + [
            f"static const struct TrainerMonNoItemDefaultMoves {PARTIES[name]}[] = {{",
            "    {",
            "        .iv = 0,",
            "        .lvl = 5,",
            f"        .species = {SPECIES[name]},",
            "    },",
            "};",
            "",
        ]
        for name in PARTIES
    )
    party_text = party_text.replace(marker, block + marker)
    PARTIES.write_text(party_text)

# Add nine trainer records immediately before the trainer array terminator.
trainer_text = TRAINERS.read_text()
if "TRAINER_ASTERRA_NOVA_SQUIRTLE" not in trainer_text:
    entries = []
    for name in PARTIES:
        entries.append(
            f'''    [TRAINER_ASTERRA_NOVA_{name}] = {{\n'''
            "        .trainerClass = TRAINER_CLASS_RIVAL,\n"
            "        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_RIVAL,\n"
            "        .trainerPic = TRAINER_PIC_RIVAL,\n"
            "        .trainerName = _(\"NOVA\"),\n"
            "        .items = {},\n"
            "        .doubleBattle = FALSE,\n"
            "        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE,\n"
            f"        .party = NO_ITEM_DEFAULT_MOVES({PARTIES[name]}),\n"
            "    },\n"
        )
    last = trainer_text.rfind("\n};")
    if last < 0:
        raise SystemExit("Could not find gTrainers array terminator")
    trainer_text = trainer_text[:last] + "\n" + "".join(entries) + trainer_text[last:]
    TRAINERS.write_text(trainer_text)

# Add the nine battle branches to the starter scene after the starter is received.
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
'''
    scripts += battle_block
    scripts += '\nPalletTown_ProfessorOaksLab_Text_AsterraNovaDefeat::\n    .string "NOVA: Not bad, {PLAYER}!$"\n'
    scripts += 'PalletTown_ProfessorOaksLab_Text_AsterraNovaAfterBattle::\n    .string "NOVA: This is only the beginning.\nLet\'s see what Asterra has in store!$"\n'
    SCRIPTS.write_text(scripts)

print("Asterra v0.2 Nova trainer parties and native opening battle integration applied.")
