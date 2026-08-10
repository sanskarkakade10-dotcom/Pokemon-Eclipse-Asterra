#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "pokefirered"
SCRIPTS = BUILD / "data/maps/PalletTown_ProfessorOaksLab/scripts.inc"
TEXT = BUILD / "data/maps/PalletTown_ProfessorOaksLab/text.inc"

scene_start = "PalletTown_ProfessorOaksLab_ChooseStarterScene::"
scene_end = "PalletTown_ProfessorOaksLab_Movement_OakEnter::"

new_scene = r'''PalletTown_ProfessorOaksLab_ChooseStarterScene::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	applymovement LOCALID_OAKS_LAB_PROF_OAK, PalletTown_ProfessorOaksLab_Movement_OakEnter
	waitmovement 0
	removeobject LOCALID_OAKS_LAB_PROF_OAK
	setobjectxyperm LOCALID_OAKS_LAB_PROF_OAK, 6, 3
	setobjectmovementtype LOCALID_OAKS_LAB_PROF_OAK, MOVEMENT_TYPE_FACE_DOWN
	clearflag FLAG_HIDE_OAK_IN_HIS_LAB
	applymovement LOCALID_PLAYER, PalletTown_ProfessorOaksLab_Movement_PlayerEnter
	waitmovement 0
	applymovement LOCALID_OAKS_LAB_RIVAL, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	clearflag FLAG_DONT_TRANSITION_MUSIC
	savebgm MUS_DUMMY
	fadedefaultbgm
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraWelcome
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraChooseGenerationI MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGenI
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraChooseGenerationII MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGenII
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraChooseGenerationIII MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGenIII
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraChooseGenerationAgain
	goto PalletTown_ProfessorOaksLab_ChooseStarterScene
	end

PalletTown_ProfessorOaksLab_EventScript_AsterraGenI::
	setvar VAR_TEMP_1, 0
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenI
	end

PalletTown_ProfessorOaksLab_EventScript_AsterraGenII::
	setvar VAR_TEMP_1, 1
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenII
	end

PalletTown_ProfessorOaksLab_EventScript_AsterraGenIII::
	setvar VAR_TEMP_1, 2
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenIII
	end

PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenI::
	showmonpic SPECIES_BULBASAUR, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraBulbasaur MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGiveBulbasaur
	showmonpic SPECIES_CHARMANDER, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraCharmander MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGiveCharmander
	showmonpic SPECIES_SQUIRTLE, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraSquirtle MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGiveSquirtle
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenI
	end

PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenII::
	showmonpic SPECIES_CHIKORITA, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraChikorita MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGiveChikorita
	showmonpic SPECIES_CYNDAQUIL, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraCyndaquil MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGiveCyndaquil
	showmonpic SPECIES_TOTODILE, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraTotodile MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGiveTotodile
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenII
	end

PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenIII::
	showmonpic SPECIES_TREECKO, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraTreecko MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGiveTreecko
	showmonpic SPECIES_TORCHIC, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraTorchic MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGiveTorchic
	showmonpic SPECIES_MUDKIP, 10, 3
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraMudkip MSGBOX_YESNO
	hidemonpic
	goto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGiveMudkip
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenIII
	end

PalletTown_ProfessorOaksLab_EventScript_AsterraGiveBulbasaur::
	setvar VAR_TEMP_2, 0
	setvar VAR_STARTER_MON, 0
	givemon SPECIES_BULBASAUR, 5
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived
	end
PalletTown_ProfessorOaksLab_EventScript_AsterraGiveCharmander::
	setvar VAR_TEMP_2, 1
	setvar VAR_STARTER_MON, 1
	givemon SPECIES_CHARMANDER, 5
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived
	end
PalletTown_ProfessorOaksLab_EventScript_AsterraGiveSquirtle::
	setvar VAR_TEMP_2, 2
	setvar VAR_STARTER_MON, 2
	givemon SPECIES_SQUIRTLE, 5
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived
	end
PalletTown_ProfessorOaksLab_EventScript_AsterraGiveChikorita::
	setvar VAR_TEMP_2, 0
	givemon SPECIES_CHIKORITA, 5
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived
	end
PalletTown_ProfessorOaksLab_EventScript_AsterraGiveCyndaquil::
	setvar VAR_TEMP_2, 1
	givemon SPECIES_CYNDAQUIL, 5
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived
	end
PalletTown_ProfessorOaksLab_EventScript_AsterraGiveTotodile::
	setvar VAR_TEMP_2, 2
	givemon SPECIES_TOTODILE, 5
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived
	end
PalletTown_ProfessorOaksLab_EventScript_AsterraGiveTreecko::
	setvar VAR_TEMP_2, 0
	givemon SPECIES_TREECKO, 5
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived
	end
PalletTown_ProfessorOaksLab_EventScript_AsterraGiveTorchic::
	setvar VAR_TEMP_2, 1
	givemon SPECIES_TORCHIC, 5
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived
	end
PalletTown_ProfessorOaksLab_EventScript_AsterraGiveMudkip::
	setvar VAR_TEMP_2, 2
	givemon SPECIES_MUDKIP, 5
	goto PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived
	end

PalletTown_ProfessorOaksLab_EventScript_AsterraStarterReceived::
	bufferleadmonspeciesname STR_VAR_1
	msgbox PalletTown_ProfessorOaksLab_Text_AsterraStarterReceived
	setvar VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 3
	releaseall
	end

'''

