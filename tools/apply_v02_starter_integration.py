from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / 'build' / 'pokefirered'


def edit(path, transform):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    new = transform(text)
    if new == text:
        raise SystemExit(f'No change made to {path}; upstream layout may have changed.')
    p.write_text(new, encoding='utf-8')

# Add six Gen II/III early-rival trainers. Gen I keeps FireRed's original trainers.
def patch_opponents(text):
    marker = '#define TRAINER_CUE_BALL_PAXTON                  742\n'
    addition = '''#define TRAINER_CUE_BALL_PAXTON                  742
#define TRAINER_ASTERRA_RIVAL_GEN2_CHIKORITA     743
#define TRAINER_ASTERRA_RIVAL_GEN2_CYNDAQUIL     744
#define TRAINER_ASTERRA_RIVAL_GEN2_TOTODILE      745
#define TRAINER_ASTERRA_RIVAL_GEN3_TREECKO       746
#define TRAINER_ASTERRA_RIVAL_GEN3_TORCHIC       747
#define TRAINER_ASTERRA_RIVAL_GEN3_MUDKIP        748
'''
    text = text.replace(marker, addition, 1)
    text = text.replace('#define NUM_TRAINERS                             743', '#define NUM_TRAINERS                             749', 1)
    return text

# Add one-mon level-5 parties for Nova.
def patch_parties(text):
    marker = 'static const struct TrainerMonNoItemDefaultMoves sParty_RivalOaksLabSquirtle[] = {'
    insert = '''static const struct TrainerMonNoItemDefaultMoves sParty_AsterraRivalGen2Chikorita[] = {
    {.iv = 0, .lvl = 5, .species = SPECIES_TOTODILE},
};
static const struct TrainerMonNoItemDefaultMoves sParty_AsterraRivalGen2Cyndaquil[] = {
    {.iv = 0, .lvl = 5, .species = SPECIES_CHIKORITA},
};
static const struct TrainerMonNoItemDefaultMoves sParty_AsterraRivalGen2Totodile[] = {
    {.iv = 0, .lvl = 5, .species = SPECIES_CYNDAQUIL},
};
static const struct TrainerMonNoItemDefaultMoves sParty_AsterraRivalGen3Treecko[] = {
    {.iv = 0, .lvl = 5, .species = SPECIES_MUDKIP},
};
static const struct TrainerMonNoItemDefaultMoves sParty_AsterraRivalGen3Torchic[] = {
    {.iv = 0, .lvl = 5, .species = SPECIES_TREECKO},
};
static const struct TrainerMonNoItemDefaultMoves sParty_AsterraRivalGen3Mudkip[] = {
    {.iv = 0, .lvl = 5, .species = SPECIES_TORCHIC},
};

'''
    text = text.replace(marker, insert + marker, 1)
    return text

# Add trainer records just before the closing array brace.
def patch_trainers(text):
    marker = '\n};\n'
    records = '''
    [TRAINER_ASTERRA_RIVAL_GEN2_CHIKORITA] = {
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .trainerName = _("NOVA"),
        .items = {}, .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = NO_ITEM_DEFAULT_MOVES(sParty_AsterraRivalGen2Chikorita),
    },
    [TRAINER_ASTERRA_RIVAL_GEN2_CYNDAQUIL] = {
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .trainerName = _("NOVA"),
        .items = {}, .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = NO_ITEM_DEFAULT_MOVES(sParty_AsterraRivalGen2Cyndaquil),
    },
    [TRAINER_ASTERRA_RIVAL_GEN2_TOTODILE] = {
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .trainerName = _("NOVA"),
        .items = {}, .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = NO_ITEM_DEFAULT_MOVES(sParty_AsterraRivalGen2Totodile),
    },
    [TRAINER_ASTERRA_RIVAL_GEN3_TREECKO] = {
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .trainerName = _("NOVA"),
        .items = {}, .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = NO_ITEM_DEFAULT_MOVES(sParty_AsterraRivalGen3Treecko),
    },
    [TRAINER_ASTERRA_RIVAL_GEN3_TORCHIC] = {
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .trainerName = _("NOVA"),
        .items = {}, .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = NO_ITEM_DEFAULT_MOVES(sParty_AsterraRivalGen3Torchic),
    },
    [TRAINER_ASTERRA_RIVAL_GEN3_MUDKIP] = {
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .trainerName = _("NOVA"),
        .items = {}, .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = NO_ITEM_DEFAULT_MOVES(sParty_AsterraRivalGen3Mudkip),
    },
'''
    # trainers.h has one gTrainers array; insert before its final brace.
    idx = text.rfind(marker)
    if idx < 0:
        raise SystemExit('Could not find gTrainers closing brace')
    return text[:idx] + '\n' + records + text[idx:]

