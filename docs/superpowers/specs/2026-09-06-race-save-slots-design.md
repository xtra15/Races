# Race Save Slots — Design Spec

**Date:** 2026-09-06
**Status:** Approved (design), pending spec review

## Purpose

A `/raceslot` GUI system that lets each player store up to 5 race snapshots
(save / replace / re-load-to-active), with a configurable cooldown on loading
to prevent rapid race switching.

## Commands & Permissions

- `/raceslot` (permission `randomrace.claim`) opens the Main GUI.
- No other commands are needed; save/load/replace are all GUI-driven.

## Flow

Main GUI → the 5 save slots in the middle row.

1. **Click EMPTY slot** → Confirm GUI "save" asks to save the player's current
   race into that slot. Green confirms (save), red cancels (back to Main).
2. **Click FILLED slot** → Sub-menu GUI opens with two choices:
   - **Save new race here** → Confirm GUI "replace" (center shows the slot's
     existing race) → green overwrites the slot with the current race.
   - **Load this race** → Confirm GUI "load" (center shows the saved race) →
     green applies that race as the active race (`AssignmentManager.assign`,
     applies ValhallaRaces buffs), marks the player claimed, and starts the
     load cooldown.
3. Saving/loading requires a current race; if the player has none, saving shows
   `&cYou have no race to save.`

Cancel paths: red glass and Esc both cancel (red reopens the Main GUI; Esc just
closes). After a successful save/replace/load, the Main GUI reopens refreshed.

## Cooldown (load only)

- Config key: `race-slot-cooldown-seconds: 30`
- Applies only to **loading** a saved race; saves/replaces are never throttled.
- While cooling down, load confirm shows `&cWait Xs before switching races.`

## GUI Layouts (single chest, 9×3)

Rows use black glass panes as filler background.

### Main GUI
- Middle row (slots 9–17 of 27): save slots at columns `0, 2, 4, 6, 8`
  (exactly one empty column between each, full-row centered).
  - Empty slot item: green stained glass pane, `&aSlot #N`, lore
    `Click to save your current race here`.
  - Filled slot item: that race's icon material, `&f<Race display name>`,
    lore `&7Slot #N`, `Click to manage`.
- Top row center: info item showing the player's current race name.

### Confirm GUI (shared layout; title/lore/center item vary)
- Middle row: `_ _ RED _ CENTER _ GREEN _ _` — 2 empty cells each side,
  1 empty cell around the center item, **red on left, green on right**.
- Green = confirm/yes. Red = cancel/no.
- Center item by case:
  - Save: current race icon; lore `Save into slot #N?`
  - Replace: the slot's existing race icon; lore `This race will be overwritten`
  - Load: the slot's saved race icon; lore `Switch to this race?`

### Sub-menu GUI (after clicking a filled slot)
- Middle row: columns `2` and `6` (equal spacing each side):
  - Col 2: `&eSave new race here` (icon: WRITABLE_BOOK), lore `Overwrite slot #N with your current race`.
  - Col 6: `&bLoad this race` (icon: DIAMOND), lore `Make this your active race (cooldown applies)`.

## Minecraft title limit

Chest inventory titles truncate at **32 characters**. All long prompts
("Do you want to save this race into this slot?", "Are you sure you want to
replace this race?") live in item **lore**; the GUI titles are short:
- Main: `&8Race Slots`
- Sub-menu: `&8Slot #N`
- Confirm save: `&aSave this race?`
- Confirm replace: `&cReplace race?`
- Confirm load: `&eLoad saved race?`

## Storage (`playerdata.yml`, per player UUID)

- `{uuid}.raceslots.1` … `.5` → race key strings (absent/null = empty slot)
- `{uuid}.race-slot-cooldown` → epoch millis until a load is allowed again
- `PlayerDataManager` additions (testable via the existing `File` constructor):
  - `String getRaceSlot(UUID, int)` (returns null when empty)
  - `void setRaceSlot(UUID, int, String)` (null clears the slot)
  - `java.util.Map<Integer,String> getRaceSlots(UUID)`
  - `long getLoadCooldown(UUID)` (0 = not cooling down)
  - `void setLoadCooldown(UUID, long)` (epoch millis)

## Rules

- Save/replace: always allowed, free, saves whatever the current race key is.
- Load: always applies the saved race (no permission re-check), marks claimed,
  starts the load cooldown, applies buffs via `AssignmentManager.assign`.
- Reroll points are untouched by this feature.

## Out of Scope

- Loading has no permission re-check (saved races may belong to admin-restricted groups).
- No per-race unlock/cost to occupy a slot.
- Reroll points unaffected.

## Testing

- `PlayerDataManagerTest`: slot get/set/clear, slots map, cooldown get/set.
- Pure cooldown helper test (remaining-seconds math), if introduced.
- `mvn -q compile` and `mvn -q test` (full suite) must stay green.

## Version

Bump `pom.xml` and `plugin.yml` to **1.3.0**.