text_add = r'''

PalletTown_ProfessorOaksLab_Text_AsterraWelcome::
    .string "PROF. OAK: Welcome to ASTERRA!\p"
    .string "Today, you can choose a partner\n"
    .string "from three different generations.$"

PalletTown_ProfessorOaksLab_Text_AsterraChooseGenerationI::
    .string "Would you like to choose from\n"
    .string "GENERATION I?$"
PalletTown_ProfessorOaksLab_Text_AsterraChooseGenerationII::
    .string "Would you like to choose from\n"
    .string "GENERATION II?$"
PalletTown_ProfessorOaksLab_Text_AsterraChooseGenerationIII::
    .string "Would you like to choose from\n"
    .string "GENERATION III?$"
PalletTown_ProfessorOaksLab_Text_AsterraChooseGenerationAgain::
    .string "Let's choose a generation first.$"

PalletTown_ProfessorOaksLab_Text_AsterraBulbasaur::
    .string "Choose BULBASAUR?$"
PalletTown_ProfessorOaksLab_Text_AsterraCharmander::
    .string "Choose CHARMANDER?$"
PalletTown_ProfessorOaksLab_Text_AsterraSquirtle::
    .string "Choose SQUIRTLE?$"
PalletTown_ProfessorOaksLab_Text_AsterraChikorita::
    .string "Choose CHIKORITA?$"
PalletTown_ProfessorOaksLab_Text_AsterraCyndaquil::
    .string "Choose CYNDAQUIL?$"
PalletTown_ProfessorOaksLab_Text_AsterraTotodile::
    .string "Choose TOTODILE?$"
PalletTown_ProfessorOaksLab_Text_AsterraTreecko::
    .string "Choose TREECKO?$"
PalletTown_ProfessorOaksLab_Text_AsterraTorchic::
    .string "Choose TORCHIC?$"
PalletTown_ProfessorOaksLab_Text_AsterraMudkip::
    .string "Choose MUDKIP?$"

PalletTown_ProfessorOaksLab_Text_AsterraStarterReceived::
    .string "{PLAYER} received the {STR_VAR_1}!$"
'''

scripts = SCRIPTS.read_text()
start = scripts.index(scene_start)
end = scripts.index(scene_end, start)
scripts = scripts[:start] + new_scene + scripts[end:]
SCRIPTS.write_text(scripts)

text = TEXT.read_text()
if "PalletTown_ProfessorOaksLab_Text_AsterraWelcome::" not in text:
    TEXT.write_text(text + text_add)

print("Asterra native starter selection scene applied.")