# Replace FireRed's starter opening with an Asterra generation + starter selection.
def patch_scripts(text):
    pattern = re.compile(r'PalletTown_ProfessorOaksLab_ChooseStarterScene::.*?\nPalletTown_ProfessorOaksLab_Movement_OakEnter::', re.S)
    replacement = r'''PalletTown_ProfessorOaksLab_ChooseStarterScene::
\tlockall
\ttextcolor NPC_TEXT_COLOR_MALE
\tapplymovement LOCALID_OAKS_LAB_PROF_OAK, PalletTown_ProfessorOaksLab_Movement_OakEnter
\twaitmovement 0
\tremoveobject LOCALID_OAKS_LAB_PROF_OAK
\tsetobjectxyperm LOCALID_OAKS_LAB_PROF_OAK, 6, 3
\tsetobjectmovementtype LOCALID_OAKS_LAB_PROF_OAK, MOVEMENT_TYPE_FACE_DOWN
\tclearflag FLAG_HIDE_OAK_IN_HIS_LAB
\tapplymovement LOCALID_PLAYER, PalletTown_ProfessorOaksLab_Movement_PlayerEnter
\twaitmovement 0
\tclearflag FLAG_DONT_TRANSITION_MUSIC
\tsavebgm MUS_DUMMY
\tfadedefaultbgm
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraWelcomeStarter
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraChooseGeneration
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGeneration
\tend

PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGeneration::
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraGenIQuestion
\tyesnobox 4, 4
\tgoto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGenI
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraGenIIQuestion
\tyesnobox 4, 4
\tgoto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraGenII
\tsetvar VAR_0x4034, 2
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenIII
\tend

PalletTown_ProfessorOaksLab_EventScript_AsterraGenI::
\tsetvar VAR_0x4034, 0
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenI
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraGenII::
\tsetvar VAR_0x4034, 1
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenII
\tend

PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenI::
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraBulbasaurQuestion
\tyesnobox 4, 4
\tgoto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraSetBulbasaur
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraCharmanderQuestion
\tyesnobox 4, 4
\tgoto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraSetCharmander
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraSetSquirtle
\tend

PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenII::
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraChikoritaQuestion
\tyesnobox 4, 4
\tgoto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraSetChikorita
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraCyndaquilQuestion
\tyesnobox 4, 4
\tgoto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraSetCyndaquil
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraSetTotodile
\tend

PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGenIII::
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraTreeckoQuestion
\tyesnobox 4, 4
\tgoto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraSetTreecko
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraTorchicQuestion
\tyesnobox 4, 4
\tgoto_if_eq VAR_RESULT, YES, PalletTown_ProfessorOaksLab_EventScript_AsterraSetTorchic
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraSetMudkip
\tend

PalletTown_ProfessorOaksLab_EventScript_AsterraSetBulbasaur::
\tsetvar PLAYER_STARTER_NUM, 0
\tsetvar PLAYER_STARTER_SPECIES, SPECIES_BULBASAUR
\tsetvar RIVAL_STARTER_SPECIES, SPECIES_CHARMANDER
\tsetvar RIVAL_STARTER_ID, LOCALID_CHARMANDER_BALL
\tsetvar VAR_TEMP_5, LOCALID_BULBASAUR_BALL
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraSetCharmander::
\tsetvar PLAYER_STARTER_NUM, 2
\tsetvar PLAYER_STARTER_SPECIES, SPECIES_CHARMANDER
\tsetvar RIVAL_STARTER_SPECIES, SPECIES_SQUIRTLE
\tsetvar RIVAL_STARTER_ID, LOCALID_SQUIRTLE_BALL
\tsetvar VAR_TEMP_5, LOCALID_CHARMANDER_BALL
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraSetSquirtle::
\tsetvar PLAYER_STARTER_NUM, 1
\tsetvar PLAYER_STARTER_SPECIES, SPECIES_SQUIRTLE
\tsetvar RIVAL_STARTER_SPECIES, SPECIES_BULBASAUR
\tsetvar RIVAL_STARTER_ID, LOCALID_BULBASAUR_BALL
\tsetvar VAR_TEMP_5, LOCALID_SQUIRTLE_BALL
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraSetChikorita::
\tsetvar PLAYER_STARTER_NUM, 0
\tsetvar PLAYER_STARTER_SPECIES, SPECIES_CHIKORITA
\tsetvar RIVAL_STARTER_SPECIES, SPECIES_TOTODILE
\tsetvar RIVAL_STARTER_ID, LOCALID_CHARMANDER_BALL
\tsetvar VAR_TEMP_5, LOCALID_BULBASAUR_BALL
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraSetCyndaquil::
\tsetvar PLAYER_STARTER_NUM, 2
\tsetvar PLAYER_STARTER_SPECIES, SPECIES_CYNDAQUIL
\tsetvar RIVAL_STARTER_SPECIES, SPECIES_CHIKORITA
\tsetvar RIVAL_STARTER_ID, LOCALID_BULBASAUR_BALL
\tsetvar VAR_TEMP_5, LOCALID_CHARMANDER_BALL
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraSetTotodile::
\tsetvar PLAYER_STARTER_NUM, 1
\tsetvar PLAYER_STARTER_SPECIES, SPECIES_TOTODILE
\tsetvar RIVAL_STARTER_SPECIES, SPECIES_CYNDAQUIL
\tsetvar RIVAL_STARTER_ID, LOCALID_SQUIRTLE_BALL
\tsetvar VAR_TEMP_5, LOCALID_SQUIRTLE_BALL
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraSetTreecko::
\tsetvar PLAYER_STARTER_NUM, 0
\tsetvar PLAYER_STARTER_SPECIES, SPECIES_TREECKO
\tsetvar RIVAL_STARTER_SPECIES, SPECIES_MUDKIP
\tsetvar RIVAL_STARTER_ID, LOCALID_CHARMANDER_BALL
\tsetvar VAR_TEMP_5, LOCALID_BULBASAUR_BALL
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraSetTorchic::
\tsetvar PLAYER_STARTER_NUM, 2
\tsetvar PLAYER_STARTER_SPECIES, SPECIES_TORCHIC
\tsetvar RIVAL_STARTER_SPECIES, SPECIES_TREECKO
\tsetvar RIVAL_STARTER_ID, LOCALID_BULBASAUR_BALL
\tsetvar VAR_TEMP_5, LOCALID_CHARMANDER_BALL
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraSetMudkip::
\tsetvar PLAYER_STARTER_NUM, 1
\tsetvar PLAYER_STARTER_SPECIES, SPECIES_MUDKIP
\tsetvar RIVAL_STARTER_SPECIES, SPECIES_TORCHIC
\tsetvar RIVAL_STARTER_ID, LOCALID_SQUIRTLE_BALL
\tsetvar VAR_TEMP_5, LOCALID_SQUIRTLE_BALL
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter
\tend

PalletTown_ProfessorOaksLab_EventScript_AsterraConfirmStarter::
\tshowmonpic PLAYER_STARTER_SPECIES, 10, 3
\tmsgbox PalletTown_ProfessorOaksLab_Text_AsterraConfirmStarter, MSGBOX_YESNO
\tgoto_if_eq VAR_RESULT, NO, PalletTown_ProfessorOaksLab_EventScript_AsterraDeclineStarter
\thidemonpic
\tremoveobject VAR_TEMP_5
\tsetflag FLAG_SYS_POKEMON_GET
\tsetflag FLAG_PALLET_LADY_NOT_BLOCKING_SIGN
\tgivemon PLAYER_STARTER_SPECIES, 5
\tcopyvar VAR_STARTER_MON, PLAYER_STARTER_NUM
\tbufferspeciesname STR_VAR_1, PLAYER_STARTER_SPECIES
\tmessage PalletTown_ProfessorOaksLab_Text_ReceivedMonFromOak
\twaitmessage
\tplayfanfare MUS_OBTAIN_KEY_ITEM
\twaitfanfare
\tmsgbox Text_GiveNicknameToThisMon, MSGBOX_YESNO
\tgoto_if_eq VAR_RESULT, YES, EventScript_GiveNicknameToStarter
\tgoto PalletTown_ProfessorOaksLab_EventScript_RivalPicksStarter
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraDeclineStarter::
\thidemonpic
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraChooseGeneration
\tend

PalletTown_ProfessorOaksLab_Movement_OakEnter::'''
    new, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit('Could not replace FireRed starter scene')

    # Make the opening rival battle use the new Gen II/III trainer parties.
    old = '''\tgoto_if_eq VAR_STARTER_MON, 0, PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleCharmander
\tgoto_if_eq VAR_STARTER_MON, 1, PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleBulbasaur
\tgoto_if_eq VAR_STARTER_MON, 2, PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleSquirtle
\tend'''
    new = '''\tgoto_if_eq VAR_0x4034, 1, PalletTown_ProfessorOaksLab_EventScript_AsterraRivalBattleGenII
\tgoto_if_eq VAR_0x4034, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraRivalBattleGenIII
\tgoto_if_eq VAR_STARTER_MON, 0, PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleCharmander
\tgoto_if_eq VAR_STARTER_MON, 1, PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleBulbasaur
\tgoto_if_eq VAR_STARTER_MON, 2, PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleSquirtle
\tend

PalletTown_ProfessorOaksLab_EventScript_AsterraRivalBattleGenII::
\tgoto_if_eq VAR_STARTER_MON, 0, PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen2Totodile
\tgoto_if_eq VAR_STARTER_MON, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen2Chikorita
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen2Cyndaquil
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraRivalBattleGenIII::
\tgoto_if_eq VAR_STARTER_MON, 0, PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen3Mudkip
\tgoto_if_eq VAR_STARTER_MON, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen3Treecko
\tgoto PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen3Torchic
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen2Totodile::
\tgoto PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleSquirtle
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen2Chikorita::
\tgoto PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleBulbasaur
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen2Cyndaquil::
\tgoto PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleCharmander
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen3Mudkip::
\tgoto PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleSquirtle
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen3Treecko::
\tgoto PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleBulbasaur
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraRivalGen3Torchic::
\tgoto PalletTown_ProfessorOaksLab_EventScript_RivalApproachForBattleCharmander
\tend'''
    if old not in new:
        raise SystemExit('Starter battle branch was not found after scene replacement')
    # Replace the battle calls inside the existing approach endpoints for Gen II/III by
    # branching on the persistent generation variable.
    replacements = {
        'PalletTown_ProfessorOaksLab_EventScript_RivalBattleSquirtle::\n\ttrainerbattle_earlyrival TRAINER_RIVAL_OAKS_LAB_SQUIRTLE': 'PalletTown_ProfessorOaksLab_EventScript_RivalBattleSquirtle::\n\tgoto_if_eq VAR_0x4034, 1, PalletTown_ProfessorOaksLab_EventScript_AsterraBattleTotodile\n\tgoto_if_eq VAR_0x4034, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraBattleMudkip\n\ttrainerbattle_earlyrival TRAINER_RIVAL_OAKS_LAB_SQUIRTLE',
        'PalletTown_ProfessorOaksLab_EventScript_RivalBattleCharmander::\n\ttrainerbattle_earlyrival TRAINER_RIVAL_OAKS_LAB_CHARMANDER': 'PalletTown_ProfessorOaksLab_EventScript_RivalBattleCharmander::\n\tgoto_if_eq VAR_0x4034, 1, PalletTown_ProfessorOaksLab_EventScript_AsterraBattleCyndaquil\n\tgoto_if_eq VAR_0x4034, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraBattleTorchic\n\ttrainerbattle_earlyrival TRAINER_RIVAL_OAKS_LAB_CHARMANDER',
        'PalletTown_ProfessorOaksLab_EventScript_RivalBattleBulbasaur::\n\ttrainerbattle_earlyrival TRAINER_RIVAL_OAKS_LAB_BULBASAUR': 'PalletTown_ProfessorOaksLab_EventScript_RivalBattleBulbasaur::\n\tgoto_if_eq VAR_0x4034, 1, PalletTown_ProfessorOaksLab_EventScript_AsterraBattleChikorita\n\tgoto_if_eq VAR_0x4034, 2, PalletTown_ProfessorOaksLab_EventScript_AsterraBattleTreecko\n\ttrainerbattle_earlyrival TRAINER_RIVAL_OAKS_LAB_BULBASAUR',
    }
    for a,b in replacements.items():
        new = new.replace(a,b,1)
    battle_defs = '''
PalletTown_ProfessorOaksLab_EventScript_AsterraBattleTotodile::
\ttrainerbattle_earlyrival TRAINER_ASTERRA_RIVAL_GEN2_CHIKORITA, RIVAL_BATTLE_TUTORIAL, PalletTown_ProfessorOaksLab_Text_RivalDefeat, Text_RivalVictory
\tgoto PalletTown_ProfessorOaksLab_EventScript_EndRivalBattle
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraBattleCyndaquil::
\ttrainerbattle_earlyrival TRAINER_ASTERRA_RIVAL_GEN2_TOTODILE, RIVAL_BATTLE_TUTORIAL, PalletTown_ProfessorOaksLab_Text_RivalDefeat, Text_RivalVictory
\tgoto PalletTown_ProfessorOaksLab_EventScript_EndRivalBattle
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraBattleChikorita::
\ttrainerbattle_earlyrival TRAINER_ASTERRA_RIVAL_GEN2_CYNDAQUIL, RIVAL_BATTLE_TUTORIAL, PalletTown_ProfessorOaksLab_Text_RivalDefeat, Text_RivalVictory
\tgoto PalletTown_ProfessorOaksLab_EventScript_EndRivalBattle
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraBattleMudkip::
\ttrainerbattle_earlyrival TRAINER_ASTERRA_RIVAL_GEN3_TREECKO, RIVAL_BATTLE_TUTORIAL, PalletTown_ProfessorOaksLab_Text_RivalDefeat, Text_RivalVictory
\tgoto PalletTown_ProfessorOaksLab_EventScript_EndRivalBattle
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraBattleTorchic::
\ttrainerbattle_earlyrival TRAINER_ASTERRA_RIVAL_GEN3_MUDKIP, RIVAL_BATTLE_TUTORIAL, PalletTown_ProfessorOaksLab_Text_RivalDefeat, Text_RivalVictory
\tgoto PalletTown_ProfessorOaksLab_EventScript_EndRivalBattle
\tend
PalletTown_ProfessorOaksLab_EventScript_AsterraBattleTreecko::
\ttrainerbattle_earlyrival TRAINER_ASTERRA_RIVAL_GEN3_TORCHIC, RIVAL_BATTLE_TUTORIAL, PalletTown_ProfessorOaksLab_Text_RivalDefeat, Text_RivalVictory
\tgoto PalletTown_ProfessorOaksLab_EventScript_EndRivalBattle
\tend
'''
    anchor = 'PalletTown_ProfessorOaksLab_EventScript_EndRivalBattle::'
    new = new.replace(anchor, battle_defs + '\n' + anchor, 1)
    return new


