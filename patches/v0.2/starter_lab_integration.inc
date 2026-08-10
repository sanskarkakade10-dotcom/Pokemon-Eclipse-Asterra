@ Pokémon Eclipse / Asterra v0.2 — starter lab integration candidate
@ Target: pret/pokefirered revision c75f352304d529f6ba92d4f74b9cf8b5c3810788
@
@ This is the native FireRed script layer to be applied to
@ data/maps/PalletTown_ProfessorOaksLab/scripts.inc once the complete
@ source checkout is available to the build job.
@
@ The implementation intentionally branches to concrete species/trainer
@ scripts. This keeps the ROM-side logic simple and compatible with the
@ existing Gen III script VM.

.equ ASTERRA_STARTER_GEN, VAR_TEMP_1
.equ ASTERRA_STARTER_CHOICE, VAR_TEMP_2
.equ ASTERRA_PLAYER_SPECIES, VAR_TEMP_3
.equ ASTERRA_NOVA_SPECIES, VAR_TEMP_4

@ ---------------------------------------------------------------------------
@ Generation selection
@ ---------------------------------------------------------------------------
Asterra_ChooseGeneration::
	multichoice 1, 1, MULTI_ASTERRA_GENERATION, FALSE
	switch VAR_RESULT
	case 0, Asterra_SelectGenI
	case 1, Asterra_SelectGenII
	case 2, Asterra_SelectGenIII
	goto Asterra_ChooseGeneration

Asterra_SelectGenI::
	setvar ASTERRA_STARTER_GEN, 0
	goto Asterra_ChooseStarter

Asterra_SelectGenII::
	setvar ASTERRA_STARTER_GEN, 1
	goto Asterra_ChooseStarter

Asterra_SelectGenIII::
	setvar ASTERRA_STARTER_GEN, 2
	goto Asterra_ChooseStarter

@ ---------------------------------------------------------------------------
@ Starter selection
@ ---------------------------------------------------------------------------
Asterra_ChooseStarter::
	multichoice 1, 1, MULTI_ASTERRA_STARTERS, FALSE
	copyvar ASTERRA_STARTER_CHOICE, VAR_RESULT
	goto_if_eq ASTERRA_STARTER_GEN, 0, Asterra_ChooseGenIStarter
	goto_if_eq ASTERRA_STARTER_GEN, 1, Asterra_ChooseGenIIStarter
	goto_if_eq ASTERRA_STARTER_GEN, 2, Asterra_ChooseGenIIIStarter
	goto Asterra_ChooseGeneration

Asterra_ChooseGenIStarter::
	goto_if_eq ASTERRA_STARTER_CHOICE, 0, Asterra_GiveBulbasaur
	goto_if_eq ASTERRA_STARTER_CHOICE, 1, Asterra_GiveCharmander
	goto_if_eq ASTERRA_STARTER_CHOICE, 2, Asterra_GiveSquirtle
	goto Asterra_ChooseStarter

Asterra_ChooseGenIIStarter::
	goto_if_eq ASTERRA_STARTER_CHOICE, 0, Asterra_GiveChikorita
	goto_if_eq ASTERRA_STARTER_CHOICE, 1, Asterra_GiveCyndaquil
	goto_if_eq ASTERRA_STARTER_CHOICE, 2, Asterra_GiveTotodile
	goto Asterra_ChooseStarter

Asterra_ChooseGenIIIStarter::
	goto_if_eq ASTERRA_STARTER_CHOICE, 0, Asterra_GiveTreecko
	goto_if_eq ASTERRA_STARTER_CHOICE, 1, Asterra_GiveTorchic
	goto_if_eq ASTERRA_STARTER_CHOICE, 2, Asterra_GiveMudkip
	goto Asterra_ChooseStarter

@ ---------------------------------------------------------------------------
@ Concrete party insertion. Level 5 matches the original FireRed opening.
@ ---------------------------------------------------------------------------
Asterra_GiveBulbasaur::
	givemon SPECIES_BULBASAUR, 5
	setvar ASTERRA_PLAYER_SPECIES, SPECIES_BULBASAUR
	goto Asterra_StarterReceived

Asterra_GiveCharmander::
	givemon SPECIES_CHARMANDER, 5
	setvar ASTERRA_PLAYER_SPECIES, SPECIES_CHARMANDER
	goto Asterra_StarterReceived

Asterra_GiveSquirtle::
	givemon SPECIES_SQUIRTLE, 5
	setvar ASTERRA_PLAYER_SPECIES, SPECIES_SQUIRTLE
	goto Asterra_StarterReceived

Asterra_GiveChikorita::
	givemon SPECIES_CHIKORITA, 5
	setvar ASTERRA_PLAYER_SPECIES, SPECIES_CHIKORITA
	goto Asterra_StarterReceived

Asterra_GiveCyndaquil::
	givemon SPECIES_CYNDAQUIL, 5
	setvar ASTERRA_PLAYER_SPECIES, SPECIES_CYNDAQUIL
	goto Asterra_StarterReceived

Asterra_GiveTotodile::
	givemon SPECIES_TOTODILE, 5
	setvar ASTERRA_PLAYER_SPECIES, SPECIES_TOTODILE
	goto Asterra_StarterReceived

Asterra_GiveTreecko::
	givemon SPECIES_TREECKO, 5
	setvar ASTERRA_PLAYER_SPECIES, SPECIES_TREECKO
	goto Asterra_StarterReceived

Asterra_GiveTorchic::
	givemon SPECIES_TORCHIC, 5
	setvar ASTERRA_PLAYER_SPECIES, SPECIES_TORCHIC
	goto Asterra_StarterReceived

Asterra_GiveMudkip::
	givemon SPECIES_MUDKIP, 5
	setvar ASTERRA_PLAYER_SPECIES, SPECIES_MUDKIP
	goto Asterra_StarterReceived

Asterra_StarterReceived::
	setflag FLAG_GOT_STARTER
	msgbox Asterra_Text_StarterReceived
	@ Nova's battle is wired after the menu/party insertion is verified.
	end

@ ---------------------------------------------------------------------------
@ Text labels to add to data/text/PalletTown_ProfessorOaksLab.inc
@ ---------------------------------------------------------------------------
Asterra_Text_StarterReceived::
	.string "Your new partner joins your journey!$"
