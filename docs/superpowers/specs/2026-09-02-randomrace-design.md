# RandomRace Plugin — Design Spec

**Date:** 2026-09-02
**Status:** Approved
**Plugin:** RandomRace (Paper 1.21.2 / api-version 1.21)
**Depends on:** ValhallaMMO, ValhallaRaces (both hard dependencies)

## 1. Purpose

A Paper plugin that gives each player a randomly selected ValhallaRaces race via a
slot-machine chest GUI. The race pool is pulled **live** from ValhallaRaces' registry at
runtime — there is no duplicate race config in this plugin. Players claim one race per
account (one-time), with optional weighted randomization and admin re-roll/reset.

## 2. ValhallaRaces Integration (validated against source)

All integration points were verified against `github.com/Athlaeos/ValhallaRaces`
(commit on `main`, version 2.1). Full source is pinned in the build (see §10).

### 2.1 Race pool access

There is **no `RaceRegistry` class**. Races are exposed via a static registry:

```java
// me.athlaeos.valhallaraces.RaceManager
public static Map<String, Race> getRegisteredRaces() { return registeredRaces; }
```

- Registry type: `Map<String, Race>`
- `Race` public getters (me.athlaeos.valhallaraces.Race):
  - `getName()` — race key (id)
  - `getDisplayName()` — colored display name
  - `getIcon()` — `ItemStack` icon (null if unset)
  - `getPermissionRequired()` — required permission to pick, or null
- Races are registered in `RaceManager.loadRaces()` reading `races.yml` from ValhallaRaces'
  own data folder.

### 2.2 Assigning a race

Assign in-process via the static manager. This applies stat buffs, perk rewards, and any
`commands:`/`undo_commands:` and writes to the player's PersistentDataContainer:

```java
RaceManager.setRace(Player player, Race race);
RaceManager.setRace(player, null); // removes the race
```

Do **not** dispatch the `/races set race` console command. Its argument order is
`<player> <race>` (not `<race> <player>`), it requires the `valhallaraces.manager`
permission (op), and is redundant given a hard dependency. Direct API calls are atomic and
carry no string-parsing risk. Note: `RaceManager.setRace` must run on the main thread.

### 2.3 Claim gate ("already has a race")

The authoritative source of truth is the player's live race state, not this plugin's own
storage:

```java
RaceManager.getRace(Player player); // null if the player has no race
```

`RaceManager.getRace(player)` reflects the PersistentDataContainer. This avoids desync when
an admin runs `/races reset race` on a player. This plugin's `playerdata.yml` stores only
supplementary metadata (claim timestamp), never the gate itself.

## 3. Architecture & Components

Single plugin, package `com.yourname.randomrace`.

```
src/main/java/com/yourname/randomrace/
├── RandomRacePlugin.java          # main class; wires managers + commands; reload
├── commands/
│   ├── ClaimRaceCommand.java      # /claimrace
│   └── RandomRaceAdminCommand.java# /randomrace subcommands
├── gui/
│   └── SpinAnimation.java         # 9x1 chest slot-machine + deceleration loop
├── managers/
│   ├── RacePoolManager.java       # pulls/filters/weights races live from RaceManager
│   ├── PlayerDataManager.java     # playerdata.yml (metadata only)
│   └── AssignmentManager.java     # in-process RaceManager.setRace wrappers
└── utils/
    ├── SoundUtil.java             # centralized sound effects
    └── MessageUtil.java           # message formatting + replacement
src/main/resources/
├── plugin.yml
├── config.yml
└── playerdata.yml                 # empty default (filled at runtime)
```

## 4. Runtime Flow

```
Server start
  └── RacePoolManager.refresh()  // cache of available Races from RaceManager

/claimrace
  ├── permission randomrace.claim? else no-permission
  ├── RaceManager.getRace(player) != null → already-claimed + VILLAGER_NO
  ├── refresh pool (live)
  ├── if pool empty → message, abort
  ├── weighted pre-select winner (weights or equal)
  ├── open 9x1 GUI, spin
  │    Phase 1 fast   (2-tick delay, 20 cycles)
  │    Phase 2 medium (4-tick delay, 10 cycles)
  │    Phase 3 slow   (8-tick delay,  5 cycles)
  │    winner lands in center slot (slot 4)
  ├── 2s pause → close GUI
  ├── AssignmentManager.assign(player, race)   // RaceManager.setRace
  ├── record metadata in playerdata.yml
  ├── assigned message + FIREWORK (+ optional broadcast)
```

## 5. Animation (SpinAnimation)

- 9x1 chest inventory (`InventoryType.CHEST`, rows=1).
- Center slot (index 4) is the selector window labeled `▼ YOUR RACE ▼`.
- Slots left/right show neighboring race icons for depth.
- Items scroll right → left across all 9 slots per tick.
- Race icon: `race-materials.<name>` override from config, else `race.getIcon()`
  (material), else `PAPER`.
- Race name shown: `race.getDisplayName()`.
- Deceleration: three phases by tick delay (2 → 4 → 8) and cycle counts (20/10/5).
- Winner is pre-selected (weighted) so the center slot lands deterministically.
- Animation uses `Bukkit.getScheduler().runTaskTimer` on the main thread. Cancel
  cleanly on inventory close / plugin disable / player quit.
