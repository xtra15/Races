# Races — ValhallaRaces Compendium

A static website + Minecraft plugin configuration for a ValhallaRaces server with **227 races** and **127 classes**.

## Contents

| Path | Purpose |
|------|---------|
| `races.yml` | ValhallaRaces config — all 227 races (stat buffs/debuffs, lore) |
| `classes.yml` | ValhallaRaces config — all 127 classes across 10 groups |
| `assets/` | Website assets (CSS, JS, SVG icons, data) |
| `scripts/build_data.py` | Regenerates `assets/data/data.json` from the YAML configs |

## Files to deploy to the Minecraft server

Copy `races.yml` and `classes.yml` into your server's `plugins/ValhallaRaces/` folder alongside the existing `config.yml`.

## Rebuilding the website data

From the repo root:

```bash
python scripts/build_data.py
```

This reads `races.yml` / `classes.yml` and writes `assets/data/data.json` (used by the site).

## Serving the website

Any static file server works, e.g.:

```bash
python -m http.server 8080 --directory .
```

Then open `http://localhost:8080/races.html` and `http://localhost:8080/classes.html`.

## Icons

`assets/js/icons.js` ships 54 hand-drawn sigil SVGs (the original races/classes) plus an `_custom` list marking which keys are hand-drawn. Every key **not** in `_custom` automatically falls back to a **monogram letter glyph** (two-letter initials in a brass frame) rendered by `app.js` — so all 354 entries always display a clean, on-theme mark with zero extra work.

To replace a monogram with a hand-drawn SVG:
1. Add the key to the `_custom` array in `icons.js`.
2. Give that key an SVG entry (see the format in `assets/ICON_FORMAT.md`).

## Group structure

Classes are split across 10 groups; a player picks **one** class per group:

- 1 Warrior · 2 Specialist · 3 Adept · 4 Healer · 5 Guardian
- 6 Shadow · 7 Warlord · 8 Mystic · 9 Artisan · 10 Weaver

## Roadmap

- Random race/class assignment on player join (dedicated plugin, planned).
