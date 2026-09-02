# RandomRace

A Paper plugin that gives each player a randomly selected **ValhallaRaces** race via a
slot-machine chest GUI. The race pool is pulled **live** from ValhallaRaces at runtime —
there is no duplicate race config. Players claim one race (`/claimrace`), with optional
weighted randomization and admin re-roll/reset.

## Requirements

- **Paper** 1.21+ (`api-version: 1.21`)
- **ValhallaRaces** (required at runtime)
- **ValhallaMMO** (required by ValhallaRaces, also a hard dependency)

Both are declared as hard dependencies in `plugin.yml`. This plugin does **not** ship or
duplicate any race definitions; whatever races exist on the server are used automatically.

## Install

Build with Maven, then drop the jar into the server's `plugins/` folder:

```bash
mvn package
# Result: target/randomrace-1.0.0.jar
```

## Commands & Permissions

| Command | Permission | Action |
|---|---|---|
| `/claimrace` | `randomrace.claim` | Run the spin and assign a random race |
| `/randomrace reset <player>` | `randomrace.admin` | Remove the player's race, allow re-claim |
| `/randomrace reroll <player>` | `randomrace.admin` | Force a fresh spin for the player |
| `/randomrace setrace <player> <race>` | `randomrace.admin` | Directly assign a race (no animation) |
| `/randomrace reload` | `randomrace.admin` | Reload config + refresh the race pool |
| `/randomrace listrace` | `randomrace.admin` | List races currently loaded from ValhallaRaces |

`randomrace.claim` defaults to all players; `randomrace.admin` defaults to ops.

## How it works

- On startup and before each `/claimrace`, the plugin refreshes its pool from
  `RaceManager.getRegisteredRaces()` (ValhallaRaces' live registry).
- Races the player lacks permission for (ValhallaRaces `permission:` key) are hidden from
  their pool.
- A weighted winner is pre-selected, then a 9x1 chest slot-machine animates across 3 phases
  (fast → medium → slow) and lands the winner in the center slot.
- Assignment is done **in-process** via `RaceManager.setRace(player, race)` — this applies
  the race's stat buffs, perk rewards, and configured commands. No command dispatch.
- The "already claimed" gate is `RaceManager.getRace(player) != null`, so it stays in sync
  with ValhallaRaces (e.g. if an admin runs `/races reset race`).

## Configuration (`config.yml`)

```yaml
race-weights:
  human: 40        # Optional weight per race id. Unlisted races default to equal weight.

one-time-only: true

race-materials:
  human: PLAYER_HEAD   # Optional icon material override per race id.

broadcast-enabled: true

messages:
  already-claimed: "&cYou have already claimed your race!"
  spin-start: "&eThe fates are deciding your race..."
  race-assigned: "&aYou have been chosen as a &e{race}&a!"
  no-permission: "&cYou don't have permission to use this."
  broadcast: "&e{player} &ahas been destined to be a &e{race}&a!"
```

`{race}` and `{player}` are replaced in message strings. Race ids in `race-weights` /
`race-materials` must match the ValhallaRaces `races.yml` keys.

## Build note

`me.athlaeos:valhallaraces` is not published to any Maven repository, so this project
compiles against a compile-time-only stub of the `Race` / `RaceManager` API
(`src/main/stub/`, excluded from the packaged jar). The real ValhallaRaces classes are used
at runtime. If a future ValhallaRaces release changes one of these signatures, update the
stub and recompile.
