# Icon SVG Format - for DeepSeek

Generate line-art "sigil" SVG icons for every race and class. Follow this format EXACTLY.

## An example icon (dragonkin)

Each icon is the **inner content** of an `<svg>` tag with this wrapper:

```html
<svg viewBox="0 0 64 64" width="64" height="64" fill="none"
  stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"
  aria-hidden="true">
  <!-- INNER CONTENT GOES HERE (the part generated) -->
</svg>
```

### dragonkin (dragon head, open jaw, swept horn)

```html
<path d="M20 46 C14 44 12 38 14 32 C16 26 22 24 30 24 C38 24 42 26 46 30 C50 34 50 40 44 44 C40 48 32 50 26 50 C22 50 19 48 20 46 Z"/>
<path d="M30 24 C28 16 22 12 16 12"/>
<path d="M20 46 L14 56 L24 50"/>
<circle cx="30" cy="31" r="2"/>
<path d="M46 30 L52 27 M46 33 L52 31"/>
```

## RULES

1. **Coordinate space:** 0 to 64 (X) and 0 to 64 (Y). Keep the whole design inside these bounds with a small margin so it is not clipped.
2. **Line art only:** no filled solids. Set everything with `fill="none"`; the outline color comes from `stroke="currentColor"` automatically - do NOT hardcode colors.
3. **One cohesive style:** thin, elegant, hand-drawn-looking lines. Use `M`, `L`, `C`, `Q`, `Z` path commands, plus `<circle>` and `<rect>` where clean.
4. **Center it:** the visual mass should sit roughly centered in the 64x64 box.
5. **Depth via opacity:** use `opacity=".5"` / `opacity=".6"` on secondary elements for layering.
6. **Keep it simple-to-medium:** use ~3-8 elements per icon. Clean silhouette, readable at 64px and 132px.
7. **Thematic:** the icon must depict the race/class concept (e.g. a flame for fire, a blade for a warrior, a moon for lunar, etc.).

## Icon key inventory (354 total)

Every key below maps to an entry in `assets/js/icons.js` whose value must be replaced with a custom SVG. Keep the exact key spelling (the key is what the site uses to look up the icon).

### Races (227)

dragonkin, kitsune, titanborn, drow, celestial, abyssal, naga, djinn, satyr, treant, orc, dwarf, undead, human, vampire, elf, werewolf, dryad, beastkin, avian, fairy, brethren, tortle, hafis, golemkin, frostborne, wraith, fire_elemental, water_elemental, earth_elemental, air_elemental, lightning_elemental, magma_lord, stormborn, tidal_dancer, glacial, volcanic, dust_wraith, mistwalker, ashborn, cinder_spark, tempest_lord, sky_sovereign, inferno_touched, void_essence, ember_knight, frost_kin, ember_soul, wolf_blooded, bear_folk, hawk_kin, serpent_blooded, spider_kin, raven_folk, fox_blooded, stag_folk, shark_kin, lion_folk, owlkin, raptor_kin, boar_folk, bat_folk, lupine_hunter, serpent_sages, lich, banshee, revenant, spectral, shade, specter, poltergeist, ghost_kin, zombie_forged, seraph, archon, demigod, solar_angel, lunar_kin, starborn, cherub, aasimar, imp, cambion, pit_fiend, balor, tiefling, shadow_demon, nightmare, void_fiend, sprite, pixie, centaur, sylph, gnome, leshy, mushroom_folk, treant_sprout, faun, merfolk, sea_elf, kelpie, sahuagin, triton, deep_one, abyssal_serpent, pearl_mermaid, automaton, warforged, clockwork, crystal_golem, construct, soulforged, ogre, troll, jotun, cyclops, firbolg, goliath, half_giant, verdant_giant, monolith, astral, void_touched, ethereal, planar, chrono, rune_carved, soul_echo, dream_walker, aether_born, null_kin, sand_wraith, iron_bound, bloodkin, storm_herald, crystal_shard, twilight_elf, dust_djinn, ironheart, rune_sorcerer, storm_spirit, thornweaver, ember_drake, storm_dragon, void_serpent, iron_drake, frost_dragon, sandstorm_beast, wild_kin, abyssal_kraken, crystal_nymph, mossling, shadow_drake, bone_colossus, ash_knight, lava_walker, ice_witch, plague_bearer, flamecaller, glacierborn, stonecaller, windrider, thunderlord, ashwalker, tidecaller, dustfiend, ember_sprite, frost_spirit, storm_wraith, earth_shaper, sky_dancer, shadowcaster, plague_doctor, void_weaver, crystal_mage, moon_weaver, sunCaller, starCaller, abyss_walker, soul_reaper, bone_weaver, sand_serpent, tundra_wolf, swamp_hag, sky_dragon, iron_golem, dark_elf, high_elf, wood_elf, sea_dwarf, mountain_giant, hill_giant, fog_phantom, dust_devil, magma_sprite, frost_fairy, shadow_fairy, star_fairy, plague_witch, warlock_v2, demon_hunter, vampire_hunter, dragon_slayer, undead_hunter, giant_slayer, troll_kin, orc_raider, elven_ranger, dwarven_smith, human_mage, undead_mage, celestial_warrior, abyssal_warrior, magma_golem, frost_golem, storm_golem, void_golem, shadow_elf, flame_elf, ice_elf, mountain_dwarf, hill_dwarf, deep_dwarf, necro_undead, war_undead, spirit_undead, wight

### Classes (127)

berserker, warrior, paladin, death_knight, spellbreaker, assassin, monk, barbarian, ranger, champion, duelist, marauder, gladiator, lancer, warmonger, reaper, juggernaut, blade_dancer, pit_fighter, sky_knight, alchemist, mage, warlock, cleric, enchanter, druid, shaman, void_knight, blacksmith, marksman, hunter, sniper, falconer, ballistae, slinger, arbalist, sharpshooter, beastmaster, trapper, miner, farmer, gunslinger, samurai, ninja, bard, warden, terraformer, spellblade, sorcerer, elementalist, conjurer, illusionist, necromancer, witch, battle_mage, pyromancer, cryomancer, storm_caller, geomancer, sage, apothecary, battle_medic, oracle, chanter, priest, spirit_walker, life_binder, confessor, herbalist, warden_of_woods, sentinel, bulwark, guardian, fortress, aegis, stone_warden, ironclad, phalanx, colossus, shadow, infiltrator, nightblade, whisper, cutthroat, phantom, renegade, deadeye, scoundrel, trickster, shadow_blade, beast_tamer, undead_commander, golemancer, banneret, warlord, commander, ritualist, binder, spellthief, blade_mage, runic_warrior, hexblade, arcane_archer, battle_cleric, spirit_knight, runepriest, mystic, adept, artificer, jeweler, tinker, skinner, lumberjack, mason, weaver, brewer, cartographer, runesmith, fate_weaver, void_walker, time_mage, dreamwalker, soul_binder, starweaver, chaos_mage, blood_mage, thaumaturge

## How to deliver

Give the results as a JavaScript object in the SAME format as `assets/js/icons.js`:

```js
const ICONS = {
  fire_elemental: `/* flame rising from a stone */
    <path .../>
    <circle .../>`,
  water_elemental: `...`,
  /* ... all 354 keys ... */
};
```

The `window.ICONS = ICONS;` assignment is handled separately.

IMPORTANT: every one of the 354 keys above MUST be present. If you cannot render a specific concept, substitute a thematic-but-generic sigil (e.g. a diamond crest) so the key is always filled.
