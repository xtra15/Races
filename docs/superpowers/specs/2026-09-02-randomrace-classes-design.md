# RandomRace — Class Support Design Spec

**Date:** 2026-09-02
**Status:** Approved
**Plugin:** RandomRace (Paper 1.21.2 / api-version 1.21)
**Extends:** `docs/superpowers/specs/2026-09-02-randomrace-design.md`

## 1. Purpose

Add class assignment to RandomRace alongside races. Players get **one class per group**
(10 groups). A new `/claimclass` command rolls one weighted-random class per group using a
**3-slot chest strip** that advances group-by-group. Assignment is done in-process via
ValhallaRaces' `ClassManager`, mirroring the race integration.

## 2. ValhallaRaces Class API (validated against source)

No `ClassRegistry` class exists — classes live in static `ClassManager`:

```java
// me.athlaeos.valhallaraces.ClassManager
public static Map<String, Class> getRegisteredClasses()          // id -> Class
public static Map<Integer, Class> getClasses(Player p)            // group -> Class
public static void setClasses(Player p, Collection<Class> classes)
```

`me.athlaeos.valhallaraces.Class` getters used:
- `getName()` — class id
- `getDisplayName()` — colored display name
- `getIcon()` — `ItemStack`
- `getGroup()` — int (1-10)
- `getPermissionRequired()` — required permission, or null
- `getLimitedToRaces()` — `Collection<String>` of race ids this class is limited to
  (`race_filter`); empty = no restriction

