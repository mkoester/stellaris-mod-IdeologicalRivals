# Ideological Rivals

A Stellaris mod (game **4.6.x**). In development. Each ambition needs its DLC: Force of Will
needs **Willpower**, Become the Crisis **Nemesis**, Galactic Hyperthermia the **Infernals** species
pack. A rival only gets ethics whose ambition your game offers; with none of the three, rivals
pursue no ambition.

At the start of a game, one to three AI empires become your **ideological rivals**: one in a
small galaxy, two in a medium or large one, three in a huge one. They start far away from you
and from each other. They hold fanatic ethics opposed to yours, and each pursues an ambition that fits:
a militarist rival **Become the Crisis**, a xenophobe one **Galactic Hyperthermia**, any other
**Force of Will**. It gets its ambition as soon as it holds three ascension perks. If you take
Force of Will yourself, your rivals redouble their efforts.

Overrides nothing from vanilla. Add it at game start; it does nothing in a running campaign.

## Layout

- `ideological_rivals/`: the mod (only this folder ships).
  - `common/scripted_effects/irv_effects.txt`: choosing and shaping rivals, their ambition,
    founding their ideology.
  - `common/on_actions/irv_on_actions.txt`: `on_game_start_country`, `on_monthly_pulse_country`,
    `on_ascension_perk_picked`.
  - `events/irv_events.txt`: `irv.1` setup, `irv.10` monthly, `irv.20` perk picked, and the
    console helpers `irv.900` (list the rivals in `game.log`), `irv.901` (rerun the setup),
    `irv.902` (3 perks per rival) and `irv.903` (spread scores and distances in `game.log`).

Unofficial fan project, not affiliated with Paradox Interactive. Stellaris and its game data are
Paradox's.
