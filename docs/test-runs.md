# Test runs

Throwaway games on Linux, mod linked with `scripts/link-mod.sh`. DevTools for shortcuts. After
each run, check `error.log` for `irv` lines.

## Checklist

1. **Loads**: `error.log` has no `irv` lines. Without this, nothing else counts.
2. **Huge galaxy**, egalitarian/xenophile/pacifist player: `event irv.900` lists 3 rivals:
   fanatic xenophobe (`aim_hyperthermia`), fanatic militarist (`aim_crisis`), and fanatic
   spiritualist or materialist (`aim_fow`), each with authoritarian as secondary. No rival is
   fanatic authoritarian. `event irv.903`: the rivals have the highest spread among the candidates
   (see run A). Their governments are valid (no egalitarian dictatorship, no empty civic slots
   left unfilled for long).
3. **Small galaxy**: exactly 1 rival. (Medium and large: 2.)
4. **Gestalt player**: rivals still chosen, random ethics on distinct axes, none authoritarian as
   primary.
5. **Ideology**: after the first contact, only the Force of Will rival founds an ideology of its
   primary ethic and is its custodian (`irv.900`: "has an ideology"). The crisis rivals found none
   (watch a few years: vanilla's own yearly roll may still found one).
6. **Ambitions granted**: `event irv.902` (3 perks per rival). By the next month `irv.900` shows
   "has Become the Crisis", "has Galactic Hyperthermia" and "has Force of Will", `game.log` shows
   `IRV ambition granted`, and each path is in the rival's Situation Log (`play <id>`). Also check
   whether the perk used a slot (perk screen, `play <id>`).
7. **Speed-up**: give the player Force of Will. `irv.21` appears, rivals carry
   `irv_rival_redoubled`, and the Force of Will rival's willpower rises by 25 a month on top of its
   objectives (top bar via `play <id>`). If it does not move, `add_resource` does not reach crisis
   currency. The documented lever is then `complete_crisis_objective = <a Force of Will objective>`
   (vanilla uses it for other paths, e.g. `crisobj_purge_pops`). The recurring
   `crisobj_have_vassals_forceofwill` pays 10–50 depending on the number of empires.
8. **Announcement**: each grant to a rival in contact gives the player `irv.22`, with the text for
   its ambition.
9. **Crisis paths run**: after a few years with `fast_forward`, the crisis rivals gain menace and
   heat (their level in the Situation Log), and nothing in `error.log` names the paths.
10. **Missing DLC** (a game with Nemesis or Infernals disabled in the launcher's DLC list): no
    rival gets that crisis's ethic as its primary; it appears as a secondary at most.
11. **4.6.1 changes** (watch these in the natural-pace run, which runs on 4.6.1). Nothing in the
    mod depends on them, but they change how the rival's path plays out:
    - The Force of Will rival's Ideological Reach: modifiers now apply before the Reach
      calculation, so inflated Reach drops. Check that its ideology still spreads, and record
      its strength over the decades.
    - Unification, the last Force of Will level: each fallen empire opposed to the ideology now
      declares one war on all its followers, and the followers join as defenders. Check who
      ends up in those wars (the player, if they adopted the rival's ideology).
    - The ambition victory now counts only the Force of Will empire's own wars.

## Results

**Run A (2026-11-24, 4.6, small galaxy, Machine Intelligence player, save
`yorphianextractorate_888024433/2200.01.01_irv-a-start.sav`):**
- Item 1, passed: `error.log` has no `irv` line. The override replaces vanilla:
  `Object with key: ap_force_of_will already exists, using the one at file:
  common/ascension_perks/zz_irv_ascension_perks.txt`. So for ascension perks, the last definition
  wins, as doc 09 says.
- Item 3, passed: exactly 1 rival.
- Item 4, passed: fanatic egalitarian + pacifist (two different axes), democratic, Memory Vault +
  Byzantine Bureaucracy, Life-Seeded.
- **Spread, failed:** the rival was not the farthest candidate. Distances to the player's capital
  in map units, measured in the save: country 8 (a valid candidate, default origin): 405 in a
  straight line, 528 by hyperlane. The rival: 372 and 456. Two gestalts (not candidates) sit in
  between. `irv.903` logs each empire's `irv_spread_1` next to both explicit measures; run it at
  the start of run B.
- `irv.900`'s flag lines end in a stray `$` (`IRV  primary_egalitarian$`): cosmetic.

**Run B (2026-11-24, 4.6, huge galaxy, Ensign, UNE-style player egalitarian/xenophile/pacifist,
saves `unitednationsofearth3_769114477/2200.01.01_irv-b-0.sav`, `autosave_2200.02.01.sav`; the
mod as of the ambitions rework, before the DLC handling):**
- Item 2, ethics passed: rival 1 fanatic xenophobe + authoritarian (`aim_hyperthermia`),
  rival 2 fanatic militarist + authoritarian (`aim_crisis`), rival 3 fanatic materialist +
  authoritarian (`aim_fow`). No fanatic authoritarian.
- Item 2, spread: `distance` without `type` is **hyperlane** distance (`irv.903`: spread = lanes
  for every empire). Rival 1 (Breannan Voyagers, 1167) has the highest spread of all empires.
  Run A's miss is still unexplained.
- Item 2, governments, **failed twice**:
  - Rival 1 has the Forever Cruise origin, which forbids xenophobe ethics. `change_government`
    failed ("Required ethic [ethic_fanatic_xenophobe] is excluded", "Result origin
    [origin_forever_cruise] is not valid"), and the empire keeps an origin its ethics forbid.
    Fix: candidates exclude every origin whose `possible` names an ethic, and every
    non-playable (scripted) origin.
  - Rival 3 (Lost Colony) had **no civic** left after `remove_invalid_civics`, still on
    2200.02.01. Fix: `civics = random` when civic points are unused (vanilla's rebels do the same).
- Item 5, passed: by 2200.02.01 the only ideology in the galaxy is rival 3's (materialist, origin
  and custodian 28). The crisis rivals founded none.
- Script errors (`error.log`): a scripted trigger called with a parameter its body does not use
  fails to compile ("Compiling source for … failed for missing args: E"). `[This.GetName]` in a
  scripted effect is an "Invalid macro entry": a scripted effect reads `[ ]` as its parameter
  syntax. Fixed: reachability is read once into global flags, and names are logged from events only.
- `game.log` **drops a line identical to an earlier one**: `irv.900` printed "IRV rival:
  Unidentified Empire" once for 3 rivals, and `secondary_authoritarian` once. Every log line now
  names its rival (number, or capital in events).


**Run C (2026-11-24, 4.6, huge galaxy, Ensign, player egalitarian/xenophile/pacifist, all
three DLCs; the mod with regular-empires-only candidates and the civic refill; saves
`unitednationsofearth4_-337465913/2200.01.01_irv-b-0.sav`, `autosave_2200.02.01.sav`, screenshots
`~/Pictures/Screenshots/screenshot_2026-11-24_21-15-24`, `21-15-38`, `21-16-04`):**
- Item 1, passed: no `irv` line in `error.log`, no `change_government` failure.
- Item 2, passed: Authority of Ba Grax (capital Backatta, fanatic xenophobe + authoritarian,
  `aim_hyperthermia`), United Spuxulac Authority (Greater Spuxulac, fanatic militarist +
  authoritarian, `aim_crisis`), Falleran Star Dynasty (Cradle of Decay, fanatic materialist +
  authoritarian, `aim_fow`). All dictatorial with two civics, regular origins. Rival 1 has the
  highest spread among the candidates (1146); the only empire above it, Bothria (1167), is a hive
  mind.
- Item 5, passed: on 2200.02.01 only rival 3 has an ideology, and it is its custodian.
- Seen, not a mod bug: rivals 1 and 2 got rulers with the same name (Executor Kul-Pox, two leaders
  of two species from one name list), both new from `change_government` in the same tick.
- Open: the diplomacy screen shows a "?" icon beside Ba Grax's government; Spuxulac, with the
  same government type and authority in the save, shows the dictatorial icon.
- `irv.900`'s flag lines read `rival1$:primary_xenophobe$`: cosmetic.
- Item 6, passed (2200.06.01, `irv.902`; autosave 2200.08.01): Ba Grax got Galactic Hyperthermia,
  Spuxulac Become the Crisis, Falleran Force of Will, each beside its three test perks, each with
  a `crisis_progression`. **The grant came at once**, inside `irv.902`: `add_ascension_perk` fires
  `on_ascension_perk_picked`, so `irv.20` ran it. Ba Grax's views (`play`, screenshots
  `21-37-03`, `21-37-12`, `21-37-32`): Ambition tab Hyperthermia level 1 "Concern" with its
  objectives; the four perks fill 4 of 8 perk slots, the other 4 locked, with no tradition adopted.
- The two crisis rivals had founded ideologies through `devtools.21` (a test shortcut), so they
  are custodians, which vanilla's `possible` would refuse. The grant gave them the crisis anyway;
  Ba Grax keeps its ideology (Backattan Nativism, faction, momentum) beside Hyperthermia. Nothing
  in `error.log`.
- Item 8, passed: three `irv.22` popups, one per rival, each with its ambition's text (screenshot
  `21-35-33`).
- Item 7, passed (saves `2200.08.01_irv-b-4.sav`, `autosave_2200.09.01.sav`, screenshots
  `21-39-48`, `21-40-17`): `activate_ascension_perk ap_force_of_will` for the player fires
  `on_ascension_perk_picked` too; `irv.21` appeared, all three rivals carry `irv_rival_redoubled`,
  and the Force of Will rival's willpower went 0 → 25 in the month (no objective paid). The
  crisis rivals get the marker but no currency, as designed. Vanilla's own Force of Will texts
  read "the pacifist values of , …": the player holds no ideology (console perk), a vanilla gap.
- Item 9, **runs, but the crisis paths stall** (`fast_forward 1800`, save `2205.10.01.sav`; nothing
  in `error.log`):
  - Force of Will (Falleran): willpower 1025 → 2568 in 60 months, of which 1500 is the mod's
    +25/month and ~43 its own objectives. Level 2 holds; level 3 needs its next project.
  - Become the Crisis (Spuxulac): level 1, **0 menace** in five years. Menace comes from its
    objectives (wars, conquest, destruction); a rival at peace earns none. Vanilla's AI takes this
    path only with 10 % of the galaxy (`ai_weight`).
  - Galactic Hyperthermia (Ba Grax): **no level yet**. Level 1 needs the special project
    `INF_CRISIS_ENTROPY`, **25000 physics** (`common/special_projects/00_projects_infernals.txt`); Ba
    Grax has it open. An early AI needs decades for it.
  - Granted at 2200 by the test shortcut, the paths had no economy behind them; a natural grant
    comes with the third perk (decades later). Whether they then move is the open question: see
    "Design questions" in `AGENTS.md`.
