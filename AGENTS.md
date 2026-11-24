# Ideological Rivals

Stellaris mod (game **4.6.x**; each ambition needs its DLC: Willpower, Nemesis, Infernals),
private, working title, started 2026-11-24, first test run 2026-11-24. At game start 1–3 AI
empires become the player's ideological rivals. They sit far from the player and from each
other, they get fanatic ethics opposed to the player's, and each pursues an **ambition** that fits
its primary ethic (see "Ambitions"). If the player takes Force of Will too, the rivals speed up.
Goal (user): it should feel like the player faces one or more real rivals, not only a fallen
empire. Workspace context: `../AGENTS.md`.

Conventions, as in the sibling mods:
- Only `ideological_rivals/` ships; the top level is dev material. Register it with
  `scripts/link-mod.sh stellaris-mod-IdeologicalRivals/ideological_rivals` from the workspace root,
  launcher closed.
- Prefix every key, id, flag and loc key with `irv_` / `irv.`.
- **No vanilla override.** Until 2026-11-24 it overrode `ap_force_of_will` to lift its ban on
  militarist, xenophobe and authoritarian ideologies. The user's call: those rivals pursue a fitting
  ambition instead (below). Run A showed that the override did load (`zz_` won); keep that in
  mind if one is ever needed again.

## Ambitions

Vanilla 4.6.0 (`common/ascension_perks/00_ascension_perks.txt`, checked 2026-11-24):
- **Force of Will** bars an ideology that is militarist, xenophobe or authoritarian, and needs 3
  perks, a fanatic ethic and custody of its ideology.
- **Become the Crisis** and **Galactic Hyperthermia** bar xenophiles and pacifists, the exact
  mirror. Their AI weight is 0 unless the empire is militarist, xenophobe or gestalt, and 0 below
  10 % of the galaxy (Become the Crisis), or for a non-infernal empire and after the first taker
  (Hyperthermia). So the AI almost never takes them for a rival by itself.
- **Every ambition but Force of Will** needs `must_not_be_custodian`. **None is reserved for
  authoritarian** ethics.

Hence (the user's decision, 2026-11-24), set in `irv_choose_aim` as a country flag:
- primary militarist → `irv_aim_crisis` (Become the Crisis, needs Nemesis);
- primary xenophobe → `irv_aim_hyperthermia` (needs Infernals);
- any other primary → `irv_aim_fow`.
- **Authoritarian is never a primary**: it opposes an egalitarian player as a secondary ethic only.
- **A primary needs a reachable ambition** (`irv_reachable_<ethic>`): militarist needs Nemesis,
  xenophobe Infernals (neither on Civilian, vanilla `blocks_disruptive_gameplay`), any other
  Willpower with ideologies on. Otherwise that ethic opposes the player as a secondary only, like
  authoritarian. If nothing reachable is left, a random primary (`KIND = fallback`) without an
  ambition: the empire stays a rival only. A descriptor cannot declare a DLC: name them in the
  store text.

`irv_grant_ambition` adds the perk with `add_ascension_perk` once the rival holds 3 perks, is
independent and has no ambition yet. It runs monthly (`irv.10`) and right after each of the rival's
perk picks (`irv.20`), so that a 4th pick cannot be another ambition first. `add_ascension_perk`
skips `possible`, so the Force of Will branch checks vanilla's conditions itself. The perk does
**not** replace a pick (`on_ascension_perk_picked` does not say which perk was picked), so it may be
a bonus perk. Only Force of Will rivals found an ideology. Players in contact get `irv.22`, worded
per ambition.

## How it works

- `irv.1` (`on_game_start_country`, first human player, once via `irv_setup_done`): saves
  `irv_player`/`irv_cap_0` and chooses rivals with `irv_choose_rival = { N = 1..3 }`. The count
  is 1 (tiny, small), 2 (medium, large) or 3 (huge and larger). Each rival is the
  `irv_can_be_rival` candidate with the highest `irv_spread_N`: the **sum** of its distances to the
  player's and the earlier rivals' capitals. A sum, not the minimum: whether `min =` is a floor
  or a cap in script values is unclear (vanilla uses both readings), so check the spread on the
  map.
- Ethics (`irv_shape_rival`): the primary is the fanatic opposite of a player ethic whose axis no
  rival holds yet, taking the player's fanatic ethic first. The secondary is the opposite of
  another player ethic on another axis. If none is left (a gestalt player, or more rivals than
  player axes), a random one is drawn from the free axes. Then `clear_ethos`, `country_add_ethic`,
  75 % of each pop group moves to the primary ethic (`pop_change_ethic` takes percent, 0–100), and the authority is repaired (`irv_fix_authority`;
  the rules come from `common/governments/authorities/00_authorities.txt`) with
  `remove_invalid_civics`.
- Candidates exclude gestalts (they cannot be fanatic), Lost Makers (own ideology), Endbringers
  (a crisis already), Slavers (barred from both crises) and the Legendary Leader origins (fixed
  authority). A random ethic is never one the player holds.
- `irv.10` (monthly, rivals only) founds a Force of Will rival's ideology through vanilla
  `generate_ideology_from_faction_or_ethic`. It waits until the rival knows another empire,
  because vanilla `can_generate_ideology` needs contact. The vanilla effect is itself 3 levels
  deep, so `irv_found_ideology` calls it directly, with no helper in between. Scripted effects stop
  running beyond 5 levels (modding insights doc 07); count the levels before adding one.
- `irv.20` (`on_ascension_perk_picked`): when the player takes Force of Will, every rival gets
  `irv_rival_redoubled` and `irv.10` adds `@irv_willpower_monthly` willpower each month to the
  rivals on Force of Will. No modifier scales objective rewards: `country_willpower_produces_mult`
  exists, but nothing produces willpower. For a rival, `irv.20` runs the ambition grant.
- `irv_rival_drive` (+10 % unity) on every rival helps it reach the 3 perks. It also carries an
  opinion of −50 toward the player.

## Known gaps (by design, until test runs say otherwise)

- The grant runs right after each pick, so a crisis rival gets its ambition the moment it holds 3
  perks, before its AI could pick another. A Force of Will rival also needs to be custodian: one
  with no contact yet has no ideology, and its 4th pick can be Cosmogenesis or Behemoths. Undo if
  seen: `remove_ascension_perk` + `cancel_crisis` (both in `effects.log`), but the other
  ambition's `on_enabled` has already run.
- A crisis rival's AI can still found an ideology by itself (vanilla yearly roll, fanatic
  faction). Vanilla would then bar the crisis; `add_ascension_perk` grants it anyway. Untested
  whether the crisis path minds.
- Hyperthermia for a non-infernal rival: vanilla lets any empire with the DLC take it, but its
  AI never does. Whether a non-infernal AI plays the path sensibly is untested.
- If another empire is custodian of the same ideology and a Force of Will rival adopts it, the
  rival is not custodian, and the grant waits. AI adoption is a yearly roll
  (`forceofwill.1112`, only while the empire has no ideology). A rival founds its own within a
  month of first contact (`irv.10`), so the window is that month.
- Multiplayer: the rivals oppose the first human player only.

## Static check

From the workspace root:
`scripts/cwtools_check.py stellaris-mod-IdeologicalRivals/ideological_rivals --game-dir <game> --rules ~/Projects/clones/cwtools-stellaris-config/config`.
0 findings on 2026-11-24 (after the ambitions rework), with a broken control file reported. The ignored rule gaps are the
4.6 ideology code and the `irv_primary_$OPP$` flags, which CWTools cannot expand.

## Test runs

`docs/test-runs.md`: the checklist, results go there.