def patch_text(text):
    addition = '''
PalletTown_ProfessorOaksLab_Text_AsterraWelcomeStarter::
    .string "PROF. LYRA: Welcome to ASTERRA, {PLAYER}!\\p"
    .string "The Eclipse Cycle has changed what we know\\n"
    .string "about POKéMON.$"
PalletTown_ProfessorOaksLab_Text_AsterraChooseGeneration::
    .string "PROF. LYRA: Choose the generation of\\n"
    .string "your first partner.\\p"
    .string "YES = GENERATION I.$"
PalletTown_ProfessorOaksLab_Text_AsterraGenIQuestion::
    .string "Choose GENERATION I?"$
PalletTown_ProfessorOaksLab_Text_AsterraGenIIQuestion::
    .string "Choose GENERATION II?"$
PalletTown_ProfessorOaksLab_Text_AsterraBulbasaurQuestion::
    .string "Choose BULBASAUR?"$
PalletTown_ProfessorOaksLab_Text_AsterraCharmanderQuestion::
    .string "Choose CHARMANDER?"$
PalletTown_ProfessorOaksLab_Text_AsterraChikoritaQuestion::
    .string "Choose CHIKORITA?"$
PalletTown_ProfessorOaksLab_Text_AsterraCyndaquilQuestion::
    .string "Choose CYNDAQUIL?"$
PalletTown_ProfessorOaksLab_Text_AsterraTreeckoQuestion::
    .string "Choose TREECKO?"$
PalletTown_ProfessorOaksLab_Text_AsterraTorchicQuestion::
    .string "Choose TORCHIC?"$
PalletTown_ProfessorOaksLab_Text_AsterraConfirmStarter::
    .string "Is this your partner?"$
'''
    if 'PalletTown_ProfessorOaksLab_Text_AsterraWelcomeStarter::' in text:
        return text
    return text.rstrip() + '\n' + addition

edit('include/constants/opponents.h', patch_opponents)
edit('src/data/trainer_parties.h', patch_parties)
edit('src/data/trainers.h', patch_trainers)
edit('data/maps/PalletTown_ProfessorOaksLab/scripts.inc', patch_scripts)
edit('data/maps/PalletTown_ProfessorOaksLab/text.inc', patch_text)
print('Asterra v0.2 starter integration applied.')
