# Offline Reroll Points — Design Spec

**Date:** 2026-09-06
**Status:** Approved (design section), pending spec review

## Problem

Reroll-points admin commands (`give`, `set`, `setslots`, `check`) are advertised as
offline-capable, but a player who has **never joined** the server has no entry in
`playerdata.yml`, so `uuidFor()` falls back to `Bukkit.getOfflinePlayer(name)` — a
synthetic `OfflinePlayer:<name>` UUID (`UUID.nameUUIDFromBytes("OfflinePlayer:<name>")`).

That synthetic UUID is **not** the player's real account UUID. Rerolls/slots granted
before a player's first login are stored under the phantom key and become invisible to
the player: on their first login the real-UUID record starts empty, so `hasAnyRerolls`
returns false, no reminder fires, and the granted points are lost permanently.

The spin actions (reset/reroll/setrace/setclass) remain online-only by design; this spec
covers only the reroll-points side, which is the part the user asked to be offline-safe.

## Design

### `PlayerDataManager.migrateByName(Player p)`

New method. Behavior:

1. If the player already has a record for their real UUID (`hasRecord(p.getUniqueId())`),
   do nothing and return.
2. Otherwise scan every top-level key in `playerdata.yml`. For each key `K != realUuid`
   with a stored `.name` equal to `p.getName()` (case-insensitive):
   - Copy `K.race-rerolls` and `K.class-rerolls` into the real UUID (only when > 0).
   - Copy `K.class-slots` when it is >= 1 (so the stored `-1` "default" is not written).
   - Copy `K.joined` if present (falling back to `System.currentTimeMillis()`).
   - Delete the entire `K` record. Stop after the first match (only one phantom key can
     be owned by a given player name).
3. Save once.

The real UUID is `p.getUniqueId()`.

### `PlayerJoinListener.onJoin`

Change the order in the existing join handler:

1. Compute `boolean first = !hasRecord(p.getUniqueId())` — **before** migration, so a
   pre-granted new player still receives the first-join intro.
2. Run `plugin.getPlayerDataManager().migrateByName(p)`.
3. If `first`, call `markJoined(uuid)` (the migrated record has no `joined` key, so this
   keeps the timestamp logic consistent with the existing flow).
4. Existing reminder logic unchanged: `hasAnyRerolls(uuid)` reads the real UUID, which now
   includes the migrated points.

## Data Flow

- Admin runs `/randomrace give <name> race 2` for a never-joined player →
  `uuidFor` → `Bukkit.getOfflinePlayer(name)` → phantom UUID → 2 race rerolls stored under
  the phantom key (no record under the real UUID).
- Player joins later → `first == true` → `migrateByName` moves the phantom record's
  rerolls/slots/joined to the real UUID and deletes the phantom key →
  `markJoined` → intro sent → `hasAnyRerolls` true → reminder sent listing 2 race rerolls.
- `/randomrace check <name>` after migration reads the real-UUID record, showing 2.

## Error Handling

- `migrateByName` is a no-op when the real record already exists (protects against
  double-apply of offline grants).
- Single-match lookup (first phantom key whose stored name matches) prevents ambiguity.
- No Bukkit API calls are required inside `migrateByName` beyond the `Player` argument
  (`getUniqueId`, `getName`), so it stays unit-testable with the existing
  `PlayerDataManager(File)` constructor.

## Testing

- `PlayerDataManagerTest`:
  - migrating a phantom record moves rerolls/slots to the real UUID and deletes the phantom key;
  - `migrateByName` is a no-op when the real record already exists;
  - `class-slots` default `-1` is not copied; only explicit slots (>= 1) are.
- `mvn -q compile` and `mvn -q test` (full suite) must stay green.

## Out of Scope

- Offline spin actions (`reset`, `reroll`, `rerollclass`, `resetclass`, `setrace`,
  `setclass`) — require an online player; unchanged.
- `/valracestats` — already offline-capable and unaffected.