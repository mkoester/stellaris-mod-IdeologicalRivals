# Ideological Rivals

Stellaris mod (game **4.6.x**, Force of Will DLC), private, working title, started 2026-11-24, not
yet run in game. At game start 1–3 AI empires become the player's ideological rivals. They sit far
from the player and from each other, they get fanatic ethics opposed to the player's, and they
steer for the **Force of Will** ambition. If the player takes Force of Will too, the rivals speed
up. Goal (user): it should feel like the player faces one or more real rivals, not only a fallen
empire. Workspace context: `../AGENTS.md`.

Conventions, as in the sibling mods:
- Only `ideological_rivals/` ships; the top level is dev material. Register it with
  `scripts/link-mod.sh stellaris-mod-IdeologicalRivals/ideological_rivals` from the workspace root,
  launcher closed.
- Prefix every key, id, flag and loc key with `irv_` / `irv.`.
- **One vanilla override**, `ap_force_of_will`, in
  `common/ascension_perks/zz_irv_ascension_perks.txt`. It is byte-identical to vanilla 4.6.0 apart from
  the lines marked `IRV:`. After every game update, diff it against vanilla
  (`common/ascension_perks/00_ascension_perks.txt`, the `ap_force_of_will` block).

## Why the override

Vanilla `ap_force_of_will` `possible` requires 3 or more perks, a fanatic ethic, custody of the
empire's own ideology, and an ideology that is **not militarist, xenophobe or authoritarian**. A
rival of an egalitarian, pacifist or xenophile player holds exactly those ethics. Nothing additive
can widen a `possible` block, so the override wraps the three bans in
`if = { limit = { NOT = { has_country_flag = irv_rival } } … }`. It also adds an `ai_weight`
×1000 for rivals. Nothing else in the path bars those ideologies (checked 2026-11-24):
crisis levels, special projects and menace perks contain no such ban, and all eight
`ethic_absolute_*` exist for level 2.
Duplicate keys: `stellaris-modding-insights` doc 09 says that the last definition wins, hence
the `zz_` prefix. That ascension perks follow this rule is **untested**.

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
  75 % of the pops move to the primary ethic, and the authority is repaired (`irv_fix_authority`;
  the rules come from `common/governments/authorities/00_authorities.txt`) with
  `remove_invalid_civics`.
- Candidates exclude gestalts (they cannot be fanatic), Lost Makers (own ideology), Endbringers
  (a crisis already) and the Legendary Leader origins (fixed authority).
- `irv.10` (monthly, rivals only) founds the ideology through vanilla
  `generate_ideology_from_faction_or_ethic`. It waits until the rival knows another empire,
  because vanilla `can_generate_ideology` needs contact. The vanilla effect is itself 3 levels
  deep, so `irv_found_ideology` calls it directly, with no helper in between. Scripted effects stop
  running beyond 5 levels (modding insights doc 07); count the levels before adding one.
- `irv.20` (`on_ascension_perk_picked`): when the player takes Force of Will, every rival gets
  `irv_rival_redoubled` and `irv.10` adds `@irv_willpower_monthly` willpower each month. No
  modifier scales objective rewards: `country_willpower_produces_mult` exists, but nothing
  produces willpower. When a rival takes Force of Will, players in contact get `irv.22`.
- `irv_rival_drive` (+10 % unity) on every rival helps it reach the 3 perks. It also carries an
  opinion of −50 toward the player.

## Known gaps (by design, until test runs say otherwise)

- A rival can take another ambition first (Become the Crisis and others), and `has_ambition` then
  blocks Force of Will. Preventing that would mean overriding the other ambition perks.
- If another empire is custodian of the same ideology and the rival adopts it, the rival
  is not custodian, and the perk stays closed.
- Multiplayer: the rivals oppose the first human player only.

## Test runs

`docs/test-runs.md`: the checklist, results go there.
