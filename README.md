# ValhallaRaces — Project

Local project folder for the ValhallaRaces plugin configuration and companion website.

## Structure

```
ValhallaRaces/
├── plugin/            # Minecraft server config (deploy to plugins/ValhallaRaces/)
│   ├── races.yml      #   227 races (stats, lore)
│   ├── classes.yml    #   127 classes across 10 groups
│   └── config.yml     #   server options (pick_race/pick_class, menu)
├── site/              # Companion website (static, no build step)
│   ├── index.html     #   Home
│   ├── races.html     #   Races compendium
│   ├── classes.html   #   Classes compendium
│   └── assets/        #   CSS, JS, SVG icons, data.json
└── scripts/           # Generators and builders
    ├── build_data.py          # Regenerates site/assets/data/data.json from plugin/*.yml
    ├── generate_content.py    # Generated the 200 races + 100 classes
    ├── merge_website.py       # One-off: merged new entries into website data
    └── gen_icons.py           # One-off: generated placeholder icon slots
```

## Deploying to the server

Copy `plugin/races.yml` and `plugin/classes.yml` into your server's
`plugins/ValhallaRaces/` folder (alongside the existing `config.yml`).

## Rebuilding website data

Edits to `plugin/races.yml` or `plugin/classes.yml` won't show on the site until the
data is rebuilt:

```bash
python scripts/build_data.py
```

This reads `plugin/races.yml` / `plugin/classes.yml` and writes
`site/assets/data/data.json`.

## Running the website locally

Serve the `site/` folder with any static file server:

```bash
python -m http.server 8080 --directory site
```

Then open `http://localhost:8080/races.html` and `http://localhost:8080/classes.html`.

## Icons

Icons are line-art monogram glyphs generated automatically by `app.js` for every
entry. The 54 original races/classes use hand-drawn SVGs listed in `ICONS._custom`
in `site/assets/js/icons.js`. To use a custom SVG for an entry, add its key to
`_custom` and give it an SVG body (format in `site/assets/ICON_FORMAT.md`).

## GitHub

The website + configs are also published to `github.com/xtra15/Races` (repo root
layout with `races.yml`/`classes.yml` at root and the site files at root).