- On close mid-animation, cancel the task; the player keeps no race (nothing applied yet).

## 6. Sound Design (SoundUtil)

| Event             | Sound                                        |
|-------------------|----------------------------------------------|
| Spin starts       | `BLOCK_CHEST_OPEN`                           |
| Each scroll tick  | `UI_BUTTON_CLICK`                            |
| Slowing down      | `UI_BUTTON_CLICK` (longer delay between)     |
| Final stop        | `BLOCK_NOTE_BLOCK_PLING`                     |
| Race assigned     | `ENTITY_FIREWORK_ROCKET_BLAST`               |
| Already claimed   | `ENTITY_VILLAGER_NO`                         |

All names are valid Paper 1.21 `org.bukkit.Sound` enums.

## 7. Config (config.yml)

```yaml
# No race definitions — the pool comes live from ValhallaRaces.

# Optional weight per race. Unlisted races default to equal weight (1).
race-weights:
  human: 40

one-time-only: true

# Optional icon material override per race. Unlisted → race.getIcon() / PAPER.
race-materials:
  human: PLAYER_HEAD

messages:
  already-claimed: "&cYou have already claimed your race!"
  spin-start: "&eThe fates are deciding your race..."
  race-assigned: "&aYou have been chosen as a &e{race}&a!"
  no-permission: "&cYou don't have permission to use this."
  broadcast: "&e{player} &ahas been destined to be a &e{race}&a!"
```

There is **no `valhalla-command` option** — assignment is in-process (§2.2).

## 8. Commands & Permissions

| Command | Permission | Action |
|---|---|---|
| `/claimrace` | `randomrace.claim` | Run the spin, assign the race |
| `/randomrace reset <player>` | `randomrace.admin` | Remove live race + metadata, allow re-claim |
| `/randomrace reroll <player>` | `randomrace.admin` | Force a fresh spin for a player |
| `/randomrace setrace <player> <race>` | `randomrace.admin` | Directly assign, skip animation |
| `/randomrace reload` | `randomrace.admin` | Reload config + refresh pool |
| `/randomrace listrace` | `randomrace.admin` | List live race ids/names from the pool |

### plugin.yml

```yaml
name: RandomRace
version: 1.0.0
main: com.yourname.randomrace.RandomRacePlugin
api-version: 1.21
depend: [ ValhallaMMO, ValhallaRaces ]

commands:
  claimrace:
    description: Spin to claim your race
    permission: randomrace.claim
  randomrace:
    description: Admin commands
    permission: randomrace.admin

permissions:
  randomrace.claim:
    default: true
  randomrace.admin:
    default: op
  randomrace.admin.bypass:
    default: op
```

## 9. Persistence (playerdata.yml)

- Keyed by player UUID.
- Stores metadata only: `claimed: <timestamp>`.
- Not a gate — the gate is `RaceManager.getRace(player)` (§2.3).
- `reset` clears the corresponding entry.

## 10. Build

- Maven (`pom.xml`), compile target Java 21 (Paper 1.21.2 requires Java 21 bytecode).
- **No published ValhallaRaces artifact exists.** `github.com/Athlaeos/ValhallaRaces`
  README documents `me.athlaeos:valhallaraces:2.1` on the repsy repo, but that artifact
  returns HTTP 404 (verified). The repsy repo only publishes `me.athlaeos:valhallammo-*`
  artifacts. ValhallaRaces is also **not** published to its declared distribution repo.
  Building ValhallaRaces from source is not viable: it depends on `valhallammo-dist` and a
  large tree of `valhallammo-paper1_21_R*:premium_*` artifacts whose resolution times out
  (verified: network timeouts on `repo.repsy.io`), making the upstream build fragile.
- **Resolution — compile against a stub.** RandomRace declares a compile-time-only stub of
  exactly the ValhallaRaces API surface it calls, in the same package via a `stub/` source
  root. The stub is used for compilation only (never shipped, never loaded):
  - `me.athlaeos.valhallaraces.RaceManager` — `getRegisteredRaces()`, `getRace(player)`,
    `setRace(player, race)` (and `setRace(player, null)`).
  - `me.athlaeos.valhallaraces.Race` — `getName()`, `getDisplayName()`, `getIcon()`,
    `getPermissionRequired()`.
  - These signatures match the verified ValhallaRaces source (§2). At runtime the real
    ValhallaRaces classes on the server override/back the same fully-qualified names; the
    stub is never present in the packaged jar (`stub/` is excluded from packaging).
- Paper API (compile-only) from the papermc repo.
- Shade not required (no external runtime deps of our own).
- `plugin.yml` declares `depend: [ ValhallaMMO, ValhallaRaces ]` so the server guarantees
  the real types are loaded before RandomRace.

## 11. Resolved Build Risk

The §10 stub approach removes the original open item (published artifact availability).
Required stub signatures are pinned to the verified ValhallaRaces source. If a future
ValhallaRaces release changes any of these signatures, update the stub and recompile. The
only remaining manual step is ensuring the deployed ValhallaRaces on the server matches
these signatures (2.x lineage, which they do).
