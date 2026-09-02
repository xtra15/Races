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

## Icon placeholders

`assets/js/icons.js` ships with placeholder sigil SVGs for every race and class (350 total). Each entry is a set of SVG path/line primitives inside a 64×64 viewBox with `fill="none"` and `stroke="currentColor"`. Replace the placeholder under each key to customize the icon.

## Group structure

Classes are split across 10 groups; a player picks **one** class per group:

- 1 Warrior · 2 Specialist · 3 Adept · 4 Healer · 5 Guardian
- 6 Shadow · 7 Warlord · 8 Mystic · 9 Artisan · 10 Weaver

## Roadmap

- Random race/class assignment on player join (dedicated plugin, planned).
