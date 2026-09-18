# Design: Reroll Points + Class Slots for RandomRace

Date: 2026-09-06
Status: Approved (user: "okeoke yes i accept")

## Goal

Give each player two separate **reroll currencies** — **race rerolls** and **class
rerolls** — plus a per-player **class slot cap** (max number of classes). Only
admins can grant points or change slots. Players spend their points to re-roll
their race/classes, and are reminded of any spare points on join and after each
claim/reroll.

## Current behavior (before this change)

- `/claimrace`: free one-time spin; blocked once `RaceManager.getRace(player) != null`.
- `/claimclass`: rolls `classes-count` (default 3) groups the player doesn't have yet;
  blocked once they have `classes-count` classes.
- `/randomrace reroll <p>` / `rerollclass <p>` are free admin powers that clear +
  re-spin, and they wipe the player's whole `playerdata.yml` record.
- `PlayerDataManager` stores per-UUID: `claimed` timestamp, `race` key, `classes` list,
  `name`. `clear(UUID)` deletes the entire node.

## New concepts

- **Race rerolls** (int, default 0) — spend 1 to re-roll the race.
- **Class rerolls** (int, default 0) — spend 1 to re-roll all classes.
- **Class slots** (int, default -1 = not customized, falls back to config
  `classes-count`) — the max number of classes a player may hold. Admin-set to 1-10.

## Design decisions (user-confirmed)

1. **Spend mechanism = "Both"**: `/claimrace` / `/claimclass` automatically become
   rerolls once a player is already claimed/full (burning a point), AND dedicated
   `/rerollrace` / `/rerollclass` commands exist.
2. **Slots filling = "Both"**: `/claimclass` fills missing slots **free** up to the
   cap; only a full re-roll (all slots filled) burns a class reroll point.
3. **Join reminder = "Both"**: first join shows an intro (claim instructions); any
   join with spare rerolls shows a reminder listing them.
4. **New player defaults**: 0 race rerolls, 0 class rerolls, slot cap = config
   default (3). Free first claims regardless.
5. **Admin controls**: `/randomrace give` (add), `set` (absolute), `setslots`,
   `check`.
6. **Also show rerolls/slots in `/valracestats`** output (accepted as part of the
   design).

## Architecture (Approach A)

```
RandomRacePlugin
 ├── PlayerDataManager      (storage: playerdata.yml + offline resolve)
 ├── RerollService          (rules: spend, slots, gauges — single owner)
 ├── ClaimRaceCommand       (free claim OR spend race reroll)
 ├── ClaimClassCommand      (free fill OR spend class reroll)
 ├── RerollRaceCommand      (NEW: spend race reroll + spin)
 ├── RerollClassCommand     (NEW: spend class reroll + spin)
 ├── PlayerJoinListener     (NEW: intro + reminders)
 ├── RandomRaceAdminCommand (adds give/set/setclassslots/check)
 ├── ValhallaStatsCommand   (adds reroll/slot line)
 ├── SpinAnimation          (unchanged)
 ├── ClassSpinAnimation     (unchanged)
 └── MessageUtil            (adds {plural} helper if needed)
```

## 1. PlayerDataManager

Record keys per UUID:
- `race-rerolls` (int, default 0)
- `class-rerolls` (int, default 0)
- `class-slots` (int, default -1 → config `classes-count`)
- `joined` (long timestamp, first-seen join; also `hasRecord` for first-join detect)

New methods:
- `getRaceRerolls(UUID)` / `addRaceRerolls(UUID, int)` / `setRaceRerolls(UUID, int)`
- `getClassRerolls(UUID)` / `addClassRerolls(UUID, int)` / `setClassRerolls(UUID, int)`
- `getClassSlots(UUID)` / `setClassSlots(UUID, int)`
- `hasRecord(UUID)` / `markJoined(UUID)`
- `clearClaim(UUID)` — removes `claimed`/`race`/`classes` but **keeps** rerolls,
  slots, `name`, `joined`. Replaces the destructive `clear`.
- Add a constructor `PlayerDataManager(File file)` (test-friendly, no plugin
  required). Keep the plugin constructor delegating to it (plugin version still
  saves the default `playerdata.yml` resource on first boot).

`getRaceRerolls` and `getClassRerolls` lazily default missing keys to 0 so old
records and admin-created records behave identically.

## 2. RerollService

Single owner of the rules. Constructors:
- `RerollService(PlayerDataManager, int defaultClassSlots)` — testable.
- `RerollService(RandomRacePlugin plugin)` — convenience, reads
  `config.classes-count` for the default.

Methods:
- `boolean trySpendRaceReroll(UUID)` — if `race-rerolls > 0`: decrement, save,
  return true; else false.
- `boolean trySpendClassReroll(UUID)` — same for class rerolls.
- `int raceRerolls(UUID)` / `int classRerolls(UUID)`
- `boolean hasAnyRerolls(UUID)` — raceRerolls > 0 || classRerolls > 0.
- `int classSlots(UUID)` — `getClassSlots()` or `defaultClassSlots` when -1.
- `void addRaceRerolls(UUID,int)` / `setRaceRerolls(UUID,int)` /
  `addClassRerolls(UUID,int)` / `setClassRerolls(UUID,int)` /
  `setClassSlots(UUID,int)` — thin, clamp to >= 0 (slots clamp 1-10).

