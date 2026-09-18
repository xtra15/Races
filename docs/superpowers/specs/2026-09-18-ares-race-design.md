# Ares Race Design

**Date:** 2026-09-18
**Status:** approved design, awaiting implementation plan
**Scope:** one new race entry (`ares`) in `plugin/races.yml` + website rebuild + one custom SVG sigil in `site/assets/js/icons.js`. No plugin-code changes.

## Goal

Add **Ares**, a god-of-war race: nearly untouchable (70% dodge), fast, slightly small, harder-hitting in melee — paid for with low health and weak armor. Fierce red (`&c`) identity, netherite-axe in-game icon, hand-drawn Corinthian war-helm sigil on the site.

## Decisions

- Kit follows "Approach A, balanced war god" but with `DODGE_CHANCE: 0.7` per user choice (flagged: 2.8x above the existing 0.25 ceiling; accepted as the race's defining fantasy).
- In-game icon is `NETHERITE_AXE:-1` — `NETHERITE_SWORD:-1` was requested but is already taken by `demon_hunter`, and icons must be unique per race.
- Small size (`SCALE: -0.2`) is listed under "suffers" in lore to match the site, which classifies negative size as a debuff (final card: 3 buffs / 3 debuffs).

## Race block (append to `races:` in `plugin/races.yml`)

```yaml
  ares:
    position: 250 # Position in racepicker GUI (free: used range is 9-249)
    icon: NETHERITE_AXE:-1 # Icon in racepicker GUI (NETHERITE_SWORD taken by demon_hunter)
    icon_locked: BARRIER:-1 # Icon in racepicker GUI if another race has already been selected
    prefix: '&8[&cAres&8]' # Chat race prefix
    display_name: '&cAres' # Display name in racepicker GUI
    description: # Lore in racepicker GUI
      - '&cAres&7, the god of war incarnate, a'
      - '&7blur of bronze and blood. No blade'
      - '&7can touch him, yet every wound he'
      - '&7takes cuts to the bone'
      - '&8&m                                       '
      - '&cAres &7benefits from'
      - '&f- &c+70% &fDodge Chance'
      - '&f- &c+15% &fMovement Speed'
      - '&f- &c+10% &fMelee Damage'
      - '&7But suffers from'
      - '&f- &c-5 &fMaximum Health'
      - '&f- &c-10% &fArmor Effectiveness'
      - '&f- &c-20% &fSize'
    stat_buffs: # Stat buffs the race provides
      DODGE_CHANCE: 0.7
      MOVEMENT_SPEED_BONUS: 0.15
      MELEE_DAMAGE_DEALT: 0.1
      HEALTH_BONUS: -5
      ARMOR_MULTIPLIER_BONUS: -0.1
      SCALE: -0.2
```

Uniqueness verified 2026-09-18: key `ares` free, display name `Ares` free, `NETHERITE_AXE:-1` unused by any race, position 250 unused. Total becomes 228 races.

## Website pipeline

1. Append the block above to `plugin/races.yml`.
2. Run `python scripts/build_data.py` from repo root — regenerates `site/assets/data/data.json`.
3. Verify: race count 228, Ares card shows +70% Dodge Chance / +15% Movement Speed / +10% Melee Damage buffs and -5 Maximum Health / -10% Armor Effectiveness / -20% Size debuffs, modal opens.
4. Serve locally (`python -m http.server 8080 --directory site`) and eyeball `races.html`.

## SVG sigil (`ares` in `site/assets/js/icons.js`)

Add `ares` to the `_custom` array and add this body to `ICONS` (inner content of the standard 64x64 wrapper per `ICON_FORMAT.md`; Corinthian war-helm, plume at reduced opacity for depth):

```html
<path d="M20 52 C20 33 24 19 32 19 C40 19 44 33 44 52"/>
<path d="M32 19 C32 11 28 7 21 6 C26 4 33 7 34 14"/>
<path d="M32 19 C31 13 29 10 26 8" opacity=".5"/>
<path d="M25 40 H39"/>
<path d="M32 40 V52"/>
<path d="M24 44 C25 48 27 50 30 51"/>
<path d="M40 44 C39 48 37 50 34 51"/>
```

Verify the sigil renders centered and unclipped on the Ares card at 64px and in the modal at 132px.

## Out of scope

- No `RandomRace` plugin changes, no version bump (content-only change; data rebuild only).
- No git commits unless the user asks (project convention).
