# Ideological Rivals

A Stellaris mod (game **4.6.x**, needs the Force of Will DLC). In development, not yet tested.

At the start of a game, one to three AI empires become your **ideological rivals**: one in a
small galaxy, two in a medium or large one, three in a huge one. They start far away from you
and from each other. They hold fanatic ethics opposed to yours, and they aim for the **Force of
Will** ambition. The mod lets them take that ambition even with an authoritarian, militarist or
xenophobe ideology. If you take Force of Will yourself, your rivals redouble their efforts.

Overrides one vanilla object: the ascension perk `ap_force_of_will`. Conflicts with any mod that
overrides the same perk. Add it at game start; it does nothing in a running campaign.

## Layout

- `ideological_rivals/`: the mod (only this folder ships).
  - `common/ascension_perks/zz_irv_ascension_perks.txt`: the override (changes marked `IRV:`).
  - `common/scripted_effects/irv_effects.txt`: choosing and shaping rivals, founding their ideology.
  - `common/on_actions/irv_on_actions.txt`: `on_game_start_country`, `on_monthly_pulse_country`,
    `on_ascension_perk_picked`.
  - `events/irv_events.txt`: `irv.1` setup, `irv.10` monthly, `irv.20` perk picked, and the
    console helpers `irv.900` (list the rivals in `game.log`) and `irv.901` (rerun the setup).

Unofficial fan project, not affiliated with Paradox Interactive. Stellaris and its game data are
Paradox's.