Delegates (thin, live-query ValhallaRaces like the current commands do):
- `boolean isRaceClaimed(Player)` → `RaceManager.getRace(p) != null`
- `boolean areClassesFull(Player)` → current class count >= `classSlots(uuid)`

## 3. Player commands

### /claimrace
1. Permission `randomrace.claim` (unchanged).
2. If not claimed → free spin (existing path).
3. If claimed → reroll branch:
   - `trySpendRaceReroll(uuid)` false → deny with
     `messages.reroll-race-no-points` + show remaining (0).
   - true → send `messages.reroll-race-spin`, spin a new race
     (fresh winner, `SpinAnimation`). Point is consumed before the spin.

### /claimclass
1. Permission `randomrace.class` (unchanged).
2. `cap = service.classSlots(uuid)`.
3. If current class count < cap → free fill of missing groups (existing
   `pickRandomGroups` with `skip` = existing group keys, target `cap`).
4. Else (at/over cap) → reroll branch:
   - `trySpendClassReroll(uuid)` false → deny
     `messages.reroll-class-no-points` + remaining.
   - true → clear all classes (ValhallaRaces), re-pick `cap` groups fresh, spin
     (`ClassSpinAnimation`). Point consumed before the spin.

### /rerollrace (new, pipe through same logic as claim-race reroll branch)
1. `trySpendRaceReroll` false → deny; true → spin new race.

### /rerollclass (new, same as claim-class reroll branch)
1. `trySpendClassReroll` false → deny; true → clear, re-pick `cap` groups, spin.

### Rerolls-left line (all four paths)
After the spin completes, append one line built from
`messages.rerolls-left`: replaces `{rrace}`, `{cclass}`,
`{race_plural}` ("s"/""), `{class_plural}`. Both counts are always shown.

## 4. Join reminders — PlayerJoinListener

- On join, delayed ~20 ticks (world may not be loaded in the event):
  - `first = !playerDataManager.hasRecord(uuid)` (before marking).
  - `markJoined(uuid)` always.
  - If `first` → send `messages.first-join` intro (welcome + claim instructions).
  - If `service.hasAnyRerolls(uuid)` → send `messages.reroll-reminder`
    with counts + how to use (list `/rerollrace`, `/rerollclass`).

## 5. RandomRaceAdminCommand additions

Subcommands (all offline-capable via `resolveOffline` → fallback
`Bukkit.getOfflinePlayer(name).getUniqueId()`):
- `give <player> <race|class> <n>` — `addRaceRerolls` / `addClassRerolls` (n >= 1).
- `set <player> <race|class> <n>` — absolute, clamped >= 0.
- `setslots <player> <n>` — `setClassSlots` (1-10). Lowering does **not** strip
  existing classes; the next class re-roll shrinks to the new cap. Admin reply notes
  this when lowering below current count.
- `check <player>` — race, classes (count/cap), race rerolls, class rerolls.

Changes to existing behavior:
- `reset` and `reroll` call `clearClaim` instead of `clear` so granted points and
  slots survive.
- `rerollclass` likewise uses `clearClaim` path (no point loss).
- Admin `reroll` / `rerollclass` remain **free** (no player points consumed) —
  they are admin powers; only the player-facing commands burn points.
- Extended tab completion for the new subcommands (player name, then
  `race|class`, then number).

## 6. ValhallaStatsCommand

Detail output gains a line: `Rerolls: {rrace} race / {cclass} class | Slots: {n}`
using stored values (offline-safe, reads `playerdata.yml`).

## 7. Config + plugin.yml

Config `messages` additions:
- `first-join` (`{player}`)
- `reroll-reminder` (`{rrace}`, `{cclass}`, `{race_plural}`, `{class_plural}`)
- `reroll-race-no-points`
- `reroll-class-no-points`
- `reroll-race-spin`
- `reroll-class-spin`
- `rerolls-left` (shown after every claim/reroll)

`plugin.yml`:
- new commands `rerollrace` (permission `randomrace.claim`) and `rerollclass`
  (permission `randomrace.class`)
- version bumped to `1.2.0` in both `plugin.yml` and `pom.xml`.

## 8. Error handling

- Missing/old records: all reads default (0 points, -1 slots, not joined).
- Negative admin inputs: `give` requires 1+, `set` clamps 0+, `setslots` clamps
  1-10, replies with usage on bad input.
- Offline target with no record: `give`/`set`/`setslots` create the record
  (offline-mode UUID = name-hash, consistent with what they get on join).
- Mid-spin GUI close forfeits the already-spent point (documented in
  config.yml comments).

## 9. Testing

- `PlayerDataManagerTest` (uses the `File` constructor + temp dir):
  defaults, add/set/get, setslots, `clearClaim` preserves points/slots/joined,
  `markJoined`/`hasRecord`, offline `resolveOffline`.
- `RerollServiceTest` (fake `PlayerDataManager` on a temp file):
  spend with 0 → false; spend with points → true + decremented; slot fallback to
  default; setClassSlots clamps; `hasAnyRerolls`.
- Existing tests keep passing. Verify with `mvn test`, then `mvn package`.

## Out of scope

- No GUI for spending points (chat commands only).
- No per-race or per-class point costs.
- No automatic point grants (except future config values; defaults are 0).
- No wipe command (`set` to 0 covers it).