`setClasses(player, collection)` applies stats/perks/**commands** for each class and
**merges** per group (the group key is overwritten). Passing an empty/null collection
removes all classes. `getClasses(player)` reflects the player's PersistentDataContainer;
an empty map means the player has no classes.

**Claim gate** = `ClassManager.getClasses(player)`.

## 3. Architecture & Component Changes

New/extended files under `RandomRace/src/main/java/com/yourname/randomrace/`:

| File | Responsibility |
|---|---|
| `commands/ClaimClassCommand.java` (new) | `/claimclass` |
| `gui/ClassSpinAnimation.java` (new) | 3-slot strip, group-by-group |
| `managers/ClassPoolManager.java` (new) | live class pool, group filtering, per-group pick |
| `managers/ClassAssignmentManager.java` (new) | `ClassManager` wrappers |
| `managers/WeightedPicker.java` (new) | shared weighted-selection util (races + classes) |
| `commands/RandomRaceAdminCommand.java` (modify) | add class subcommands |
| `RandomRacePlugin.java` (modify) | wire ClaimClassCommand + ClassPoolManager |
| resources `config.yml`, `plugin.yml` (modify) | class config, messages, `/claimclass` |

`RacePoolManager` keeps race logic but delegates weighting to `WeightedPicker`.

## 4. Runtime Flow (/claimclass)

```
/claimclass
  ├── permission randomrace.class? else no-permission
  ├── Map<Integer,Class> existing = ClassManager.getClasses(player)
  ├── if existing.size() >= 10 → already-claimed + VILLAGER_NO
  ├── refresh class pool (ClassManager.getRegisteredClasses())
  ├── collect groups to fill: groups 1..10 not present in `existing`
  ├── for each group g (ascending):
  │     candidates = classes with group==g filtered by:
  │         - getPermissionRequired() (null or player has it)
  │         - race_filter: if !limitedToRaces().isEmpty() AND player's race
  │           (!= null) not in it → exclude
  │     if candidates empty → skip group g (message)
  │     winner = WeightedPicker.pick(rand, candidates, class-weights)
  │     ClassSpinAnimation.rollOnce(g, winner)  // 3-slot land + per-group success msg
  ├── after all groups: ClassAssignmentManager.assign(player, winners)
  ├── final summary message
  └── optional broadcast
```

Success message per group: `&eYou are now a &b{group} {class}&e!` (group uses the config
group name, class uses display name). Final summary lists all assigned classes.

## 5. ClassSpinAnimation (3-slot)

- **3-slot chest inventory** (`InventoryType.CHEST`, rows=1, 3 columns).
- Center slot (index 1) is the winner window.
- Left/right slots show neighboring classes for depth.
- Each **rollOnce(group, winner)** runs a short 3-phase deceleration (reuse the 2/4/8-tick,
  5/3/2 cycle pattern) landing the winner in the center, then re-opens/advances to the
  next group. The window title shows the current group name (e.g. `&8— Group 1: Warrior —`).
- Icons from `class-materials.<id>` → `class.getIcon()` → `PAPER`.
- Winner guaranteed to land center (winner placed at `reel[TOTAL_TICKS + CENTER]`).
- Cancel cleanly on close/quit/disable; nothing is assigned until the full pass completes.

## 6. Sounds

Reuse `SoundUtil`. Per-roll: `BLOCK_CHEST_OPEN` on open, `UI_BUTTON_CLICK` each tick,
`BLOCK_NOTE_BLOCK_PLING` on each land, `ENTITY_FIREWORK_ROCKET_BLAST` on final completion.

## 7. Config Additions (config.yml)

```yaml
class-weights:
  berserker: 30          # per class id; unlisted = equal

class-materials:
  berserker: IRON_SWORD  # per class id; else class icon; else PAPER

groups:                  # display names for group numbers
  1: "Warrior"
  2: "Specialist"
  # ... 1-10

class-one-time-only: true

broadcast-class: true

messages:
  class-no-permission: "&cYou don't have permission to use this."
  class-already-claimed: "&cYou already have all your classes!"
  class-assigned: "&eYou are now a &b{group} {class}&e!"
  class-summary: "&aYour classes are now: &e{classes}&a!"
  class-broadcast: "&e{player} &ahas been destined with their classes!"
```

Group names 1-10 defaults: Warrior, Specialist, Adept, Healer, Guardian, Shadow, Warlord,
Mystic, Artisan, Weaver (same order the site uses).

## 8. Commands & Permissions Additions

Add to `plugin.yml`:

```yaml
commands:
  claimclass:
    description: Roll your classes (one per group)
    permission: randomrace.class

permissions:
  randomrace.class:
    default: true
```

Admin `/randomrace` gains (all `randomrace.admin`):

| Subcommand | Action |
|---|---|
| `resetclass <player>` | Clear all classes via `ClassManager.setClasses(player, empty)`, allow re-roll |
| `rerollclass <player>` | Clear classes, run a fresh full class roll |
| `setclass <player> <group> <class>` | Assign one class for a group (merged via setClasses) |
| `listclass` | List all classes loaded from ValhallaRaces |

`reload` already refreshes the class pool via `ClassPoolManager.refresh()`.

## 9. Persistence

No change to `playerdata.yml` semantics. The class gate is `ClassManager.getClasses(player)`
(live). `PlayerDataManager` is not used for the class gate.

## 10. Build / Stub

Extend `src/main/stub/me/athlaeos/valhallaraces/`:

- `Class.java` — `getName()`, `getDisplayName()`, `getIcon()`, `getGroup()`,
  `getPermissionRequired()`, `getLimitedToRaces()`.
- `ClassManager.java` — `getRegisteredClasses()`, `getClasses(Player)`
  (`Map<Integer, Class>`), `setClasses(Player, Collection<Class>)`.

Signatures match the verified ValhallaRaces source (§2). Stub is compile-only, excluded
from the jar (unchanged mechanism).

## 11. Testing

Unit tests (JUnit) for pure logic:
- `ClassPoolManager` per-group candidate filtering: permission filter, **race_filter**
  (limited to empty = include; non-empty + player race not listed = exclude; non-empty +
  player race listed = include).
- `WeightedPicker` weighted selection bounds + empty-pool null.
- Gate logic (existing classes size).
The 3-slot GUI/animation and `ClassManager.setClasses` integration are compile-verified
and validated on a live server.
