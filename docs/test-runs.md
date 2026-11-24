# Test runs

Throwaway games on Linux, mod linked with `scripts/link-mod.sh`. DevTools for shortcuts. After
each run, check `error.log` for `irv_` lines and for errors about `zz_irv_ascension_perks.txt`.

## Checklist

1. **Loads**: `error.log` has no `irv` lines, and the perk override gives no "duplicate"
   error. Without this, nothing else counts.
2. **Huge galaxy**, egalitarian/xenophile/pacifist player: `event irv.900` lists 3 rivals with
   primaries authoritarian, xenophobe and militarist. On the map, the rivals are far apart and
   carry those fanatic ethics. Their governments are valid (no egalitarian dictatorship, no empty
   civic slots left unfilled for long).
3. **Small galaxy**: exactly 1 rival.
4. **Gestalt player**: rivals still chosen, random ethics on distinct axes.
5. **Ideology**: after the first contact, the rival founds an ideology of its primary ethic and is
   its custodian (`irv.900`: "has an ideology").
6. **Ban lifted**: give a rival 3 perks (`play <id>`, console), then open the perk list. Force of
   Will is offered despite the authoritarian ideology, and the AI takes it. **Control**: a
   non-rival authoritarian custodian is still refused. If the rival is refused as well, the
   override lost the load order (`zz_` → try `!!_`).
7. **Speed-up**: give the player Force of Will. `irv.21` appears, rivals carry
   `irv_rival_redoubled`, and a rival's willpower rises by 25 a month on top of its objectives (top
   bar via `play <id>`). If it does not move, `add_resource` does not reach crisis currency: find
   another lever.
8. **Announcement**: a rival in contact takes Force of Will, and the player gets `irv.22`.

## Results

None yet.
