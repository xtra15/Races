#!/usr/bin/env python3
"""
ValhallaRaces Content Generator
Generates 200 new races, 100 new classes, and website data JSON.
"""
import json, os, random

random.seed(42)

EXISTING_RACES = {
    "dwarf","human","elf","orc","undead","vampire","werewolf","beastkin",
    "fairy","brethren","hafis","dragonkin","kitsune","titanborn","drow",
    "celestial","abyssal","naga","djinn","satyr","treant","dryad","avian",
    "tortle","golemkin","frostborne","wraith"
}
EXISTING_CLASSES = {
    "warrior","barbarian","ranger","alchemist","enchanter","blacksmith",
    "miner","farmer","terraformer","berserker","paladin","death_knight",
    "spellbreaker","assassin","monk","mage","warlock","cleric","druid",
    "shaman","void_knight","gunslinger","samurai","ninja","bard","warden",
    "spellblade"
}

SEP = "&8&m                                       "

def yval(v):
    if isinstance(v, float):
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        return s
    return str(v)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def build_desc(display_name, color, lore_lines, buff_descs, debuff_descs):
    lines = list(lore_lines)
    lines.append(SEP)
    lines.append(f"{color}{display_name} &7benefit from")
    for d in buff_descs:
        lines.append(f"&f- &a{d}")
    if debuff_descs:
        lines.append("&7But suffer from")
        for d in debuff_descs:
            lines.append(f"&f- &c{d}")
    return lines

def stat_desc(stat, val, flat=False):
    pretty = stat.replace("_", " ").title()
    if flat or stat in ("HEALTH_BONUS",):
        sign = "+" if val > 0 else ""
        return f"{sign}{int(val)} &f{pretty}"
    if abs(val) < 1:
        pct = int(val * 100)
    else:
        pct = int(val)
    if pct > 0:
        return f"+{pct}% &f{pretty}"
    else:
        return f"{pct}% &f{pretty}"

def make_race_yaml(name, pos, icon, color, display, lore, stats, size_delta=0):
    sd = ""
    if size_delta > 0:
        sd = f" (+{size_delta}% Size)"
    elif size_delta < 0:
        sd = f" ({size_delta}% Size)"
    descs_b = []
    descs_d = []
    for s, v in stats.items():
        d = stat_desc(s, v, s == "HEALTH_BONUS")
        if v >= 0:
            descs_b.append(d)
        else:
            descs_d.append(d)
    desc = build_desc(display, color, lore, descs_b, descs_d)
    lines = []
    lines.append(f"  {name}:")
    lines.append(f"    position: {pos}")
    lines.append(f"    icon: {icon}")
    lines.append(f"    icon_locked: BARRIER:-1")
    lines.append(f"    prefix: '&8[{color}{display}&8]'")
    lines.append(f"    display_name: '{color}{display}'")
    lines.append(f"    description:")
    for dl in desc:
        lines.append(f"      - '{dl}'")
    lines.append(f"    stat_buffs:")
    for sk, sv in stats.items():
        lines.append(f"      {sk}: {yval(sv)}")
    return "\n".join(lines)

def make_class_yaml(name, grp, pos, icon, color, display, lore, stats):
    descs_b = []
    descs_d = []
    for s, v in stats.items():
        d = stat_desc(s, v, s == "HEALTH_BONUS")
        if v >= 0:
            descs_b.append(d)
        else:
            descs_d.append(d)
    desc = build_desc(display, color, lore, descs_b, descs_d)
    lines = []
    lines.append(f"  {name}:")
    lines.append(f"    group: {grp}")
    lines.append(f"    position: {pos}")
    lines.append(f"    icon: {icon}")
    lines.append(f"    icon_locked: BARRIER:-1")
    lines.append(f"    display_name: '{color}{display}'")
    lines.append(f"    description:")
    for dl in desc:
        lines.append(f"      - '{dl}'")
    lines.append(f"    stat_buffs:")
    for sk, sv in stats.items():
        lines.append(f"      {sk}: {yval(sv)}")
    return "\n".join(lines)

# ─── RACE DEFINITIONS ──────────────────────────────────────────────────────
RACE_DEFS = []

# Helper to add race
def R(name, icon, color, display, lore, stats):
    assert name not in EXISTING_RACES, f"Duplicate race: {name}"
    EXISTING_RACES.add(name)
    RACE_DEFS.append((name, icon, color, display, lore, stats))

# ── ELEMENTAL ──
R("fire_elemental","BLAZE_POWDER:-1","&c","Fire Elemental",
  ["&cFire Elementals&7, beings born from living","&7flame that roam scorched wastes.","&7Their bodies burn all who draw near.","&7Fire is their ally but ice undoes them."],
  {"FIRE_DAMAGE_DEALT":0.3,"FIRE_RESISTANCE":0.4,"MELEE_DAMAGE_DEALT":0.15,"FREEZING_RESISTANCE":-0.25,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("water_elemental","PRISMARINE_SHARD:-1","&3","Water Elemental",
  ["&3Water Elementals&7, fluid beings of living","&7water from the deepest oceans.","&7They freeze foes and sustain allies.","&7Fire scorches their liquid forms."],
  {"FREEZING_DAMAGE_DEALT":0.25,"HEALING_BONUS":0.2,"MAGIC_RESISTANCE":0.15,"FIRE_RESISTANCE":-0.2})

R("earth_elemental","STONE:-1","&6","Earth Elemental",
  ["&6Earth Elementals&7, colossal beings of","&7living stone and soil. Their rocky","&7hides shrug off blows, but they","&7are ponderous and slow."],
  {"ARMOR_MULTIPLIER_BONUS":0.25,"DAMAGE_RESISTANCE":0.2,"KNOCKBACK_RESISTANCE":0.3,"HEALTH_BONUS":5,"MOVEMENT_SPEED_BONUS":-0.2,"DODGE_CHANCE":-0.15})

R("air_elemental","FEATHER:-1","&f","Air Elemental",
  ["&fAir Elementals&7, swift invisible beings","&7of howling wind. They dart across the","&7battlefield instantly but their","&7bodies are wisps of nothing."],
  {"MOVEMENT_SPEED_BONUS":0.2,"SPRINT_MOVEMENT_SPEED_BONUS":0.2,"DODGE_CHANCE":0.15,"RANGED_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("lightning_elemental","LIGHTNING_ROD:-1","&e","Lightning Elemental",
  ["&eLightning Elementals&7, crackling beings","&7of living thunder. They strike with","&7devastating speed, but their","&7volatile nature makes them unstable."],
  {"LIGHTNING_DAMAGE_DEALT":0.3,"COOLDOWN_REDUCTION":0.2,"MOVEMENT_SPEED_BONUS":0.15,"CRIT_CHANCE":0.1,"LIGHTNING_RESISTANCE":-0.15,"HEALTH_BONUS":-3})

R("magma_lord","MAGMA_CREAM:-1","&4","Magma Lord",
  ["&4Magma Lords&7, towering titans of molten","&7rock. They burn the earth beneath","&7their feet, but cold seeps into","&7their cores and weakens them."],
  {"FIRE_DAMAGE_DEALT":0.25,"FIRE_RESISTANCE":0.3,"EXPLOSION_DAMAGE_DEALT":0.15,"HEALTH_BONUS":5,"FREEZING_RESISTANCE":-0.2,"MOVEMENT_SPEED_BONUS":-0.15})

R("stormborn","TRIDENT:-1","&9","Stormborn",
  ["&9Stormborn&7, children of the tempest sky.","&7They command thunder and wind, striking","&7from above with shocking fury,","&7but the calm of earth unsettles them."],
  {"LIGHTNING_DAMAGE_DEALT":0.2,"RANGED_DAMAGE_DEALT":0.2,"MOVEMENT_SPEED_BONUS":0.15,"JUMP_HEIGHT_MULTIPLIER":0.1,"ARMOR_MULTIPLIER_BONUS":-0.1,"HEALTH_BONUS":-3})

R("tidal_dancer","TROPICAL_FISH:-1","&b","Tidal Dancer",
  ["&bTidal Dancers&7, graceful beings of the","&7ocean currents. They heal with the","&7tide and buff allies, but cannot","&7endure arid lands for long."],
  {"HEALING_BONUS":0.25,"FREEZING_DAMAGE_DEALT":0.15,"FISHING_LUCK":2,"FISHING_SPEED_MULTIPLIER":0.15,"MELEE_DAMAGE_DEALT":-0.1,"FIRE_RESISTANCE":-0.05})

R("glacial","PACKED_ICE:-1","&b","Glacial",
  ["&bGlacials&7, frozen giants from the heart","&7of the ice age. Their bodies radiate","&7an aura of frost, but fire","&7melts their resolve."],
  {"FREEZING_DAMAGE_DEALT":0.3,"FREEZING_RESISTANCE":0.35,"ARMOR_MULTIPLIER_BONUS":0.1,"HEALTH_BONUS":3,"FIRE_RESISTANCE":-0.25,"MOVEMENT_SPEED_BONUS":-0.1})

R("volcanic","OBSIDIAN:-1","&4","Volcanic",
  ["&4Volcanic&7, ancient beings of fire and ash.","&7Their molten hearts grant terrifying","&7power, but cold slows their","&7sluggish magma-blood."],
  {"FIRE_DAMAGE_DEALT":0.2,"EXPLOSION_DAMAGE_DEALT":0.15,"FIRE_RESISTANCE":0.2,"HEALTH_BONUS":4,"FREEZING_RESISTANCE":-0.2,"DODGE_CHANCE":-0.1})

R("dust_wraith","SAND:-1","&e","Dust Wraith",
  ["&eDust Wraiths&7, hollow spirits of the","&7endless desert. They scour foes with","&7grinding sand and move unseen,","&7but water dissolves their forms."],
  {"MAGIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.2,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":-4,"FREEZING_RESISTANCE":-0.1})

R("mistwalker","GLASS_BOTTLE:-1","&7","Mistwalker",
  ["&7Mistwalkers&7, ethereal beings woven from","&7the morning fog. They drift between","&7worlds, but strong light","&7dispels their shadows."],
  {"DODGE_CHANCE":0.2,"MAGIC_DAMAGE_DEALT":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"COOLDOWN_REDUCTION":0.1,"RADIANT_RESISTANCE":-0.1,"HEALTH_BONUS":-3})

R("ashborn","SUSPICIOUS_STEW:-1","&8","Ashborn",
  ["&8Ashborn&7, scorched remnants of a dead","&7world. They wield death-magic of","&7ashes and are immune to burning,","&7but they are withered and frail."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"FIRE_RESISTANCE":0.3,"NECROTIC_RESISTANCE":0.15,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":-5,"HEALING_BONUS":-0.1})

R("cinder_spark","BLAZE_ROD:-1","&6","Cinder Spark",
  ["&6Cinder Sparks&7, tiny but fierce beings","&7of ember and smoke. They dart through","&7battle in a flurry of sparks,","&7but water extinguishes them."],
  {"FIRE_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.2,"CRIT_CHANCE":0.15,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":-5,"FREEZING_RESISTANCE":-0.15})

R("tempest_lord","CONDUIT:-1","&9","Tempest Lord",
  ["&9Tempest Lords&7, mighty rulers of the","&7storm. They call down devastating","&7lightning, but earth binds their fury."],
  {"LIGHTNING_DAMAGE_DEALT":0.25,"FREEZING_DAMAGE_DEALT":0.15,"KNOCKBACK_RESISTANCE":0.2,"ARMOR_MULTIPLIER_BONUS":0.1,"MELEE_DAMAGE_DEALT":-0.1,"DIG_SPEED":-0.1})

R("sky_sovereign","ELYTRA:-1","&f","Sky Sovereign",
  ["&fSky Sovereigns&7, regal beings who dwell","&7above the clouds. They command winds","&7and soar, but the ground","&7is foreign to them."],
  {"RANGED_DAMAGE_DEALT":0.2,"MOVEMENT_SPEED_BONUS":0.15,"FALLING_RESISTANCE":0.3,"CRIT_CHANCE":0.1,"HEALTH_BONUS":-3,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("inferno_touched","NETHERITE_INGOT:-1","&4","Inferno Touched",
  ["&4Inferno Touched&7, mortals branded by","&7the hells. They radiate searing heat","&7and shrug off flame, but cold","&7bites them to the bone."],
  {"FIRE_DAMAGE_DEALT":0.2,"FIRE_RESISTANCE":0.25,"MAGIC_DAMAGE_DEALT":0.1,"COOLDOWN_REDUCTION":0.1,"FREEZING_RESISTANCE":-0.2,"HEALTH_BONUS":-3})

R("void_essence","ENDER_EYE:-1","&5","Void Essence",
  ["&5Void Essences&7, beings of pure nothingness","&7between dimensions. They wield entropy","&7and decay, but radiant light","&7unmakes their being."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"MAGIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.2,"COOLDOWN_REDUCTION":0.15,"RADIANT_RESISTANCE":-0.25,"HEALTH_BONUS":-5})

R("ember_knight","BLAZE_POWDER:-1","&c","Ember Knight",
  ["&cEmber Knights&7, warriors forged in","&7living flame. They fight with","&7fire-wreathed weapons, but ice","&7shatters them."],
  {"MELEE_DAMAGE_DEALT":0.15,"FIRE_DAMAGE_DEALT":0.2,"FIRE_RESISTANCE":0.15,"ARMOR_MULTIPLIER_BONUS":0.05,"FREEZING_RESISTANCE":-0.15})

R("frost_kin","BLUE_ICE:-1","&b","Frost-Kin",
  ["&bFrost-Kin&7, beings of bitter cold.","&7They command freezing winds and their","&7touch numbs all it contacts,","&7but fire melts their resolve."],
  {"FREEZING_DAMAGE_DEALT":0.2,"FREEZING_RESISTANCE":0.25,"ARMOR_MULTIPLIER_BONUS":0.1,"FIRE_RESISTANCE":-0.2,"HEALTH_BONUS":-5})

R("ember_soul","MAGMA_CREAM:-1","&4","Ember Soul",
  ["&4Ember Souls&7, beings of smoldering ash","&7and fading flame. They burn foes","&7with residual heat, but they","&7are slowly fading."],
  {"FIRE_DAMAGE_DEALT":0.15,"MAGIC_DAMAGE_DEALT":0.1,"COOLDOWN_REDUCTION":0.1,"FIRE_RESISTANCE":0.1,"HEALTH_BONUS":-5,"FREEZING_RESISTANCE":-0.1})

# ── BEAST / ANIMAL ──
R("wolf_blooded","SPIDER_EYE:-1","&7","Wolf-Blooded",
  ["&7Wolf-Blooded&7, fierce pack hunters who","&7rare strength and cunning. Their","&7jaws rend armor, but they","&7struggle with ranged combat."],
  {"MELEE_DAMAGE_DEALT":0.15,"UNARMED_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.1,"SPRINT_MOVEMENT_SPEED_BONUS":0.1,"RANGED_DAMAGE_DEALT":-0.1})

R("bear_folk","HONEYCOMB:-1","&6","Bear-Folk",
  ["&6Bear-Folk&7, massive warrior-beasts of","&7unyielding strength. They shrug off","&7wounds and crush foes, but","&7they are slow and clumsy."],
  {"MELEE_DAMAGE_DEALT":0.2,"HEALTH_BONUS":5,"KNOCKBACK_RESISTANCE":0.2,"ARMOR_MULTIPLIER_BONUS":0.1,"MOVEMENT_SPEED_BONUS":-0.15,"DODGE_CHANCE":-0.1})

R("hawk_kin","FEATHER:-1","&e","Hawk-Kin",
  ["&eHawk-Kin&7, sharp-eyed raptor folk who","&7dive upon prey from impossible heights.","&7Their vision is unmatched, but","&7they are light and fragile."],
  {"RANGED_DAMAGE_DEALT":0.2,"CRIT_CHANCE":0.15,"MOVEMENT_SPEED_BONUS":0.1,"FALLING_RESISTANCE":0.25,"HEALTH_BONUS":-4})

R("serpent_blooded","POISONOUS_POTATO:-1","&2","Serpent-Blooded",
  ["&2Serpent-Blooded&7, cold-blooded hunters","&7of the deep jungle. Their venomous","&7bite weakens prey before the","&7killing strike."],
  {"POISON_DAMAGE_DEALT":0.25,"POISON_RESISTANCE":0.3,"MELEE_DAMAGE_DEALT":0.15,"MAGIC_RESISTANCE":-0.1,"HEALTH_BONUS":-5})

R("spider_kin","STRING:-1","&5","Spider-Kin",
  ["&5Spider-Kin&7, eight-limbed stalkers of","&7the dark places. They spin webs of","&7shadow and strike from above,","&7but are frail of body."],
  {"MELEE_DAMAGE_DEALT":0.15,"POISON_DAMAGE_DEALT":0.2,"DODGE_CHANCE":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.1,"HEALTH_BONUS":-3,"RADIANT_RESISTANCE":-0.1})

R("raven_folk","BLACK_DYE:-1","&8","Raven-Folk",
  ["&8Raven-Folk&7, cunning omens of death","&7who speak with fallen spirits.","&7They wield dark magic, but","&7are brittle in prolonged combat."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"MAGIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.1,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-4,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("fox_blooded","SWEET_BERRIES:-1","&6","Fox-Blooded",
  ["&6Fox-Blooded&7, cunning tricksters of","&7the wild. Their quick wits and","&7quicker feet carry them through","&7danger."],
  {"CRIT_CHANCE":0.15,"DODGE_CHANCE":0.15,"MOVEMENT_SPEED_BONUS":0.1,"LUCK_BONUS":0.1,"HEALTH_BONUS":-3,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("stag_folk","GRASS:-1","&2","Stag-Folk",
  ["&2Stag-Folk&7, noble beasts of the ancient","&7forest. They charge with devastating","&7horns, but they avoid","&7the violence of war."],
  {"MELEE_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.15,"FARMING_EXP_GAIN":0.1,"WOODCUTTING_EXP_GAIN":0.1,"HEAVY_WEAPONS_EXP_GAIN":-0.1})

R("shark_kin","COD:-1","&3","Shark-Kin",
  ["&3Shark-Kin&7, relentless ocean predators.","&7They tear through foes in water","&7and on land, but they","&7are clumsy on land."],
  {"MELEE_DAMAGE_DEALT":0.2,"MOVEMENT_SPEED_BONUS":0.1,"BLEED_RESISTANCE":0.25,"CRIT_CHANCE":0.1,"SNEAK_MOVEMENT_SPEED_BONUS":-0.15})

R("lion_folk","GOLDEN_CARROT:-1","&e","Lion-Folk",
  ["&eLion-Folk&7, regal kings of the savage","&7savanna. Their roar stuns foes and","&7their claws rend armor, but","&7they fall to their own hubris."],
  {"MELEE_DAMAGE_DEALT":0.2,"UNARMED_DAMAGE_DEALT":0.15,"KNOCKBACK_RESISTANCE":0.1,"CRIT_DAMAGE":0.1,"MAGIC_RESISTANCE":-0.1,"DODGE_CHANCE":-0.05})

R("owlkin","CLOCK:-1","&d","Owlkin",
  ["&dOwlkin&7, silent watchers of the night.","&7Their uncanny vision guides allies","&7through darkness, but daylight","&7weakens their resolve."],
  {"RANGED_DAMAGE_DEALT":0.15,"CRIT_CHANCE":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"GLOBAL_EXP_GAIN":0.1,"MELEE_DAMAGE_DEALT":-0.1})

R("raptor_kin","MUSHROOM_STEW:-1","&2","Raptor-Kin",
  ["&2Raptor-Kin&7, swift and deadly hunters","&7of the primordial wilds. They chase","&7down prey with tireless speed."],
  {"MELEE_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.2,"CRIT_CHANCE":0.1,"SPRINT_MOVEMENT_SPEED_BONUS":0.1,"ARMOR_MULTIPLIER_BONUS":-0.1,"HEALTH_BONUS":-3})

R("boar_folk","RAW_PORKCHOP:-1","&6","Boar-Folk",
  ["&6Boar-Folk&7, tusked bruisers of the","&7thick forest. They charge headlong","&7into battle, goring foes on","&7their massive tusks."],
  {"MELEE_DAMAGE_DEALT":0.2,"KNOCKBACK_RESISTANCE":0.15,"HEALTH_BONUS":5,"MOVEMENT_SPEED_BONUS":-0.15,"MAGIC_RESISTANCE":-0.1})

R("bat_folk","BAT_SPAWN_EGG:-1","&8","Bat-Folk",
  ["&8Bat-Folk&7, agile creatures of the deep","&7caves. They navigate by sound and","&7swarm foes, but they are","&7frail in direct combat."],
  {"DODGE_CHANCE":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"MINING_EXP_GAIN":0.1,"DIG_SPEED":0.1,"HEALTH_BONUS":-4})

R("lupine_hunter","LEATHER:-1","&7","Lupine Hunter",
  ["&7Lupine Hunters&7, lone wolves of the","&7frozen tundra. They stalk prey","&7with deadly patience and strike","&7when the moment is perfect."],
  {"RANGED_DAMAGE_DEALT":0.15,"CRIT_CHANCE":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.1,"FISHING_LUCK":1,"HEALTH_BONUS":-3,"TOTAL_HEAVY_ARMOR":-0.1})

R("serpent_sages","FERMENTED_SPIDER_EYE:-1","&2","Serpent Sage",
  ["&2Serpent Sages&7, wise snake-folk who","&7master alchemy and poison craft.","&7Their venom enhances every brew."],
  {"ALCHEMY_EXP_GAIN":0.2,"POISON_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.1,"MELEE_DAMAGE_DEALT":-0.1})

# ── UNDEAD / SPECTRAL ──
R("lich","WITHER_SKELETON_SKULL:-1","&5","Lich",
  ["&5Liches&7, ancient sorcerers who cheated","&7death. They wield devastating necromancy","&7and are immune to poison, but","&7holy light unmakes them."],
  {"NECROTIC_DAMAGE_DEALT":0.25,"MAGIC_DAMAGE_DEALT":0.2,"COOLDOWN_REDUCTION":0.2,"POISON_RESISTANCE":0.5,"RADIANT_RESISTANCE":-0.3,"HEALTH_BONUS":-5})

R("banshee","SOUL_SAND:-1","&f","Banshee",
  ["&fBanshees&7, shrieking spirits of grief.","&7Their wails shatter sanity and their","&7icy touch freezes blood, but","&7radiant energy burns them."],
  {"FREEZING_DAMAGE_DEALT":0.2,"NECROTIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.2,"COOLDOWN_REDUCTION":0.15,"RADIANT_RESISTANCE":-0.25,"HEALTH_BONUS":-6})

R("revenant","BONE_BLOCK:-1","&8","Revenant",
  ["&8Revenants&7, undead warriors consumed by","&7vengeance. They cannot be stopped by","&7death and fight relentlessly,","&7but their bodies crumble slowly."],
  {"MELEE_DAMAGE_DEALT":0.15,"NECROTIC_DAMAGE_DEALT":0.15,"KNOCKBACK_RESISTANCE":0.2,"HEALTH_BONUS":5,"HEALING_BONUS":-0.2})

R("phantom","PHANTOM_MEMBRANE:-1","&b","Phantom",
  ["&bPhantoms&7, sleepless spirits that haunt","&7the waking world. They slip through","&7matter, but they are","&7ephemeral and fragile."],
  {"MAGIC_DAMAGE_DEALT":0.2,"DODGE_CHANCE":0.25,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-6,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("shade","BLACK_CANDLE:-1","&8","Shade",
  ["&8Shades&7, darkness given form. They hide","&7in shadows and strike when least","&7expected, draining warmth from","&7all they touch."],
  {"MELEE_DAMAGE_DEALT":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"DODGE_CHANCE":0.15,"NECROTIC_DAMAGE_DEALT":0.1,"RADIANT_RESISTANCE":-0.15,"HEALTH_BONUS":-3})

R("specter","GHOSTLY_GUNPOWDER:-1","&7","Specter",
  ["&7Specters&7, restless spirits bound to","&7the material plane. They pass through","&7walls, but sunlight weakens them."],
  {"FREEZING_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.2,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"COOLDOWN_REDUCTION":0.1,"RADIANT_RESISTANCE":-0.2,"HEALTH_BONUS":-4})

R("poltergeist","ANVIL:-1","&d","Poltergeist",
  ["&dPoltergeists&7, chaotic spirits of rage","&7and mischief. They hurl objects with","&7telekinetic force, but cannot","&7grasp solid weapons."],
  {"MAGIC_DAMAGE_DEALT":0.2,"EXPLOSION_DAMAGE_DEALT":0.15,"KNOCKBACK_RESISTANCE":0.15,"COOLDOWN_REDUCTION":0.1,"MELEE_DAMAGE_DEALT":-0.1,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("ghost_kin","WHITE_STAINED_GLASS:-1","&f","Ghost-Kin",
  ["&fGhost-Kin&7, translucent beings caught","&7between life and death. They drift","&7through attacks and haunt foes."],
  {"MAGIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.2,"FREEZING_DAMAGE_DEALT":0.1,"NECROTIC_RESISTANCE":0.1,"HEALTH_BONUS":-5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("zombie_forged","ROTTEN_FLESH:-1","&2","Zombie-Forged",
  ["&2Zombie-Forged&7, reanimated corpses fused","&7with necromantic magic. They feel no","&7pain, but their bodies slowly","&7decay with each battle."],
  {"MELEE_DAMAGE_DEALT":0.15,"NECROTIC_RESISTANCE":0.2,"KNOCKBACK_RESISTANCE":0.1,"HEALTH_BONUS":5,"HEALING_BONUS":-0.15,"MOVEMENT_SPEED_BONUS":-0.1})

# ── DIVINE / CELESTIAL ──
R("seraph","GOLDEN_APPLE:-1","&e","Seraph",
  ["&eSeraphs&7, six-winged angels of the","&7highest heaven. Their radiance destroys","&7evil and heals the wounded, but","&7they burn in the presence of sin."],
  {"RADIANT_DAMAGE_DEALT":0.25,"HEALING_BONUS":0.25,"RADIANT_RESISTANCE":0.15,"MAGIC_DAMAGE_DEALT":0.1,"NECROTIC_RESISTANCE":-0.2,"FOOD_BONUS_SPOILED":-1})

R("archon","LIGHT_BLUE_DYE:-1","&b","Archon",
  ["&bArchons&7, celestial commanders of divine","&7justice. They smite the wicked with","&7holy power, but cannot tolerate","&7dark magic."],
  {"RADIANT_DAMAGE_DEALT":0.2,"ARMOR_MULTIPLIER_BONUS":0.15,"HEALING_BONUS":0.15,"KNOCKBACK_RESISTANCE":0.1,"NECROTIC_DAMAGE_DEALT":-0.15})

R("demigod","NETHERITE_INGOT:-1","&6","Demigod",
  ["&6Demigods&7, mortal offspring of the","&7divine. Their godly blood grants","&7terrifying power, but their mortal","&7flesh cannot fully contain it."],
  {"DAMAGE_DEALT":0.15,"ARMOR_MULTIPLIER_BONUS":0.15,"DAMAGE_RESISTANCE":0.1,"HEALTH_BONUS":5,"GLOBAL_EXP_GAIN":-0.15})

R("solar_angel","SUNFLOWER:-1","&e","Solar Angel",
  ["&eSolar Angels&7, beings of pure sunlight.","&7Their radiance burns the unholy and","&7restores the wounded, but darkness","&7devours their strength."],
  {"RADIANT_DAMAGE_DEALT":0.25,"HEALING_BONUS":0.2,"FIRE_DAMAGE_DEALT":0.15,"NECROTIC_RESISTANCE":-0.2,"HEALTH_BONUS":-5})

R("lunar_kin","CLOCK:-1","&9","Lunar Kin",
  ["&9Lunar Kin&7, moon-touched beings of the","&7night sky. They grow stronger under","&7the moon and wield silver magic,","&7but sunlight dims their power."],
  {"MAGIC_DAMAGE_DEALT":0.2,"FREEZING_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.1,"FIRE_DAMAGE_DEALT":-0.1})

R("starborn","NETHER_STAR:-1","&e","Starborn",
  ["&eStarborn&7, beings of cosmic light who","&7fell from the heavens. They channel","&7the power of dying stars and","&7weave celestial magic."],
  {"MAGIC_DAMAGE_DEALT":0.2,"RADIANT_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.15,"CRIT_DAMAGE":0.1,"HEALTH_BONUS":-4})

R("cherub","POPPY:-1","&d","Cherub",
  ["&dCherubs&7, infant-like celestial spirits","&7of innocence and healing. They mend","&7wounds with a touch, but are","&7utterly helpless in melee."],
  {"HEALING_BONUS":0.3,"RADIANT_DAMAGE_DEALT":0.15,"RADIANT_RESISTANCE":0.2,"MELEE_DAMAGE_DEALT":-0.15,"HEALTH_BONUS":-4})

R("aasimar","GLOW_BERRIES:-1","&e","Aasimar",
  ["&eAasimars&7, mortal-born with divine blood.","&7They channel holy power instinctively,","&7but their mortal side holds them back."],
  {"RADIANT_DAMAGE_DEALT":0.15,"HEALING_BONUS":0.15,"MAGIC_RESISTANCE":0.1,"ARMOR_MULTIPLIER_BONUS":0.1,"NECROTIC_DAMAGE_DEALT":-0.1})

# ── DEMONIC / ABYSSAL ──
R("imp","BLAZE_POWDER:-1","&4","Imp",
  ["&4Imps&7, tiny but vicious servants of","&7the hells. They dart about causing","&7havoc and hurling fire, but are","&7easily crushed underfoot."],
  {"FIRE_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.2,"MOVEMENT_SPEED_BONUS":0.15,"HEALTH_BONUS":-6,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("cambion","NETHER_WART:-1","&4","Cambion",
  ["&4Cambions&7, half-fiend mortals of dark","&7ambition. They wield both martial and","&7arcane prowess, but their fiendish","&7blood repels the divine."],
  {"MELEE_DAMAGE_DEALT":0.15,"MAGIC_DAMAGE_DEALT":0.15,"FIRE_DAMAGE_DEALT":0.1,"COOLDOWN_REDUCTION":0.1,"RADIANT_RESISTANCE":-0.15})

R("pit_fiend","CHAIN_COMMAND_BLOCK:-1","&4","Pit Fiend",
  ["&4Pit Fiends&7, hulking brutes of the","&7abyss. They crush foes with massive","&7fists, but they are slow and","&7dim-witted."],
  {"MELEE_DAMAGE_DEALT":0.25,"KNOCKBACK_RESISTANCE":0.2,"HEALTH_BONUS":10,"MOVEMENT_SPEED_BONUS":-0.2,"MAGIC_DAMAGE_DEALT":-0.1})

R("balor","FIRE_CHARGE:-1","&4","Balor",
  ["&4Balors&7, terrifying lords of the","&7burning hells. Their whip of fire","&7shakes the earth, but they","&7are massive targets."],
  {"FIRE_DAMAGE_DEALT":0.25,"MELEE_DAMAGE_DEALT":0.2,"EXPLOSION_DAMAGE_DEALT":0.15,"HEALTH_BONUS":10,"MOVEMENT_SPEED_BONUS":-0.15,"DODGE_CHANCE":-0.1})

R("tiefling","CRIMSON_FUNGUS:-1","&c","Tiefling",
  ["&cTieflings&7, mortal-descended of fiends.","&7They wield dark magic and have","&7unnatural charisma, but are","&7shunned by all."],
  {"MAGIC_DAMAGE_DEALT":0.15,"FIRE_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.1,"LUCK_BONUS":0.1,"RADIANT_RESISTANCE":-0.15})

R("shadow_demon","SHADOW_DYE:-1","&8","Shadow Demon",
  ["&8Shadow Demons&7, beings of pure darkness","&7between planes. They slip through","&7shadows, but light unmakes them."],
  {"MELEE_DAMAGE_DEALT":0.2,"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"DODGE_CHANCE":0.15,"NECROTIC_DAMAGE_DEALT":0.1,"RADIANT_RESISTANCE":-0.15,"HEALTH_BONUS":-3})

R("nightmare","BLACK_HORSE_ARMOR:-1","&5","Nightmare",
  ["&5Nightmares&7, steeds of the burning hells","&7gained sentience. They spread fear","&7and their hooves ignite, but","&7cold weakens them."],
  {"FIRE_DAMAGE_DEALT":0.2,"MOVEMENT_SPEED_BONUS":0.15,"SPRINT_MOVEMENT_SPEED_BONUS":0.15,"CRIT_CHANCE":0.1,"FREEZING_RESISTANCE":-0.15,"HEALTH_BONUS":-3})

R("void_fiend","ENDER_PEARL:-1","&5","Void Fiend",
  ["&5Void Fiends&7, entities from beyond the","&7stars. They warp reality and drain","&7life, but divine light destroys them."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"MAGIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.2,"RADIANT_RESISTANCE":-0.2,"HEALTH_BONUS":-5})

# ── NATURE / FEY ──
R("sprite","DANDELION:-1","&a","Sprite",
  ["&aSprites&7, tiny fae folk of mischief","&7and wonder. They weave enchantments,","&7but their tiny bodies are","&7easily squashed."],
  {"MAGIC_DAMAGE_DEALT":0.15,"ENCHANTING_EXP_GAIN":0.2,"COOLDOWN_REDUCTION":0.15,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-6,"SCALE":-0.2})

R("pixie","OXEYE_DAISY:-1","&d","Pixie",
  ["&dPixies&7, radiant fae of joy and wonder.","&7They bless allies with luck and heal","&7wounds, but their frames","&7are laughably weak."],
  {"HEALING_BONUS":0.25,"LUCK_BONUS":0.15,"MAGIC_DAMAGE_DEALT":0.15,"HEALTH_BONUS":-7,"SCALE":-0.25})

R("centaur","BOW:-1","&6","Centaur",
  ["&6Centaurs&7, half-horse warriors of the","&7open plains. They charge with force","&7and fire arrows on the move,","&7but they tire quickly."],
  {"RANGED_DAMAGE_DEALT":0.15,"MELEE_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.1,"SPRINT_MOVEMENT_SPEED_BONUS":0.1,"SNEAK_MOVEMENT_SPEED_BONUS":-0.1})

R("sylph","WHITE_WOOL:-1","&f","Sylph",
  ["&fSylphs&7, air fae of the highest peaks.","&7They dance on the wind and command","&7breezes, but are fragile","&7in close combat."],
  {"MOVEMENT_SPEED_BONUS":0.2,"MAGIC_DAMAGE_DEALT":0.15,"FALLING_RESISTANCE":0.2,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-4,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("gnome","RED_MUSHROOM:-1","&a","Gnome",
  ["&aGnomes&7, brilliant tinkerers of the","&7underground. They craft ingenious","&7devices, but their small stature","&7limits them."],
  {"ENCHANTING_EXP_GAIN":0.25,"MINING_EXP_GAIN":0.2,"COOLDOWN_REDUCTION":0.15,"LUCK_BONUS":0.1,"HEALTH_BONUS":-4,"SCALE":-0.1})

R("leshy","AZALEA:-1","&2","Leshy",
  ["&2Leshys&7, ancient forest spirits who","&7embody the wild itself. They command","&7plants and beasts, but civilization","&7withers their strength."],
  {"HEALING_BONUS":0.2,"POISON_RESISTANCE":0.2,"FARMING_EXP_GAIN":0.15,"WOODCUTTING_EXP_GAIN":0.1,"MELEE_DAMAGE_DEALT":-0.1})

R("mushroom_folk","RED_MUSHROOM_BLOCK:-1","&c","Mushroom Folk",
  ["&cMushroom Folk&7, spore-spreading creatures","&7of the deep caves. They heal with","&7fungal magic, but fire","&7destroys them."],
  {"HEALING_BONUS":0.2,"POISON_RESISTANCE":0.25,"ALCHEMY_EXP_GAIN":0.15,"FARMING_EXP_GAIN":0.1,"FIRE_RESISTANCE":-0.15})

R("treant_sprout","OAK_SAPLING:-1","&2","Treant Sprout",
  ["&2Treant Sprouts&7, young tree spirits","&7just awakening. They grow stronger","&7over time, but are still","&7small and fragile."],
  {"HEALING_BONUS":0.15,"POISON_RESISTANCE":0.15,"FARMING_EXP_GAIN":0.1,"WOODCUTTING_EXP_GAIN":0.1,"ARMOR_MULTIPLIER_BONUS":0.05,"HEALTH_BONUS":-3})

R("faun","WHEAT:-1","&6","Faun",
  ["&6Fauns&7, gentle goat-children of the","&7meadow. They dance and play music","&7that heals and inspires, but","&7are terrified of warfare."],
  {"HEALING_BONUS":0.2,"LUCK_BONUS":0.15,"FARMING_EXP_GAIN":0.1,"GLOBAL_EXP_GAIN":0.1,"MELEE_DAMAGE_DEALT":-0.1})

# ── AQUATIC ──
R("merfolk","HEART_OF_THE_SEA:-1","&b","Merfolk",
  ["&bMerfolk&7, beautiful beings of the deep","&7sea. They wield the power of tides","&7and heal allies, but the dry","&7land saps their strength."],
  {"HEALING_BONUS":0.25,"FREEZING_DAMAGE_DEALT":0.15,"FISHING_LUCK":2,"FISHING_SPEED_MULTIPLIER":0.15,"MOVEMENT_SPEED_BONUS":-0.1})

R("sea_elf","PRISMARINE_CRYSTALS:-1","&3","Sea Elf",
  ["&3Sea Elves&7, ancient guardians of the","&7ocean depths. They command water","&7magic, but weaken far from the sea."],
  {"FREEZING_DAMAGE_DEALT":0.2,"HEALING_BONUS":0.15,"FISHING_LUCK":2,"MAGIC_RESISTANCE":0.1,"FIRE_DAMAGE_DEALT":-0.1})

R("kelpie","KELP:-1","&2","Kelpie",
  ["&2Kelpies&7, shape-shifting water spirits","&7that drown the unwary. They lure","&7victims with beauty and drag them","&7to watery graves."],
  {"FREEZING_DAMAGE_DEALT":0.15,"POISON_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.2,"MOVEMENT_SPEED_BONUS":0.1,"FIRE_RESISTANCE":-0.1})

R("sahuagin","TROPICAL_FISH_BUCKET:-1","&2","Sahuagin",
  ["&2Sahuagin&7, savage shark-warriors of the","&7abyssal depths. They hunt in packs","&7and their bite injects venom,","&7but are clumsy on land."],
  {"MELEE_DAMAGE_DEALT":0.2,"POISON_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.1,"BLEED_RESISTANCE":0.15,"FIRE_RESISTANCE":-0.15})

R("triton","CONDUIT_POWER_EFFECT:-1","&b","Triton",
  ["&bTritons&7, noble warriors of the deep","&7who protect the oceans. They wield","&7tridents of lightning and command","&7the tides in battle."],
  {"MELEE_DAMAGE_DEALT":0.15,"LIGHTNING_DAMAGE_DEALT":0.15,"ARMOR_MULTIPLIER_BONUS":0.1,"FISHING_LUCK":1,"FIRE_RESISTANCE":-0.1})

R("deep_one","PRISMARINE_SHARD:-1","&5","Deep One",
  ["&5Deep Ones&7, ancient horrors from the","&7ocean trenches. They wield dark","&7aquatic magic, but they weaken","&7in sunlight."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"MAGIC_DAMAGE_DEALT":0.15,"FREEZING_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.1,"RADIANT_RESISTANCE":-0.15})

R("abyssal_serpent","PUFFERFISH:-1","&3","Abyssal Serpent",
  ["&3Abyssal Serpents&7, titanic sea snakes","&7that crush ships in their coils.","&7Their venom is legendary, but","&7they are vulnerable to fire."],
  {"POISON_DAMAGE_DEALT":0.25,"MELEE_DAMAGE_DEALT":0.2,"FREEZING_DAMAGE_DEALT":0.15,"FIRE_RESISTANCE":-0.2,"MOVEMENT_SPEED_BONUS":-0.1})

R("pearl_mermaid","HEART_OF_THE_SEA:-1","&b","Pearl Mermaid",
  ["&bPearl Mermaids&7, elegant sea-dwellers","&7with shells of pearl. Their song","&7heals and their touch mends,","&7but dry land withers their tails."],
  {"HEALING_BONUS":0.2,"MAGIC_DAMAGE_DEALT":0.15,"FISHING_LUCK":2,"MOVEMENT_SPEED_BONUS":-0.1,"MELEE_DAMAGE_DEALT":-0.1})

# ── CONSTRUCT / ARTIFICIAL ──
R("automaton","IRON_BLOCK:-1","&7","Automaton",
  ["&7Automatons&7, clockwork constructs of brass","&7and steel. They feel no pain and never","&7tire, but their rigid forms are","&7slow and cannot heal naturally."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"DAMAGE_RESISTANCE":0.15,"DIG_SPEED":0.1,"HEALTH_BONUS":3,"HEALING_BONUS":-0.2,"MOVEMENT_SPEED_BONUS":-0.15})

R("warforged","ANVIL:-1","&8","Warforged",
  ["&8Warforged&7, living weapons forged in the","&7fires of war. They are built to fight","&7and nothing else, but lack","&7the creativity of living beings."],
  {"MELEE_DAMAGE_DEALT":0.2,"ARMOR_MULTIPLIER_BONUS":0.15,"KNOCKBACK_RESISTANCE":0.15,"HEALTH_BONUS":5,"GLOBAL_EXP_GAIN":-0.2,"HEALING_BONUS":-0.15})

R("clockwork","CLOCK:-1","&6","Clockwork",
  ["&6Clockwork&7, intricate mechanical beings","&7of gears and springs. They are","&7precision-engineered for speed,","&7but need constant maintenance."],
  {"DIG_SPEED":0.15,"MINING_EXP_GAIN":0.15,"COOLDOWN_REDUCTION":0.1,"CRAFTING_TIME_REDUCTION":0.1,"ARMOR_MULTIPLIER_BONUS":-0.1,"HEALTH_BONUS":-5})

R("crystal_golem","DIAMOND_BLOCK:-1","&b","Crystal Golem",
  ["&bCrystal Golems&7, beings of living gemstone.","&7Their crystalline bodies refract","&7magic, but they shatter under","&7repeated blows."],
  {"MAGIC_RESISTANCE":0.25,"ARMOR_MULTIPLIER_BONUS":0.2,"DAMAGE_RESISTANCE":0.1,"HEALTH_BONUS":5,"MOVEMENT_SPEED_BONUS":-0.15,"HEALING_BONUS":-0.1})

R("construct","REDSTONE_BLOCK:-1","&4","Construct",
  ["&4Constructs&7, artificial beings animated","&7by magic and redstone. They obey","&7orders without question but lack","&7self-preservation."],
  {"DAMAGE_RESISTANCE":0.15,"KNOCKBACK_RESISTANCE":0.15,"ARMOR_MULTIPLIER_BONUS":0.1,"DIG_SPEED":0.1,"GLOBAL_EXP_GAIN":-0.2,"HEALTH_BONUS":-5})

R("soulforged","SOUL_SAND:-1","&8","Soulforged",
  ["&8Soulforged&7, constructs powered by trapped","&7souls. They wield necrotic energy and","&7drain life, but their bound","&7souls torment them."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"ARMOR_MULTIPLIER_BONUS":0.15,"KNOCKBACK_RESISTANCE":0.1,"COOLDOWN_REDUCTION":0.1,"HEALING_BONUS":-0.15,"RADIANT_RESISTANCE":-0.1})

# ── GIANT / KIN ──
R("ogre","IRON_AXE:-1","&6","Ogre",
  ["&6Ogres&7, hulking brute-kin of the","&7wastelands. They smash through","&7anything, but their tiny brains","&7make them easy prey."],
  {"MELEE_DAMAGE_DEALT":0.2,"KNOCKBACK_RESISTANCE":0.15,"HEALTH_BONUS":8,"MAGIC_RESISTANCE":-0.2,"MOVEMENT_SPEED_BONUS":-0.15})

R("troll","VINE_WEB:-1","&2","Troll",
  ["&2Trolls&7, massive regenerating brutes","&7of the frozen mountains. Their flesh","&7regenerates, but fire and acid","&7are their bane."],
  {"MELEE_DAMAGE_DEALT":0.15,"HEALING_BONUS":0.2,"HEALTH_BONUS":10,"FREEZING_RESISTANCE":0.2,"FIRE_RESISTANCE":-0.25,"MOVEMENT_SPEED_BONUS":-0.15})

R("jotun","BLUE_ICE:-1","&9","Jotun",
  ["&9Jotuns&7, frost giants of primordial","&7age. They wield absolute cold and","&7their steps cause earthquakes,","&7but fire melts them."],
  {"FREEZING_DAMAGE_DEALT":0.2,"FREEZING_RESISTANCE":0.25,"HEALTH_BONUS":10,"FIRE_RESISTANCE":-0.3,"MOVEMENT_SPEED_BONUS":-0.15})

R("cyclops","SPYGLASS:-1","&e","Cyclops",
  ["&eCyclopes&7, one-eyed giants of incredible","&7strength. Their fists crush stone,","&7but they are clumsy and","&7easily flanked."],
  {"MELEE_DAMAGE_DEALT":0.25,"BLUDGEONING_DAMAGE_DEALT":0.2,"HEALTH_BONUS":8,"DODGE_CHANCE":-0.15,"MOVEMENT_SPEED_BONUS":-0.1})

R("firbolg","POPPY:-1","&d","Firbolg",
  ["&dFirbolgs&7, gentle giant-kin of the deep","&7forest. They protect nature with","&7druidic magic, but distrust outsiders."],
  {"HEALING_BONUS":0.15,"POISON_RESISTANCE":0.15,"FARMING_EXP_GAIN":0.1,"HEALTH_BONUS":10,"MELEE_DAMAGE_DEALT":-0.1})

R("goliath","HEAVY_WEIGHTED_PRESSURE_PLATE:-1","&7","Goliath",
  ["&7Goliaths&7, towering warriors who live","&7for the challenge. They seek the","&7strongest foes and fight with","&7unmatched determination."],
  {"MELEE_DAMAGE_DEALT":0.2,"KNOCKBACK_RESISTANCE":0.15,"HEALTH_BONUS":8,"ARMOR_MULTIPLIER_BONUS":0.1,"MAGIC_RESISTANCE":-0.15,"SNEAK_MOVEMENT_SPEED_BONUS":-0.1})

R("half_giant","STONE_BRICKS:-1","&6","Half-Giant",
  ["&6Half-Giants&7, mortals with giant blood.","&7They are stronger than any human","&7and nearly impossible to push over,","&7but they are clumsy and slow."],
  {"MELEE_DAMAGE_DEALT":0.15,"KNOCKBACK_RESISTANCE":0.2,"HEALTH_BONUS":5,"MOVEMENT_SPEED_BONUS":-0.1,"DODGE_CHANCE":-0.1})

R("verdant_giant","OAK_LOG:-1","&2","Verdant Giant",
  ["&2Verdant Giants&7, living mountains of","&7earth and vegetation. They command","&7the earth itself, but they","&7decay without nature."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"DAMAGE_RESISTANCE":0.15,"POISON_RESISTANCE":0.2,"HEALTH_BONUS":5,"MOVEMENT_SPEED_BONUS":-0.2,"DODGE_CHANCE":-0.1})

R("stone_warden","DEEPSLATE:-1","&8","Stone Warden",
  ["&8Stone Wardens&7, ancient guardians carved","&7from living rock. They protect sacred","&7places and never tire, but","&7are slow and unyielding."],
  {"ARMOR_MULTIPLIER_BONUS":0.25,"KNOCKBACK_RESISTANCE":0.2,"DAMAGE_RESISTANCE":0.1,"HEALTH_BONUS":5,"MOVEMENT_SPEED_BONUS":-0.2,"DODGE_CHANCE":-0.1})

# ── EXOTIC / PLANAR ──
R("astral","END_CRYSTAL:-1","&d","Astral",
  ["&dAstrals&7, beings of pure thought in","&7the spaces between stars. They wield","&7cosmic power, but are alien to","&7the material world."],
  {"MAGIC_DAMAGE_DEALT":0.2,"COOLDOWN_REDUCTION":0.15,"CRIT_DAMAGE":0.15,"LUCK_BONUS":0.1,"HEALTH_BONUS":-5})

R("void_touched","ENDER_EYE:-1","&5","Void-Touched",
  ["&5Void-Touched&7, mortals who gazed into","&7the void and were forever changed.","&7They wield entropy and shadow,","&7but the void whispers madness."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"MAGIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.2,"RADIANT_RESISTANCE":-0.2,"HEALTH_BONUS":-5})

R("ethereal","LIGHT_GRAY_STAINED_GLASS:-1","&7","Ethereal",
  ["&7Ethereals&7, beings that exist partially","&7in another dimension. They phase","&7through attacks and deal strange","&7otherworldly damage."],
  {"DODGE_CHANCE":0.2,"MAGIC_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.1,"MOVEMENT_SPEED_BONUS":0.1,"HEALTH_BONUS":-5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("planar","END_PORTAL_FRAME:-1","&5","Planar",
  ["&5Planar&7, beings from other dimensions","&7who have crossed into this world.","&7They wield reality-warping magic,","&7but the material plane weakens them."],
  {"MAGIC_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.15,"DODGE_CHANCE":0.1,"CRIT_DAMAGE":0.1,"ARMOR_MULTIPLIER_BONUS":-0.1,"HEALTH_BONUS":-5})

R("chrono","WATCH:-1","&e","Chrono",
  ["&eChronos&7, beings who exist outside of","&7time. They perceive all moments","&7simultaneously and slow time,","&7but they age rapidly."],
  {"COOLDOWN_REDUCTION":0.2,"MAGIC_DAMAGE_DEALT":0.15,"CRIT_CHANCE":0.15,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("rune_carved","ANCIENT_DEBRIS:-1","&6","Rune-Carved",
  ["&6Rune-Carved&7, beings inscribed with","&7ancient power symbols. Each rune grants","&7immense power, but the inscriptions","&7burn their flesh."],
  {"MAGIC_DAMAGE_DEALT":0.15,"ENCHANTING_EXP_GAIN":0.15,"COOLDOWN_REDUCTION":0.1,"CRIT_DAMAGE":0.1,"HEALTH_BONUS":-4,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("soul_echo","SOUL_LANTERN:-1","&8","Soul Echo",
  ["&8Soul Echoes&7, reflections of the dead","&7trapped between worlds. They drain","&7life and wield necrotic magic,","&7but are barely tangible."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"DODGE_CHANCE":0.15,"COOLDOWN_REDUCTION":0.1,"SNEAK_MOVEMENT_SPEED_BONUS":0.1,"RADIANT_RESISTANCE":-0.15,"HEALTH_BONUS":-4})

R("dream_walker","COCOA_BEANS:-1","&d","Dream Walker",
  ["&dDream Walkers&7, beings who traverse","&7the realm of dreams. They wield","&7illusory magic and blur the line","&7between reality and nightmare."],
  {"MAGIC_DAMAGE_DEALT":0.2,"COOLDOWN_REDUCTION":0.15,"CRIT_CHANCE":0.1,"SNEAK_MOVEMENT_SPEED_BONUS":0.1,"HEALTH_BONUS":-4,"MELEE_DAMAGE_DEALT":-0.1})

R("aether_born","LIGHT_GRAY_DYE:-1","&f","Aether-Born",
  ["&fAether-Born&7, beings of pure celestial","&7energy from the highest heavens.","&7They channel starlight and cosmic","&7power."],
  {"MAGIC_DAMAGE_DEALT":0.2,"RADIANT_DAMAGE_DEALT":0.15,"CRIT_DAMAGE":0.1,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":-5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("null_kin","BARRIER:-1","&8","Null-Kin",
  ["&8Null-Kin&7, beings of absolute nothing.","&7They erase existence with their touch","&7and exist as voids, but they","&7are the weakest of all races."],
  {"NECROTIC_DAMAGE_DEALT":0.25,"DODGE_CHANCE":0.2,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-10,"ARMOR_MULTIPLIER_BONUS":-0.2})

# ── ADDITIONAL REACH 200 ──
R("sand_wraith","SANDSTONE:-1","&e","Sand Wraith",
  ["&eSand Wraiths&7, desert spirits of","&7scorching wind. They blind foes","&7with sand and strike when the","&7storm obscures vision."],
  {"MAGIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.1,"FIRE_RESISTANCE":0.1,"FREEZING_RESISTANCE":-0.1,"HEALTH_BONUS":-3})

R("iron_bound","IRON_BLOCK:-1","&7","Iron-Bound",
  ["&7Iron-Bound&7, mortals fused with iron","&7through ancient rituals. Their bodies","&7are near-invulnerable but they","&7cannot move quickly."],
  {"ARMOR_MULTIPLIER_BONUS":0.25,"DAMAGE_RESISTANCE":0.2,"KNOCKBACK_RESISTANCE":0.2,"MOVEMENT_SPEED_BONUS":-0.25,"DODGE_CHANCE":-0.15})

R("blood_mage","REDSTONE:-1","&c","Blood Mage",
  ["&cBlood Mages&7, sorcerers who fuel their","&7spells with their own life force.","&7Their power is immense but their","&7bodies are weakened."],
  {"MAGIC_DAMAGE_DEALT":0.25,"COOLDOWN_REDUCTION":0.2,"NECROTIC_DAMAGE_DEALT":0.15,"HEALTH_BONUS":-8,"HEALING_BONUS":-0.15})

R("storm_caller","CONDUIT:-1","&9","Storm Caller",
  ["&9Storm Callers&7, mortals gifted with","&7the fury of the tempest. They call","&7lightning and wind to their aid,","&7but calm stillness unsettles them."],
  {"LIGHTNING_DAMAGE_DEALT":0.2,"RANGED_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.1,"CRIT_CHANCE":0.1,"HEALTH_BONUS":-5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("crystal_shard","AMETHYST_SHARD:-1","&d","Crystal Shard",
  ["&dCrystal Shards&7, fragments of a shattered","&7magical crystal. They refract magic","&7and store power, but they","&7are tiny and fragile."],
  {"MAGIC_DAMAGE_DEALT":0.15,"ENCHANTING_EXP_GAIN":0.15,"LUCK_BONUS":0.1,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":-6,"SCALE":-0.15})

R("twilight_elf","CRYING_OBSIDIAN:-1","&5","Twilight Elf",
  ["&5Twilight Elves&7, drow who have stepped","&7out of the darkness. They wield both","&7light and shadow, balancing the two."],
  {"MAGIC_DAMAGE_DEALT":0.15,"MELEE_DAMAGE_DEALT":0.15,"ENCHANTING_EXP_GAIN":0.1,"CRIT_CHANCE":0.1,"HEALTH_BONUS":-3})

R("dust_djinn","SAND:-1","&e","Dust Djinn",
  ["&eDust Djinn&7, desert spirits of sand","&7and mirage. They create illusions","&7and wield scorching heat, but","&7water dissolves their forms."],
  {"MAGIC_DAMAGE_DEALT":0.15,"FIRE_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.1,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-5,"FREEZING_RESISTANCE":-0.1})

R("ironheart","IRON_CHESTPLATE:-1","&7","Ironheart",
  ["&7Ironhearts&7, mortals whose hearts have","&7been replaced with living iron.","&7They are tireless and nearlyunkillable,","&7but cannot feel joy or pain."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"DAMAGE_RESISTANCE":0.15,"KNOCKBACK_RESISTANCE":0.1,"HEALTH_BONUS":3,"HEALING_BONUS":-0.15,"MOVEMENT_SPEED_BONUS":-0.1})

R("rune_sorcerer","ENCHANTED_BOOK:-1","&5","Rune Sorcerer",
  ["&5Rune Sorcerers&7, mages who inscribe","&7reality-bending runes upon their flesh.","&7Each rune grants immense power,","&7but damages their mortal form."],
  {"MAGIC_DAMAGE_DEALT":0.2,"ENCHANTING_EXP_GAIN":0.15,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":-5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("storm_spirit","LIGHTNING_ROD:-1","&9","Storm Spirit",
  ["&9Storm Spirits&7, living manifestations","&7of thunderstorms. They strike with","&7the fury of lightning and are","&7unstoppable in their element."],
  {"LIGHTNING_DAMAGE_DEALT":0.25,"MOVEMENT_SPEED_BONUS":0.15,"CRIT_CHANCE":0.1,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":-5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("thornweaver","CACTUS_GREEN:-1","&2","Thornweaver",
  ["&2Thornweavers&7, plant-mages who command","&7thorns and brambles. They entangle","&7foes and bleed them slowly, but","&7fire reduces them to ash."],
  {"POISON_DAMAGE_DEALT":0.15,"MELEE_DAMAGE_DEALT":0.15,"HEALING_BONUS":0.1,"FARMING_EXP_GAIN":0.1,"FIRE_RESISTANCE":-0.1})

R("ember_drake","FIRE_CHARGE:-1","&4","Ember Drake",
  ["&4Ember Drakes&7, young dragon-kin of","&7smoldering fire. They breath flames","&7and their scales are hot, but","&7they are not yet full dragons."],
  {"FIRE_DAMAGE_DEALT":0.2,"MELEE_DAMAGE_DEALT":0.15,"FIRE_RESISTANCE":0.1,"FREEZING_RESISTANCE":-0.1,"HEALTH_BONUS":-5})

R("storm_dragon","TRIDENT:-1","&9","Storm Dragon",
  ["&9Storm Dragons&7, majestic beasts of","&7thunder and lightning. They rule","&7the skies and strike with","&7devastating electrical fury."],
  {"LIGHTNING_DAMAGE_DEALT":0.25,"RANGED_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.15,"HEALTH_BONUS":5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("void_serpent","DRAGON_BREATH:-1","&5","Void Serpent",
  ["&5Void Serpents&7, serpentine entities from","&7the spaces between worlds. They warp","&7space and deal void damage that","&7cannot be resisted."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"MAGIC_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.15,"RADIANT_RESISTANCE":-0.2,"HEALTH_BONUS":-5})

R("iron_drake","IRON_BLOCK:-1","&7","Iron Drake",
  ["&7Iron Drakes&7, metallic dragons of","&7unbreakable scale. They are walking","&7fortresses of iron and steel,","&7but they are ponderous."],
  {"ARMOR_MULTIPLIER_BONUS":0.25,"KNOCKBACK_RESISTANCE":0.2,"DAMAGE_RESISTANCE":0.15,"HEALTH_BONUS":10,"MOVEMENT_SPEED_BONUS":-0.2})

R("frost_dragon","BLUE_ICE:-1","&b","Frost Dragon",
  ["&bFrost Dragons&7, ice-breathed drakes of","&7the frozen north. Their breath","&7freezes enemies solid and their","&7scales resist all cold."],
  {"FREEZING_DAMAGE_DEALT":0.25,"FREEZING_RESISTANCE":0.3,"ARMOR_MULTIPLIER_BONUS":0.1,"HEALTH_BONUS":5,"FIRE_RESISTANCE":-0.2})

R("sandstorm_beast","SAND:-1","&e","Sandstorm Beast",
  ["&eSandstorm Beasts&7, living hurricanes","&7of sand and grit. They scour the","&7desert and blind opponents, but","&7water and ice calm their fury."],
  {"MAGIC_DAMAGE_DEALT":0.15,"MELEE_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.1,"FIRE_RESISTANCE":0.1,"FREEZING_RESISTANCE":-0.1,"HEALTH_BONUS":-3})

R("wild_kin","GRASS_BLOCK:-1","&2","Wild Kin",
  ["&2Wild Kin&7, primal beasts who live by","&7the law of tooth and claw. They are","&7at their best in the untamed","&7wilderness."],
  {"MELEE_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.1,"UNARMED_DAMAGE_DEALT":0.1,"FARMING_EXP_GAIN":0.1,"MAGIC_RESISTANCE":-0.1})

R("abyssal_kraken","AXOLOTL_BUCKET:-1","&5","Abyssal Kraken",
  ["&5Abyssal Krakens&7, titanic tentacled","&7horror from the deepest trenches.","&7They crush ships and drag sailors","&7to watery graves."],
  {"MELEE_DAMAGE_DEALT":0.2,"POISON_DAMAGE_DEALT":0.15,"HEALTH_BONUS":10,"KNOCKBACK_RESISTANCE":0.15,"FIRE_RESISTANCE":-0.15,"MOVEMENT_SPEED_BONUS":-0.1})

R("crystal_nymph","AMETHYST_BLOCK:-1","&d","Crystal Nymph",
  ["&dCrystal Nymphs&7, graceful beings of","&7living gemstone. They refract light","&7and wield prismatic magic, but","&7they are fragile."],
  {"MAGIC_DAMAGE_DEALT":0.15,"ENCHANTING_EXP_GAIN":0.15,"LUCK_BONUS":0.1,"CRIT_DAMAGE":0.1,"HEALTH_BONUS":-5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("mossling","MOSS_BLOCK:-1","&2","Mossling",
  ["&2Mosslings&7, tiny plant creatures covered","&7in living moss. They heal allies","&7and grow stronger in nature,","&7but are tiny and fragile."],
  {"HEALING_BONUS":0.2,"FARMING_EXP_GAIN":0.15,"POISON_RESISTANCE":0.1,"HEALTH_BONUS":-6,"SCALE":-0.2})

R("shadow_drake","DRAGON_BREATH:-1","&8","Shadow Drake",
  ["&8Shadow Drakes&7, dragons of pure darkness.","&7They cloak themselves in shadow and","&7strike unseen, but light reveals","&7their presence."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"MELEE_DAMAGE_DEALT":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"DODGE_CHANCE":0.1,"RADIANT_RESISTANCE":-0.15})

R("bone_colossus","BONE_BLOCK:-1","&7","Bone Colossus",
  ["&7Bone Colossi&7, towering skeletons of","&7ancient giants. They tower over","&7battlefields and their bone clubs","&7crush all in their path."],
  {"MELEE_DAMAGE_DEALT":0.2,"BLUDGEONING_DAMAGE_DEALT":0.15,"HEALTH_BONUS":10,"KNOCKBACK_RESISTANCE":0.15,"MOVEMENT_SPEED_BONUS":-0.15,"DODGE_CHANCE":-0.1})

# ── MORE RACES TO REACH 200 ──

R("ash_knight","NETHERITE_CHESTPLATE:-1","&8","Ash Knight",
  ["&8Ash Knights&7, scorched warriors who","&7fight with weapons of hardened ash.","&7They endure fire and oblivion."],
  {"FIRE_RESISTANCE":0.2,"MELEE_DAMAGE_DEALT":0.15,"ARMOR_MULTIPLIER_BONUS":0.1,"HEALTH_BONUS":3,"FREEZING_RESISTANCE":-0.1})

R("lava_walker","MAGMA_CREAM:-1","&4","Lava Walker",
  ["&4Lava Walkers&7, beings who stride across","&7molten rock without harm. Their touch","&7melts all they contact."],
  {"FIRE_DAMAGE_DEALT":0.25,"FIRE_RESISTANCE":0.3,"MOVEMENT_SPEED_BONUS":0.05,"HEALTH_BONUS":-3,"FREEZING_RESISTANCE":-0.2})

R("ice_witch","PACKED_ICE:-1","&b","Ice Witch",
  ["&bIce Witches&7, crones of the frozen wastes","&7who command bitter cold. Their hexes","&7freeze the blood of the living."],
  {"FREEZING_DAMAGE_DEALT":0.25,"FREEZING_RESISTANCE":0.2,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-3,"FIRE_RESISTANCE":-0.15})

R("plague_bearer","ROTTEN_FLESH:-1","&2","Plague Bearer",
  ["&2Plague Bearers&7, diseased beings who","&7spread sickness wherever they go.","&7They are immune to all toxins."],
  {"POISON_DAMAGE_DEALT":0.25,"POISON_RESISTANCE":0.4,"HEALING_BONUS":0.1,"HEALTH_BONUS":-4,"MELEE_DAMAGE_DEALT":-0.1})

R("flamecaller","BLAZE_POWDER:-1","&c","Flamecaller",
  ["&cFlamecallers&7, pyromancers who summon","&7walls of living flame. They command","&7fire in all its forms."],
  {"FIRE_DAMAGE_DEALT":0.3,"COOLDOWN_REDUCTION":0.1,"MAGIC_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-3,"FREEZING_RESISTANCE":-0.15})

R("glacierborn","BLUE_ICE:-1","&b","Glacierborn",
  ["&bGlacierborn&7, ancient ice spirits who","&7have existed since the first winter.","&7They bring endless cold."],
  {"FREEZING_DAMAGE_DEALT":0.3,"FREEZING_RESISTANCE":0.35,"HEALTH_BONUS":5,"FIRE_RESISTANCE":-0.25,"MOVEMENT_SPEED_BONUS":-0.1})

R("stonecaller","STONE:-1","&7","Stonecaller",
  ["&7Stonecallers&7, geomancers who command","&7the earth itself. They raise walls","&7of stone and crush foes."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"DAMAGE_RESISTANCE":0.15,"BLUDGEONING_DAMAGE_DEALT":0.2,"HEALTH_BONUS":5,"MOVEMENT_SPEED_BONUS":-0.15})

R("windrider","FEATHER:-1","&f","Windrider",
  ["&fWindriders&7, sky-dancers who ride the","&7gales. They are fastest of all races","&7and strike from the air."],
  {"MOVEMENT_SPEED_BONUS":0.25,"SPRINT_MOVEMENT_SPEED_BONUS":0.15,"DODGE_CHANCE":0.15,"HEALTH_BONUS":-4,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("thunderlord","LIGHTNING_ROD:-1","&e","Thunderlord",
  ["&eThunderlords&7, masters of the storm who","&7command lightning at will. Their power","&7shakes the very heavens."],
  {"LIGHTNING_DAMAGE_DEALT":0.3,"COOLDOWN_REDUCTION":0.15,"RANGED_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-3,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("ashwalker","SUSPICIOUS_STEW:-1","&8","Ashwalker",
  ["&8Ashwalkers&7, beings who tread upon","&7the ashes of destroyed worlds.","&7They wield entropy and decay."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"FIRE_RESISTANCE":0.15,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-3,"RADIANT_RESISTANCE":-0.1})

R("tidecaller","TROPICAL_FISH:-1","&3","Tidecaller",
  ["&3Tidecallers&7, water mages who command","&7the oceans. They summon tsunamis","&7and heal with ocean magic."],
  {"FREEZING_DAMAGE_DEALT":0.2,"HEALING_BONUS":0.2,"FISHING_LUCK":2,"FIRE_RESISTANCE":-0.1})

R("dustfiend","SAND:-1","&e","Dustfiend",
  ["&eDustfiends&7, desert spirits of scorching","&7heat. They blind and burn foes with","&7sandstorms of fire."],
  {"FIRE_DAMAGE_DEALT":0.2,"MAGIC_DAMAGE_DEALT":0.1,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-3,"FREEZING_RESISTANCE":-0.1})

R("ember_sprite","BLAZE_POWDER:-1","&c","Ember Sprite",
  ["&cEmber Sprites&7, tiny fire fae who","&7dance through flames. They are fast","&7and deadly despite their size."],
  {"FIRE_DAMAGE_DEALT":0.2,"MOVEMENT_SPEED_BONUS":0.2,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-5,"SCALE":-0.15})

R("frost_spirit","PACKED_ICE:-1","&b","Frost Spirit",
  ["&bFrost Spirits&7, cold elementals who","&7numb all they touch. They freeze","&7enemies solid with a glance."],
  {"FREEZING_DAMAGE_DEALT":0.25,"FREEZING_RESISTANCE":0.25,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-4,"FIRE_RESISTANCE":-0.2})

R("storm_wraith","CONDUIT:-1","&9","Storm Wraith",
  ["&9Storm Wraiths&7, electrical phantoms","&7who haunt thunderclouds. They strike","&7with shocking force from above."],
  {"LIGHTNING_DAMAGE_DEALT":0.25,"DODGE_CHANCE":0.15,"MOVEMENT_SPEED_BONUS":0.15,"HEALTH_BONUS":-4,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("earth_shaper","STONE:-1","&6","Earth Shaper",
  ["&6Earth Shapers&7, geomancers who mold","&7terrain and create stone constructs.","&7They are sturdy and unyielding."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"DAMAGE_RESISTANCE":0.15,"HEALTH_BONUS":5,"DIG_SPEED":0.15,"MOVEMENT_SPEED_BONUS":-0.1})

R("sky_dancer","FEATHER:-1","&f","Sky Dancer",
  ["&fSky Dancers&7, graceful aerial fighters","&7who dance through the clouds. Their","&7elegance hides deadly precision."],
  {"DODGE_CHANCE":0.2,"MOVEMENT_SPEED_BONUS":0.15,"CRIT_CHANCE":0.1,"RANGED_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-3})

R("shadowcaster","SHADOW_DYE:-1","&8","Shadowcaster",
  ["&8Shadowcasters&7, dark mages who wield","&7the power of shadow. They blind foes","&7and strike from darkness."],
  {"MAGIC_DAMAGE_DEALT":0.2,"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-3,"RADIANT_RESISTANCE":-0.1})

R("plague_doctor","FERMENTED_SPIDER_EYE:-1","&2","Plague Doctor",
  ["&2Plague Doctors&7, scholars of disease","&7and remedy. They brew potions that","&7both heal and harm with equal ease."],
  {"HEALING_BONUS":0.15,"POISON_DAMAGE_DEALT":0.2,"ALCHEMY_EXP_GAIN":0.2,"COOLDOWN_REDUCTION":0.1})

R("void_weaver","ENDER_EYE:-1","&5","Void Weaver",
  ["&5Void Weavers&7, dimensional mages who","&7weave threads of nothing. They tear","&7holes in reality itself."],
  {"MAGIC_DAMAGE_DEALT":0.2,"NECROTIC_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-4,"RADIANT_RESISTANCE":-0.15})

R("crystal_mage","AMETHYST_SHARD:-1","&d","Crystal Mage",
  ["&dCrystal Mages&7, prismatic sorcerers who","&7channel light through gemstones.","&7Their spells shimmer with color."],
  {"MAGIC_DAMAGE_DEALT":0.2,"ENCHANTING_EXP_GAIN":0.2,"LUCK_BONUS":0.1,"COOLDOWN_REDUCTION":0.1})

R("moon_weaver","CLOCK:-1","&9","Moon Weaver",
  ["&9Moon Weavers&7, lunar mages who draw","&7power from the moon. They grow","&7stronger as night falls."],
  {"MAGIC_DAMAGE_DEALT":0.2,"FREEZING_DAMAGE_DEALT":0.15,"HEALING_BONUS":0.1,"DODGE_CHANCE":0.1})

R("sunCaller","SUNFLOWER:-1","&e","Sun Caller",
  ["&eSun Callers&7, solar mages who channel","&7the power of the sun. Their light","&7burns the unholy."],
  {"RADIANT_DAMAGE_DEALT":0.25,"HEALING_BONUS":0.15,"FIRE_DAMAGE_DEALT":0.1,"NECROTIC_RESISTANCE":-0.15})

R("starCaller","NETHER_STAR:-1","&e","Star Caller",
  ["&eStar Callers&7, cosmic mages who channel","&7stellar energy. Their spells rain","&7down like falling stars."],
  {"MAGIC_DAMAGE_DEALT":0.2,"RADIANT_DAMAGE_DEALT":0.15,"CRIT_DAMAGE":0.15,"HEALTH_BONUS":-4})

R("abyss_walker","OBSIDIAN:-1","&5","Abyss Walker",
  ["&5Abyss Walkers&7, void-touched warriors","&7who stride between dimensions. They","&7wield entropy as a weapon."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"DODGE_CHANCE":0.2,"MOVEMENT_SPEED_BONUS":0.1,"HEALTH_BONUS":-4,"RADIANT_RESISTANCE":-0.15})

R("soul_reaper","SOUL_SAND:-1","&8","Soul Reaper",
  ["&8Soul Reapers&7, death-themed fighters who","&7harvest souls with each kill. They","&7grow stronger with every death."],
  {"NECROTIC_DAMAGE_DEALT":0.25,"MELEE_DAMAGE_DEALT":0.15,"HEALING_BONUS":0.1,"HEALTH_BONUS":-3,"RADIANT_RESISTANCE":-0.1})

R("bone_weaver","BONE_BLOCK:-1","&7","Bone Weaver",
  ["&7Bone Weavers&7, necromancers who craft","&7weapons and armor from bone. Their","&7creations are grotesque but powerful."],
  {"NECROTIC_DAMAGE_DEALT":0.15,"SMITHING_QUALITY_GENERAL":20,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":3})

R("sand_serpent","SAND:-1","&e","Sand Serpent",
  ["&eSand Serpents&7, desert snake-folk who","&7burrow beneath the dunes. They","&7ambush prey from below."],
  {"MELEE_DAMAGE_DEALT":0.2,"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"POISON_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-3,"FIRE_RESISTANCE":0.05})

R("tundra_wolf","POPPED_CHORUS_FRUIT:-1","&f","Tundra Wolf",
  ["&fTundra Wolves&7, arctic pack hunters who","&7endure the harshest cold. They","&7fight with icy fury and pack tactics."],
  {"MELEE_DAMAGE_DEALT":0.15,"FREEZING_DAMAGE_DEALT":0.1,"MOVEMENT_SPEED_BONUS":0.1,"SPRINT_MOVEMENT_SPEED_BONUS":0.1,"HEALTH_BONUS":3})

R("swamp_hag","SLIME_BALL:-1","&2","Swamp Hag",
  ["&2Swamp Hags&7, bog-dwelling crones who","&7brew potions and hexes from swamp","&7herbs. Their毒 is legendary."],
  {"POISON_DAMAGE_DEALT":0.2,"ALCHEMY_EXP_GAIN":0.2,"HEALING_BONUS":0.1,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-3})

R("sky_dragon","ELYTRA:-1","&b","Sky Dragon",
  ["&bSky Dragons&7, aerial dragons who rule","&7the clouds. They rain destruction","&7from above with impunity."],
  {"RANGED_DAMAGE_DEALT":0.2,"MOVEMENT_SPEED_BONUS":0.15,"FALLING_RESISTANCE":0.3,"HEALTH_BONUS":5,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("iron_golem","IRON_BLOCK:-1","&7","Iron Golem",
  ["&7Iron Golems&7, living constructs of iron","&7and magic. They protect villages","&7and are nearly indestructible."],
  {"ARMOR_MULTIPLIER_BONUS":0.3,"KNOCKBACK_RESISTANCE":0.3,"HEALTH_BONUS":10,"MOVEMENT_SPEED_BONUS":-0.2,"DODGE_CHANCE":-0.15})

R("dark_elf","PURPLE_DYE:-1","&5","Dark Elf",
  ["&5Dark Elves&7, exiled elves of the","&7underdark. They master poison and","&7shadow magic with deadly skill."],
  {"MAGIC_DAMAGE_DEALT":0.15,"POISON_DAMAGE_DEALT":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-3})

R("high_elf","LIGHT_BLUE_DYE:-1","&b","High Elf",
  ["&bHigh Elves&7, ancient elves of supreme","&7magical talent. They are the most","&7powerful spellcasters among the fey."],
  {"MAGIC_DAMAGE_DEALT":0.2,"ENCHANTING_EXP_GAIN":0.25,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-4,"ARMOR_MULTIPLIER_BONUS":-0.1})

R("wood_elf","OAK_LOG:-1","&2","Wood Elf",
  ["&2Wood Elves&7, forest-dwelling elves who","&7are at one with nature. They excel","&7in archery and woodcraft."],
  {"RANGED_DAMAGE_DEALT":0.2,"WOODCUTTING_EXP_GAIN":0.2,"DODGE_CHANCE":0.15,"MOVEMENT_SPEED_BONUS":0.1,"HEALTH_BONUS":-3})

R("sea_dwarf","PRISMARINE_SHARD:-1","&3","Sea Dwarf",
  ["&3Sea Dwarves&7, dwarves who dwell beneath","&7the waves. They mine underwater veins","&7and craft tridents of great power."],
  {"MINING_EXP_GAIN":0.2,"FISHING_LUCK":2,"MELEE_DAMAGE_DEALT":0.1,"ARMOR_MULTIPLIER_BONUS":0.1,"HEALTH_BONUS":3})

R("mountain_giant","STONE_BRICKS:-1","&7","Mountain Giant",
  ["&7Mountain Giants&7, colossal beings who","&7dwell in the highest peaks. They are","&7living mountains of stone and fury."],
  {"HEALTH_BONUS":15,"ARMOR_MULTIPLIER_BONUS":0.25,"KNOCKBACK_RESISTANCE":0.3,"MOVEMENT_SPEED_BONUS":-0.25,"DODGE_CHANCE":-0.2})

R("hill_giant","GRASS_BLOCK:-1","&6","Hill Giant",
  ["&6Hill Giants&7, large but not overly bright","&7giants who roam the hills. They are","&7strong but not the sharpest."],
  {"HEALTH_BONUS":10,"MELEE_DAMAGE_DEALT":0.2,"KNOCKBACK_RESISTANCE":0.15,"MOVEMENT_SPEED_BONUS":-0.15,"MAGIC_RESISTANCE":-0.15})

R("fog_phantom","GLASS_BOTTLE:-1","&7","Fog Phantom",
  ["&7Fog Phantoms&7, misty spirits that haunt","&7foggy moors. They drift unseen and","&7strike when the mist is thickest."],
  {"DODGE_CHANCE":0.25,"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"MAGIC_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-5,"RADIANT_RESISTANCE":-0.15})

R("dust_devil","SAND:-1","&e","Dust Devil",
  ["&eDust Devils&7, whirlwind spirits of the","&7desert. They scour foes with grit","&7and sand, blinding all who oppose."],
  {"MAGIC_DAMAGE_DEALT":0.15,"MOVEMENT_SPEED_BONUS":0.2,"DODGE_CHANCE":0.15,"HEALTH_BONUS":-4,"FIRE_RESISTANCE":0.05})

R("magma_sprite","MAGMA_CREAM:-1","&4","Magma Sprite",
  ["&4Magma Sprites&7, tiny fire spirits who","&7dance in volcanic vents. They are","&7fast and burn all they touch."],
  {"FIRE_DAMAGE_DEALT":0.2,"MOVEMENT_SPEED_BONUS":0.2,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-5,"SCALE":-0.15})

R("frost_fairy","BLUE_ICE:-1","&b","Frost Fairy",
  ["&bFrost Fairies&7, tiny ice fae who","&7bring the cold. They heal allies","&7and freeze foes with equal ease."],
  {"FREEZING_DAMAGE_DEALT":0.15,"HEALING_BONUS":0.2,"FREEZING_RESISTANCE":0.15,"HEALTH_BONUS":-6,"SCALE":-0.2})

R("shadow_fairy","SHADOW_DYE:-1","&5","Shadow Fairy",
  ["&5Shadow Fairies&7, dark fae who dwell in","&7the shadows. They are tricksters and","&7thieves of the highest order."],
  {"DODGE_CHANCE":0.2,"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"MAGIC_DAMAGE_DEALT":0.15,"HEALTH_BONUS":-6,"SCALE":-0.2})

R("star_fairy","NETHER_STAR:-1","&e","Star Fairy",
  ["&eStar Fairies&7, celestial fae who fell","&7from the heavens. They wield cosmic","&7power in their tiny frames."],
  {"MAGIC_DAMAGE_DEALT":0.2,"CRIT_DAMAGE":0.15,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-6,"SCALE":-0.2})

R("plague_witch","FERMENTED_SPIDER_EYE:-1","&2","Plague Witch",
  ["&2Plague Witches&7, crones who spread","&7disease and decay. Their curses are","&7unbreakable and their potions deadly."],
  {"POISON_DAMAGE_DEALT":0.3,"ALCHEMY_EXP_GAIN":0.2,"NECROTIC_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-3,"HEALING_BONUS":0.05})

R("warlock_v2","WITHER_SKELETON_SKULL:-1","&5","Warlock",
  ["&5Warlocks&7, dark magic users who draw","&7on forbidden power. Their necrotic","&7spells are devastating."],
  {"NECROTIC_DAMAGE_DEALT":0.25,"COOLDOWN_REDUCTION":0.15,"MAGIC_DAMAGE_DEALT":0.15,"RADIANT_RESISTANCE":-0.15})

R("demon_hunter","NETHERITE_SWORD:-1","&4","Demon Hunter",
  ["&4Demon Hunters&7, warriors who specialize","&7in slaying demons and undead. They","&7are relentless in their pursuit."],
  {"MELEE_DAMAGE_DEALT":0.15,"NECROTIC_DAMAGE_DEALT":0.1,"FIRE_DAMAGE_DEALT":0.1,"DODGE_CHANCE":0.1,"RADIANT_RESISTANCE":0.1})

R("vampire_hunter","GOLDEN_SWORD:-1","&e","Vampire Hunter",
  ["&eVampire Hunters&7, specialists in undead","&7slaying. They carry blessed weapons","&7and are immune to life drain."],
  {"MELEE_DAMAGE_DEALT":0.15,"RADIANT_DAMAGE_DEALT":0.1,"NECROTIC_RESISTANCE":0.15,"CRIT_CHANCE":0.1,"HEALING_BONUS":0.1})

R("dragon_slayer","DIAMOND_SWORD:-1","&c","Dragon Slayer",
  ["&cDragon Slayers&7, warriors who have","&7sworn to slay all dragons. Their","&7weapons are forged specifically for","&7the task."],
  {"MELEE_DAMAGE_DEALT":0.2,"CRIT_DAMAGE":0.2,"DAMAGE_RESISTANCE":0.1,"HEALTH_BONUS":3,"DODGE_CHANCE":-0.05})

R("undead_hunter","IRON_SWORD:-1","&7","Undead Hunter",
  ["&7Undead Hunters&7, holy warriors who","&7destroy the undead. Their radiant","&7weapons burn all who have died."],
  {"RADIANT_DAMAGE_DEALT":0.2,"MELEE_DAMAGE_DEALT":0.1,"NECROTIC_RESISTANCE":0.2,"RADIANT_RESISTANCE":0.15})

R("giant_slayer","DIAMOND_AXE:-1","&6","Giant Slayer",
  ["&6Giant Slayers&7, warriors specialized in","&7bringing down massive foes. Their","&7weapons cut through thick hide."],
  {"MELEE_DAMAGE_DEALT":0.2,"CRIT_DAMAGE":0.15,"CRIT_CHANCE":0.1,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-2})

R("troll_kin","VINE_WEB:-1","&2","Troll-Kin",
  ["&2Troll-Kin&7, lesser trolls of the deep","&7forests. They regenerate slowly and","&7fight with brutal strength."],
  {"HEALTH_BONUS":8,"HEALING_BONUS":0.15,"MELEE_DAMAGE_DEALT":0.15,"FIRE_RESISTANCE":-0.2,"MOVEMENT_SPEED_BONUS":-0.1})

R("orc_raider","DIAMOND_AXE:-1","&2","Orc Raider",
  ["&2Orc Raiders&7, swift orc warriors who","&7strike fast and hard. They take","&7what they want by force and speed."],
  {"MELEE_DAMAGE_DEALT":0.2,"MOVEMENT_SPEED_BONUS":0.15,"SPRINT_MOVEMENT_SPEED_BONUS":0.1,"KNOCKBACK_RESISTANCE":0.1,"MAGIC_RESISTANCE":-0.1})

R("elven_ranger","BOW:-1","&b","Elven Ranger",
  ["&bElven Rangers&7, forest guardians who","&7never miss their mark. They patrol","&7the woodlands protecting the innocent."],
  {"RANGED_DAMAGE_DEALT":0.25,"CRIT_CHANCE":0.15,"DODGE_CHANCE":0.1,"WOODCUTTING_EXP_GAIN":0.15,"HEALTH_BONUS":-2})

R("dwarven_smith","ANVIL:-1","&6","Dwarven Smith",
  ["&6Dwarven Smiths&7, master craftsmen of","&7metal and stone. Their creations","&7are of unmatched quality."],
  {"SMITHING_QUALITY_GENERAL":30,"MINING_EXP_GAIN":0.2,"DURABILITY_BONUS":0.2,"HEALTH_BONUS":3})

R("human_mage","EXPERIENCE_BOTTLE:-1","&a","Human Mage",
  ["&aHuman Mages&7, versatile spellcasters","&7who adapt to any situation. Their","&7raw talent compensates for lack","&7of specialization."],
  {"MAGIC_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.15,"ENCHANTING_EXP_GAIN":0.15,"HEALTH_BONUS":-3})

R("undead_mage","WITHER_SKELETON_SKULL:-1","&7","Undead Mage",
  ["&7Undead Mages&7, liches who have not yet","&7achieved true immortality. They wield","&7necromancy with growing power."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"MAGIC_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-4,"HEALING_BONUS":-0.1})

R("celestial_warrior","GOLDEN_CHESTPLATE:-1","&e","Celestial Warrior",
  ["&eCelestial Warriors&7, divine champions","&7who fight with holy fury. Their","&7weapons burn with radiant light."],
  {"RADIANT_DAMAGE_DEALT":0.2,"MELEE_DAMAGE_DEALT":0.1,"ARMOR_MULTIPLIER_BONUS":0.1,"HEALING_BONUS":0.1})

R("abyssal_warrior","NETHERITE_CHESTPLATE:-1","&4","Abyssal Warrior",
  ["&4Abyssal Warriors&7, demons who fight","&7in the front lines. They wield","&7fire-wreathed weapons of destruction."],
  {"MELEE_DAMAGE_DEALT":0.2,"FIRE_DAMAGE_DEALT":0.15,"KNOCKBACK_RESISTANCE":0.15,"HEALTH_BONUS":5,"RADIANT_RESISTANCE":-0.2})

R("magma_golem","MAGMA_CREAM:-1","&4","Magma Golem",
  ["&4Magma Golems&7, constructs of living lava.","&7They burn all they touch and are","&7nearly impossible to destroy."],
  {"FIRE_DAMAGE_DEALT":0.2,"FIRE_RESISTANCE":0.3,"ARMOR_MULTIPLIER_BONUS":0.2,"HEALTH_BONUS":8,"MOVEMENT_SPEED_BONUS":-0.2})

R("frost_golem","PACKED_ICE:-1","&b","Frost Golem",
  ["&bFrost Golems&7, constructs of enchanted ice.","&7They freeze all they touch and their","&7bodies are nearly indestructible."],
  {"FREEZING_DAMAGE_DEALT":0.25,"FREEZING_RESISTANCE":0.3,"ARMOR_MULTIPLIER_BONUS":0.2,"HEALTH_BONUS":8,"FIRE_RESISTANCE":-0.2})

R("storm_golem","CONDUIT:-1","&9","Storm Golem",
  ["&9Storm Golems&7, constructs charged with","&7lightning. They shock all who approach","&7and are powered by electrical fury."],
  {"LIGHTNING_DAMAGE_DEALT":0.25,"ARMOR_MULTIPLIER_BONUS":0.15,"HEALTH_BONUS":5,"DODGE_CHANCE":0.1,"MOVEMENT_SPEED_BONUS":0.1})

R("void_golem","OBSIDIAN:-1","&5","Void Golem",
  ["&5Void Golems&7, constructs from the spaces","&7between dimensions. They warp reality","&7and drain life from all they touch."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"ARMOR_MULTIPLIER_BONUS":0.2,"HEALTH_BONUS":8,"DODGE_CHANCE":0.1,"RADIANT_RESISTANCE":-0.15})

R("shadow_elf","BLACK_DYE:-1","&8","Shadow Elf",
  ["&8Shadow Elves&7, elves who dwell in","&7perpetual darkness. They master","&7stealth and shadow magic."],
  {"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"DODGE_CHANCE":0.15,"MAGIC_DAMAGE_DEALT":0.15,"MELEE_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-3})

R("flame_elf","BLAZE_POWDER:-1","&c","Flame Elf",
  ["&cFlame Elves&7, elves who have embraced","&7the power of fire. Their blades","&7burn with eternal flame."],
  {"FIRE_DAMAGE_DEALT":0.25,"MELEE_DAMAGE_DEALT":0.1,"FIRE_RESISTANCE":0.15,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":-3})

R("ice_elf","BLUE_ICE:-1","&b","Ice Elf",
  ["&bIce Elves&7, elves of the frozen north.","&7They wield freezing magic and their","&7touch brings eternal winter."],
  {"FREEZING_DAMAGE_DEALT":0.25,"FREEZING_RESISTANCE":0.2,"DODGE_CHANCE":0.1,"MOVEMENT_SPEED_BONUS":0.1,"HEALTH_BONUS":-3})

R("mountain_dwarf","STONE:-1","&7","Mountain Dwarf",
  ["&7Mountain Dwarves&7, the hardiest of all","&7dwarven clans. They delve deepest","&7and mine the richest veins."],
  {"MINING_EXP_GAIN":0.25,"DIG_SPEED":0.2,"HEALTH_BONUS":5,"ARMOR_MULTIPLIER_BONUS":0.15,"MOVEMENT_SPEED_BONUS":-0.1})

R("hill_dwarf","GRASS_BLOCK:-1","&6","Hill Dwarf",
  ["&6Hill Dwarves&7, dwarven farmers and","&7brewers who tend the rolling hills.","&7They are masters of ale and harvest."],
  {"FARMING_EXP_GAIN":0.2,"HEALING_BONUS":0.15,"LUCK_BONUS":0.1,"HEALTH_BONUS":3,"MELEE_DAMAGE_DEALT":-0.05})

R("deep_dwarf","DEEPSLATE:-1","&8","Deep Dwarf",
  ["&8Deep Dwarves&7, dwarves who dwell in","&7the deepest caverns. They are adapted","&7to total darkness and rich veins."],
  {"MINING_EXP_GAIN":0.3,"DIG_SPEED":0.25,"DODGE_CHANCE":0.1,"HEALTH_BONUS":3,"MOVEMENT_SPEED_BONUS":-0.1})

R("necro_undead","WITHER_SKELETON_SKULL:-1","&5","Necrotic Undead",
  ["&5Necrotic Undead&7, undead who have learned","&7to channel necromantic magic. They","&7wield death itself as a weapon."],
  {"NECROTIC_DAMAGE_DEALT":0.25,"NECROTIC_RESISTANCE":0.3,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":3,"RADIANT_RESISTANCE":-0.2})

R("war_undead","NETHERITE_CHESTPLATE:-1","&8","War Undead",
  ["&8War Undead&7, undead warriors raised for","&7battle. They fight with tireless","&7fury and know no fear."],
  {"MELEE_DAMAGE_DEALT":0.2,"KNOCKBACK_RESISTANCE":0.2,"HEALTH_BONUS":8,"HEALING_BONUS":-0.2,"MOVEMENT_SPEED_BONUS":-0.1})

R("spirit_undead","SOUL_LANTERN:-1","&f","Spirit Undead",
  ["&fSpirit Undead&7, incorporeal undead who","&7drift between the living and dead","&7worlds. They are nearly untouchable."],
  {"DODGE_CHANCE":0.25,"MAGIC_DAMAGE_DEALT":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"HEALTH_BONUS":-5,"RADIANT_RESISTANCE":-0.15})

R("wight","BONE_MEAL:-1","&7","Wight",
  ["&7Wights&7, gaunt undead who drain the","&7warmth from all they touch. They are","&7fast and relentless hunters."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"MOVEMENT_SPEED_BONUS":0.15,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-3,"RADIANT_RESISTANCE":-0.15})

print(f"Total races defined: {len(RACE_DEFS)}")
assert len(RACE_DEFS) == 200, f"Expected 200 races, got {len(RACE_DEFS)}"

# ─── CLASS DEFINITIONS ──────────────────────────────────────────────────────
CLASS_DEFS = []

def C(name, grp, icon, color, display, lore, stats):
    assert name not in EXISTING_CLASSES, f"Duplicate class: {name}"
    EXISTING_CLASSES.add(name)
    CLASS_DEFS.append((name, grp, icon, color, display, lore, stats))

# Group 1 - Melee DPS
C("champion",1,"DIAMOND_SWORD:-1","&c","Champion",
  ["&cChampions&7, noble warriors who lead","&7the charge. They fight with honor","&7and inspire allies with their courage."],
  {"MELEE_DAMAGE_DEALT":0.15,"ARMOR_MULTIPLIER_BONUS":0.1,"CRIT_DAMAGE":0.1,"KNOCKBACK_RESISTANCE":0.1})

C("duelist",1,"GOLDEN_SWORD:-1","&e","Duelist",
  ["&eDuellists&7, masters of single combat.","&7They parry and riposte with deadly","&7precision, but fight alone."],
  {"MELEE_DAMAGE_DEALT":0.2,"CRIT_CHANCE":0.15,"DODGE_CHANCE":0.1,"MELEE_DAMAGE_DEALT":-0.05})

C("marauder",1,"NETHERITE_AXE:-1","&4","Marauder",
  ["&4Marauders&7, ruthless raiders who take","&7what they want by force. They deal","&7devastating blows and steal from","&7the fallen."],
  {"MELEE_DAMAGE_DEALT":0.2,"KNOCKBACK_RESISTANCE":0.15,"CRIT_DAMAGE":0.15,"ARMOR_MULTIPLIER_BONUS":-0.05})

C("gladiator",1,"CHAINMAIL_HELMET:-1","&6","Gladiator",
  ["&6Gladiators&7, arena champions who fight","&7for glory. They are versatile fighters","&7with strong offense and defense."],
  {"MELEE_DAMAGE_DEALT":0.1,"ARMOR_MULTIPLIER_BONUS":0.1,"CRIT_CHANCE":0.1,"HEALTH_BONUS":3})

C("lancer",1,"TRIDENT:-1","&9","Lancer",
  ["&9Lancers&7, mounted warriors who charge","&7with devastating force. Their reach","&7and speed make them deadly."],
  {"MELEE_DAMAGE_DEALT":0.15,"RANGED_DAMAGE_DEALT":0.1,"MOVEMENT_SPEED_BONUS":0.1,"CRIT_CHANCE":0.05})

C("warmonger",1,"BLAZE_ROD:-1","&4","Warmonger",
  ["&4Warmongers&7, bloodthirsty warriors who","&7feed on battle. They grow stronger","&7as they fight, becoming unstoppable."],
  {"MELEE_DAMAGE_DEALT":0.15,"HEALTH_BONUS":5,"DAMAGE_RESISTANCE":0.1,"MOVEMENT_SPEED_BONUS":-0.05})

C("reaper",1,"WITHER_SKELETON_SKULL:-1","&8","Reaper",
  ["&8Reapers&7, death-themed fighters who","&7harvest souls with each kill. They","&7are feared on the battlefield."],
  {"MELEE_DAMAGE_DEALT":0.15,"CRIT_CHANCE":0.15,"NECROTIC_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-3})

C("juggernaut",1,"SHIELD:-1","&7","Juggernaut",
  ["&7Juggernauts&7, unstoppable forces of","&7destruction. They shrug off blows","&7and keep advancing, but are slow."],
  {"HEALTH_BONUS":8,"ARMOR_MULTIPLIER_BONUS":0.15,"KNOCKBACK_RESISTANCE":0.2,"MOVEMENT_SPEED_BONUS":-0.15})

C("blade_dancer",1,"DIAMOND_SWORD:-1","&d","Blade Dancer",
  ["&dBlade Dancers&7, graceful warriors who","&7turn combat into a deadly dance.","&7They weave between foes with","&7lethal elegance."],
  {"MELEE_DAMAGE_DEALT":0.1,"DODGE_CHANCE":0.15,"CRIT_CHANCE":0.1,"MOVEMENT_SPEED_BONUS":0.1})

C("pit_fighter",1,"RAW_BEEF:-1","&c","Pit Fighter",
  ["&cPit Fighters&7, brawlers who fight with","&7raw power and dirty tactics.","&7They deal massive damage but","&7take hits to give them."],
  {"MELEE_DAMAGE_DEALT":0.2,"UNARMED_DAMAGE_DEALT":0.15,"ARMOR_MULTIPLIER_BONUS":-0.1,"HEALTH_BONUS":3})

# Group 2 - Ranged DPS
C("marksman",2,"BOW:-1","&e","Marksman",
  ["&eMarksmen&7, expert archers who never","&7miss their mark. Their arrows fly","&7true and strike with deadly force."],
  {"RANGED_DAMAGE_DEALT":0.2,"CRIT_CHANCE":0.15,"RANGED_VELOCITY_BONUS":0.1})

C("hunter",2,"ARROW:-1","&a","Hunter",
  ["&aHunters&7, wilderness trackers who use","&7bows and traps. They are masters","&7of the hunt and the harvest."],
  {"RANGED_DAMAGE_DEALT":0.15,"FARMING_DROP_MULTIPLIER":0.15,"FISHING_LUCK":1,"CRIT_CHANCE":0.05})

C("sniper",2,"SPECTRAL_ARROW:-1","&8","Sniper",
  ["&8Snipers&7, patient killers who strike","&7from extreme range. One shot, one","&7kill is their motto."],
  {"RANGED_DAMAGE_DEALT":0.25,"CRIT_DAMAGE":0.2,"RANGED_VELOCITY_BONUS":0.15,"MELEE_DAMAGE_DEALT":-0.1})

C("falconer",2,"FEATHER:-1","&6","Falconer",
  ["&6Falconers&7, bird-masters who fight","&7alongside their avian companions.","&7Their birds distract and wound foes."],
  {"RANGED_DAMAGE_DEALT":0.15,"CRIT_CHANCE":0.1,"DODGE_CHANCE":0.1,"FARMING_DROP_MULTIPLIER":0.1})

C("ballistae",2,"CROSSBOW:-1","&7","Ballistae",
  ["&7Ballistae&7, heavy ranged specialists","&7who wield massive crossbows. They","&7pierce armor with ease."],
  {"RANGED_DAMAGE_DEALT":0.2,"BLUDGEONING_DAMAGE_DEALT":0.1,"CRIT_DAMAGE":0.15,"MOVEMENT_SPEED_BONUS":-0.05})

C("slinger",2,"STRING:-1","&a","Slinger",
  ["&aSlings&7, quick-draw fighters who use","&7slings and thrown weapons. They","&7attack rapidly and move fast."],
  {"RANGED_DAMAGE_DEALT":0.1,"ATTACK_SPEED_BONUS":0.15,"MOVEMENT_SPEED_BONUS":0.1,"CRIT_CHANCE":0.05})

C("arbalist",2,"CROSSBOW:-1","&8","Arbalist",
  ["&8Arbalists&7, crossbow experts who fire","&7heavy bolts with devastating force.","&7They can punch through any shield."],
  {"RANGED_DAMAGE_DEALT":0.2,"CRIT_DAMAGE":0.15,"ARMOR_MULTIPLIER_BONUS":0.05})

C("sharpshooter",2,"SPECTRAL_ARROW:-1","&e","Sharpshooter",
  ["&eSharpshooters&7, legendary marksmen whose","&7accuracy is supernatural. They hit","&7weak spots with every shot."],
  {"RANGED_DAMAGE_DEALT":0.2,"CRIT_CHANCE":0.2,"CRIT_DAMAGE":0.1,"DODGE_CHANCE":0.05})

C("beastmaster",2,"LEAD:-1","&6","Beastmaster",
  ["&6Beastmasters&7, warriors who fight alongside","&7tamed beasts. Their animal companions","&7amplify their power in battle."],
  {"RANGED_DAMAGE_DEALT":0.1,"MELEE_DAMAGE_DEALT":0.1,"HEALTH_BONUS":3,"FARMING_DROP_MULTIPLIER":0.15})

C("trapper",2,"STRING:-1","&2","Trapper",
  ["&2Trappers&7, cunning hunters who use","&7traps and snares. They control the","&7battlefield and bleed foes slowly."],
  {"RANGED_DAMAGE_DEALT":0.1,"POISON_DAMAGE_DEALT":0.15,"CRIT_CHANCE":0.1,"DIG_SPEED":0.1})

# Group 3 - Magic DPS
C("sorcerer",3,"BLAZE_ROD:-1","&b","Sorcerer",
  ["&bSorcerers&7, raw magical talent who","&7wield immense arcane power. They","&7devastate foes with pure magic."],
  {"MAGIC_DAMAGE_DEALT":0.25,"COOLDOWN_REDUCTION":0.15,"CRIT_DAMAGE":0.1,"ARMOR_MULTIPLIER_BONUS":-0.1})

C("elementalist",3,"MAGMA_CREAM:-1","&e","Elementalist",
  ["&eElementalists&7, mages who command all","&7elements. They shift between fire,","&7ice, and lightning at will."],
  {"FIRE_DAMAGE_DEALT":0.15,"FREEZING_DAMAGE_DEALT":0.15,"LIGHTNING_DAMAGE_DEALT":0.15,"MAGIC_DAMAGE_DEALT":0.1})

C("conjurer",3,"EXPERIENCE_BOTTLE:-1","&d","Conjurer",
  ["&dConjurers&7, mages who summon and create","&7magical constructs. They bend reality","&7to their will with devastating power."],
  {"MAGIC_DAMAGE_DEALT":0.2,"COOLDOWN_REDUCTION":0.2,"ARMOR_MULTIPLIER_BONUS":-0.15})

C("illusionist",3,"PHANTOM_MEMBRANE:-1","&f","Illusionist",
  ["&fIllusionists&7, masters of deception and","&7misdirection. They confuse foes and","&7strike from impossible angles."],
  {"MAGIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.2,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-3})

C("necromancer",3,"WITHER_SKELETON_SKULL:-1","&8","Necromancer",
  ["&8Necromancers&7, dark mages who command","&7the dead. They raise undead armies","&7and drain the life from foes."],
  {"NECROTIC_DAMAGE_DEALT":0.25,"COOLDOWN_REDUCTION":0.15,"HEALING_BONUS":0.1,"RADIANT_RESISTANCE":-0.15})

C("witch",3,"FERMENTED_SPIDER_EYE:-1","&5","Witch",
  ["&5Witches&7, crafters of potions and curses.","&7They brew devastating concoctions","&7and hex their enemies."],
  {"POISON_DAMAGE_DEALT":0.2,"ALCHEMY_EXP_GAIN":0.2,"COOLDOWN_REDUCTION":0.1,"HEALING_BONUS":0.05})

C("battle_mage",3,"DIAMOND_SWORD:-1","&9","Battle Mage",
  ["&9Battle Mages&7, warriors who combine","&7steel and sorcery. They fight in","&7the thick of battle with magic","&7and blade alike."],
  {"MAGIC_DAMAGE_DEALT":0.15,"MELEE_DAMAGE_DEALT":0.1,"ARMOR_MULTIPLIER_BONUS":0.1,"COOLDOWN_REDUCTION":0.05})

C("pyromancer",3,"BLAZE_POWDER:-1","&c","Pyromancer",
  ["&cPyromancers&7, fire mages of terrible","&7power. They immolate foes and create","&7walls of flame."],
  {"FIRE_DAMAGE_DEALT":0.3,"MAGIC_DAMAGE_DEALT":0.1,"COOLDOWN_REDUCTION":0.1,"FREEZING_RESISTANCE":-0.15})

C("cryomancer",3,"PACKED_ICE:-1","&b","Cryomancer",
  ["&bCryomancers&7, ice mages who freeze","&7all they touch. They control the","&7battlefield with walls of ice."],
  {"FREEZING_DAMAGE_DEALT":0.3,"MAGIC_DAMAGE_DEALT":0.1,"FREEZING_RESISTANCE":0.15,"FIRE_RESISTANCE":-0.15})

C("storm_caller",3,"CONDUIT:-1","&9","Stormcaller",
  ["&9Stormcallers&7, lightning mages who","&7call down the fury of the heavens.","&7Their storms devastate all foes."],
  {"LIGHTNING_DAMAGE_DEALT":0.3,"RANGED_DAMAGE_DEALT":0.1,"MOVEMENT_SPEED_BONUS":0.1,"ARMOR_MULTIPLIER_BONUS":-0.1})

# Group 4 - Healing/Support
C("sage",4,"GOLDEN_APPLE:-1","&e","Sage",
  ["&eSages&7, wise healers who command","&7restorative magic. They mend wounds","&7and provide wisdom to allies."],
  {"HEALING_BONUS":0.3,"RADIANT_DAMAGE_DEALT":0.1,"COOLDOWN_REDUCTION":0.15,"ARMOR_MULTIPLIER_BONUS":0.05})

C("apothecary",4,"BREWING_STAND:-1","&a","Apothecary",
  ["&aApothecaries&7, potion masters who heal","&7with alchemical brews. Their potions","&7are stronger and more potent."],
  {"HEALING_BONUS":0.25,"ALCHEMY_EXP_GAIN":0.2,"ALCHEMY_QUALITY_GENERAL":20,"COOLDOWN_REDUCTION":0.1})

C("battle_medic",4,"REDSTONE:-1","&c","Battle Medic",
  ["&cBattle Medics&7, combat healers who","&7fight on the front lines. They","&7heal allies while dealing damage."],
  {"HEALING_BONUS":0.2,"MELEE_DAMAGE_DEALT":0.1,"ARMOR_MULTIPLIER_BONUS":0.1,"RADIANT_DAMAGE_DEALT":0.1})

C("oracle",4,"EYE_OF_ENDER:-1","&d","Oracle",
  ["&dOracles&7, seers who glimpse the future.","&7They guide allies with prescient","&7knowledge and divine power."],
  {"HEALING_BONUS":0.2,"COOLDOWN_REDUCTION":0.2,"LUCK_BONUS":0.15,"CRIT_CHANCE":0.05})

C("chanter",4,"NOTE_BLOCK:-1","&b","Chanter",
  ["&bChanters&7, speakers of power words.","&7Their chants buff allies and weaken","&7foes with arcane resonance."],
  {"HEALING_BONUS":0.15,"MAGIC_DAMAGE_DEALT":0.1,"COOLDOWN_REDUCTION":0.15,"DODGE_CHANCE":0.1})

C("priest",4,"GOLDEN_APPLE:-1","&e","Priest",
  ["&ePriests&7, devout healers who channel","&7divine power. Their prayers mend","&7wounds and shield allies from harm."],
  {"HEALING_BONUS":0.3,"RADIANT_RESISTANCE":0.15,"ARMOR_MULTIPLIER_BONUS":0.1,"RADIANT_DAMAGE_DEALT":0.1})

C("spirit_walker",4,"TOTEM_OF_UNDYING:-1","&3","Spirit Walker",
  ["&3Spirit Walkers&7, shamans who walk between","&7the living and spirit worlds. They","&7heal with spirit magic."],
  {"HEALING_BONUS":0.2,"NECROTIC_RESISTANCE":0.15,"COOLDOWN_REDUCTION":0.15,"MAGIC_DAMAGE_DEALT":0.1})

C("life_binder",4,"HEART_OF_THE_SEA:-1","&a","Life Binder",
  ["&aLife Binders&7, mages of vital energy.","&7They tether life force and redirect","&7it to heal or harm."],
  {"HEALING_BONUS":0.25,"MAGIC_DAMAGE_DEALT":0.1,"HEALTH_BONUS":3,"ARMOR_MULTIPLIER_BONUS":0.05})

C("confessor",4,"BOOK:-1","&7","Confessor",
  ["&7Confessors&7, spiritual advisors who","&7absorb the pain of others. They","&7sacrifice their own health to","&7heal allies."],
  {"HEALING_BONUS":0.35,"HEALTH_BONUS":-3,"ARMOR_MULTIPLIER_BONUS":0.1,"COOLDOWN_REDUCTION":0.1})

# Group 5 - Tank/Defense
C("sentinel",5,"SHIELD:-1","&e","Sentinel",
  ["&eSentinels&7, watchful guardians who","&7protect allies at all costs. They","&7are the bulwark against evil."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"DAMAGE_RESISTANCE":0.15,"HEALTH_BONUS":5,"KNOCKBACK_RESISTANCE":0.15})

C("bulwark",5,"SHIELD:-1","&7","Bulwark",
  ["&7Bulwarks&7, immovable walls of defense.","&7They stand firm against any assault","&7and cannot be moved."],
  {"ARMOR_MULTIPLIER_BONUS":0.25,"KNOCKBACK_RESISTANCE":0.3,"HEALTH_BONUS":5,"MOVEMENT_SPEED_BONUS":-0.1})

C("guardian",5,"IRON_CHESTPLATE:-1","&e","Guardian",
  ["&eGuardians&7, devoted protectors who","&7shield the weak. Their defensive","&7magic makes them nearly unkillable."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"HEALING_BONUS":0.15,"HEALTH_BONUS":5,"DAMAGE_RESISTANCE":0.1})

C("fortress",5,"STONE_BRICKS:-1","&8","Fortress",
  ["&8Fortresses&7, living walls of stone and","&7steel. They absorb tremendous damage","&7and barely flinch."],
  {"ARMOR_MULTIPLIER_BONUS":0.3,"KNOCKBACK_RESISTANCE":0.25,"HEALTH_BONUS":8,"MOVEMENT_SPEED_BONUS":-0.15})

C("aegis",5,"GOLDEN_CHESTPLATE:-1","&e","Aegis",
  ["&eAegis&7, holy shield-bearers who combine","&7defense with divine power. Their","&7shields glow with sacred energy."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"RADIANT_RESISTANCE":0.15,"HEALING_BONUS":0.1,"HEALTH_BONUS":3})

C("stone_warden",5,"DEEPSLATE:-1","&7","Stone Warden",
  ["&7Stone Wardens&7, earth-bound guardians","&7who draw power from the ground. They","&7are nearly impossible to topple."],
  {"ARMOR_MULTIPLIER_BONUS":0.25,"DAMAGE_RESISTANCE":0.2,"KNOCKBACK_RESISTANCE":0.2,"MOVEMENT_SPEED_BONUS":-0.15})

C("ironclad",5,"IRON_CHESTPLATE:-1","&7","Ironclad",
  ["&7Ironclad&7, warriors wrapped in layers","&7of iron. They shrug off blows that","&7would fell lesser fighters."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"DAMAGE_RESISTANCE":0.15,"HEALTH_BONUS":5,"MOVEMENT_SPEED_BONUS":-0.1})

C("phalanx",5,"SHIELD:-1","&e","Phalanx",
  ["&ePhalanx&7, formation fighters who are","&7stronger together. Their defensive","&7coordination makes them formidable."],
  {"ARMOR_MULTIPLIER_BONUS":0.2,"KNOCKBACK_RESISTANCE":0.2,"DAMAGE_RESISTANCE":0.1,"HEALTH_BONUS":3})

C("colossus",5,"NETHERITE_CHESTPLATE:-1","&4","Colossus",
  ["&4Colossi&7, towering defensive warriors","&7of incredible endurance. They absorb","&7punishment meant for armies."],
  {"HEALTH_BONUS":10,"ARMOR_MULTIPLIER_BONUS":0.2,"KNOCKBACK_RESISTANCE":0.25,"MOVEMENT_SPEED_BONUS":-0.2})

# Group 6 - Stealth/Assassin
C("shadow",6,"BLACK_DYE:-1","&8","Shadow",
  ["&8Shadows&7, masters of stealth who strike","&7from the darkness. They deal lethal","&7damage before vanishing."],
  {"MELEE_DAMAGE_DEALT":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.25,"DODGE_CHANCE":0.15,"CRIT_CHANCE":0.1,"ARMOR_MULTIPLIER_BONUS":-0.1})

C("infiltrator",6,"LEATHER_HELMET:-1","&7","Infiltrator",
  ["&7Infiltrators&7, spies who slip past any","&7defense. They are experts of disguise","&7and deadly ambush."],
  {"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"CRIT_CHANCE":0.15,"DODGE_CHANCE":0.1,"MELEE_DAMAGE_DEALT":0.1})

C("nightblade",6,"NETHERITE_SWORD:-1","&5","Nightblade",
  ["&5Nightblades&7, warriors of shadow and","&7steel. They fight with dark magic","&7infused in every strike."],
  {"MELEE_DAMAGE_DEALT":0.15,"NECROTIC_DAMAGE_DEALT":0.1,"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"CRIT_CHANCE":0.1})

C("whisper",6,"STRING:-1","&7","Whisper",
  ["&7Whispers&7, silent killers who leave no","&7trace. Their strikes are precise and","&7utterly deadly."],
  {"SNEAK_MOVEMENT_SPEED_BONUS":0.25,"CRIT_CHANCE":0.2,"CRIT_DAMAGE":0.15,"HEALTH_BONUS":-3})

C("cutthroat",6,"GOLDEN_SWORD:-1","&c","Cutthroat",
  ["&cCutthroats&7, ruthless assassins who","&7fight dirty. They deal massive","&7damage in close quarters."],
  {"MELEE_DAMAGE_DEALT":0.2,"CRIT_CHANCE":0.15,"BLEED_DAMAGE":0.15,"ARMOR_MULTIPLIER_BONUS":-0.1})

C("phantom",6,"PHANTOM_MEMBRANE:-1","&f","Phantom",
  ["&fPhantoms&7, ghost-like assassins who","&7seem to disappear. They strike from","&7nowhere and vanish instantly."],
  {"DODGE_CHANCE":0.2,"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"CRIT_CHANCE":0.1,"MAGIC_DAMAGE_DEALT":0.1})

C("renegade",6,"WITHER_SKELETON_SKULL:-1","&8","Renegade",
  ["&8Renegades&7, outlaws who fight outside","&7the law. They use every dirty trick","&7to gain the upper hand."],
  {"MELEE_DAMAGE_DEALT":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"DODGE_CHANCE":0.15,"CRIT_DAMAGE":0.1})

C("deadeye",6,"SPECTRAL_ARROW:-1","&e","Deadeye",
  ["&eDeadeyes&7, ranged assassins who strike","&7from the shadows. Their shots never","&7miss and always find the heart."],
  {"RANGED_DAMAGE_DEALT":0.2,"CRIT_CHANCE":0.2,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"HEALTH_BONUS":-3})

C("scoundrel",6,"TRIPWIRE_HOOK:-1","&a","Scoundrel",
  ["&aScoundrels&7, rogues who use traps and","&7tricks. They control the battlefield","&7with cunning and treachery."],
  {"CRIT_CHANCE":0.15,"DODGE_CHANCE":0.15,"POISON_DAMAGE_DEALT":0.1,"LUCK_BONUS":0.15})

C("trickster",6,"SLIME_BALL:-1","&d","Trickster",
  ["&dTricksters&7, magical rogues who combine","&7spell and stealth. They confound foes","&7with illusions and backstab."],
  {"MAGIC_DAMAGE_DEALT":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.15,"DODGE_CHANCE":0.15,"CRIT_CHANCE":0.1})

# Group 7 - Summoner/Commander
C("beast_tamer",7,"LEAD:-1","&6","Beast Tamer",
  ["&6Beast Tamers&7, masters who command","&7wild creatures. Their animal allies","&7fight alongside them in battle."],
  {"MELEE_DAMAGE_DEALT":0.1,"HEALTH_BONUS":5,"DODGE_CHANCE":0.1,"FARMING_DROP_MULTIPLIER":0.15})

C("undead_commander",7,"WITHER_SKELETON_SKULL:-1","&8","Undead Commander",
  ["&8Undead Commanders&7, necromancers who lead","&7armies of the dead. They raise","&7fallen foes to fight for them."],
  {"NECROTIC_DAMAGE_DEALT":0.2,"HEALTH_BONUS":5,"KNOCKBACK_RESISTANCE":0.15,"ARMOR_MULTIPLIER_BONUS":0.1})

C("golemancer",7,"IRON_BLOCK:-1","&7","Golemancer",
  ["&7Golemancers&7, mages who create and","&7command stone and iron golems. Their","&7constructs are formidable defenders."],
  {"HEALTH_BONUS":5,"ARMOR_MULTIPLIER_BONUS":0.15,"DAMAGE_RESISTANCE":0.1,"MAGIC_DAMAGE_DEALT":0.1})

C("banneret",7,"BANNER:-1","&e","Banneret",
  ["&eBannerets&7, rallying commanders who","&7inspire allies with their presence.","&7Their battle cries strengthen the","&7entire party."],
  {"HEALTH_BONUS":3,"ARMOR_MULTIPLIER_BONUS":0.1,"DAMAGE_RESISTANCE":0.1,"CRIT_CHANCE":0.1})

C("warlord",7,"NETHERITE_AXE:-1","&4","Warlord",
  ["&4Warlords&7, military leaders who dominate","&7the battlefield. They boost ally","&7morale and crush enemy resolve."],
  {"MELEE_DAMAGE_DEALT":0.15,"HEALTH_BONUS":5,"ARMOR_MULTIPLIER_BONUS":0.1,"KNOCKBACK_RESISTANCE":0.15})

C("commander",7,"GOLDEN_SWORD:-1","&e","Commander",
  ["&eCommanders&7, strategic leaders who","&7coordinate allied forces. Their tactical","&7brilliance turns the tide of battle."],
  {"DAMAGE_DEALT":0.1,"DAMAGE_RESISTANCE":0.1,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":3})

C("ritualist",7,"ENCHANTMENT_TABLE:-1","&5","Ritualist",
  ["&5Ritualists&7, mages who summon powerful","&7entities through dark ceremonies.","&7Their rituals grant immense power."],
  {"MAGIC_DAMAGE_DEALT":0.2,"COOLDOWN_REDUCTION":0.15,"NECROTIC_DAMAGE_DEALT":0.1,"ARMOR_MULTIPLIER_BONUS":-0.1})

C("binder",7,"LEAD:-1","&8","Binder",
  ["&8Binders&7, mages who chain and control","&7entities. They bind spirits to their","&7will and force them to fight."],
  {"NECROTIC_DAMAGE_DEALT":0.15,"MAGIC_DAMAGE_DEALT":0.15,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":3})

# Group 8 - Hybrid
C("spellthief",8,"DIAMOND_SWORD:-1","&5","Spellthief",
  ["&5Spellthieves&7, rogues who steal and use","&7enemy magic. They combine spell","&7and blade with deadly efficiency."],
  {"MELEE_DAMAGE_DEALT":0.1,"MAGIC_DAMAGE_DEALT":0.1,"DODGE_CHANCE":0.15,"COOLDOWN_REDUCTION":0.1})

C("blade_mage",8,"DIAMOND_SWORD:-1","&9","Blade Mage",
  ["&9Blade Mages&7, warriors who infuse their","&7weapons with magic. Each strike","&7carries both steel and sorcery."],
  {"MELEE_DAMAGE_DEALT":0.15,"MAGIC_DAMAGE_DEALT":0.1,"CRIT_CHANCE":0.1,"COOLDOWN_REDUCTION":0.05})

C("runic_warrior",8,"ENCHANTED_BOOK:-1","&6","Runic Warrior",
  ["&6Runic Warriors&7, fighters inscribed with","&7battle runes. Their runes grant","&7both offensive and defensive power."],
  {"MELEE_DAMAGE_DEALT":0.1,"ARMOR_MULTIPLIER_BONUS":0.1,"MAGIC_DAMAGE_DEALT":0.1,"HEALTH_BONUS":3})

C("hexblade",8,"WITHER_SKELETON_SKULL:-1","&5","Hexblade",
  ["&5Hexblades&7, warriors who channel curses","&7through their blades. They weaken","&7foes with dark enchantments."],
  {"MELEE_DAMAGE_DEALT":0.15,"NECROTIC_DAMAGE_DEALT":0.1,"COOLDOWN_REDUCTION":0.1,"HEALING_BONUS":0.1})

C("arcane_archer",8,"BOW:-1","&b","Arcane Archer",
  ["&bArcane Archers&7, mages who enchant their","&7arrows with spells. Each shot carries","&7devastating magical force."],
  {"RANGED_DAMAGE_DEALT":0.15,"MAGIC_DAMAGE_DEALT":0.1,"CRIT_CHANCE":0.1,"CRIT_DAMAGE":0.1})

C("battle_cleric",8,"GOLDEN_APPLE:-1","&e","Battle Cleric",
  ["&eBattle Clerics&7, holy warriors who fight","&7and heal in equal measure. They","&7are versatile front-line support."],
  {"HEALING_BONUS":0.15,"MELEE_DAMAGE_DEALT":0.1,"RADIANT_DAMAGE_DEALT":0.1,"ARMOR_MULTIPLIER_BONUS":0.1})

C("spirit_knight",8,"TOTEM_OF_UNDYING:-1","&3","Spirit Knight",
  ["&3Spirit Knights&7, warriors empowered by","&7ancestral spirits. They fight with","&7otherworldly strength and resilience."],
  {"MELEE_DAMAGE_DEALT":0.1,"NECROTIC_DAMAGE_DEALT":0.1,"HEALTH_BONUS":5,"ARMOR_MULTIPLIER_BONUS":0.1})

C("runepriest",8,"ENCHANTED_BOOK:-1","&6","Runepriest",
  ["&6Runepriests&7, mages who inscribe runes","&7of power. Their rune magic enhances","&7all aspects of combat."],
  {"MAGIC_DAMAGE_DEALT":0.15,"HEALING_BONUS":0.1,"ENCHANTING_EXP_GAIN":0.15,"COOLDOWN_REDUCTION":0.1})

C("mystic",8,"EXPERIENCE_BOTTLE:-1","&d","Mystic",
  ["&dMystics&7, spiritual warriors who channel","&7inner power. They achieve transcendence","&7through meditation and combat."],
  {"MAGIC_DAMAGE_DEALT":0.1,"HEALING_BONUS":0.1,"DODGE_CHANCE":0.15,"COOLDOWN_REDUCTION":0.1})

C("adept",8,"DIAMOND_SWORD:-1","&e","Adept",
  ["&eAdepts&7, versatile fighters who master","&7multiple disciplines. They adapt to","&7any situation with ease."],
  {"DAMAGE_DEALT":0.1,"ARMOR_MULTIPLIER_BONUS":0.1,"COOLDOWN_REDUCTION":0.1,"HEALTH_BONUS":3})

# Group 9 - Crafting/Gathering
C("artificer",9,"CRAFTING_TABLE:-1","&b","Artificer",
  ["&bArtificers&7, magical craftsmen who create","&7enchanted items and devices. Their","&7creations are of superior quality."],
  {"CRAFTING_TIME_REDUCTION":0.2,"ENCHANTING_QUALITY":20,"LUCK_BONUS":0.1,"COOKING_SPEED_BONUS":0.15})

C("jeweler",9,"DIAMOND:-1","&b","Jeweler",
  ["&bJewelers&7, masters of precious stones","&7and metals. They craft items of","&7unmatched beauty and power."],
  {"SMITHING_QUALITY_GENERAL":25,"ENCHANTING_QUALITY":15,"LUCK_BONUS":0.15})

C("tinker",9,"REDSTONE:-1","&6","Tinker",
  ["&6Tinkerers&7, inventors who create useful","&7gadgets and improve existing tools.","&7They make everything work better."],
  {"DIG_SPEED":0.2,"MINING_EXP_GAIN":0.15,"CRAFTING_TIME_REDUCTION":0.15,"DURABILITY_BONUS":0.15})

C("herbalist",4,"OXEYE_DAISY:-1","&a","Herbalist",
  ["&aHerbalists&7, plant experts who brew","&7potions and remedies from gathered","&7herbs. Their knowledge of nature is","&7unmatched."],
  {"ALCHEMY_EXP_GAIN":0.25,"FARMING_EXP_GAIN":0.2,"FARMING_DROP_MULTIPLIER":0.15,"POISON_RESISTANCE":0.1})

C("skinner",9,"LEATHER:-1","&6","Skinner",
  ["&6Skinners&7, experts of animal hides","&7and leather. They harvest resources","&7from beasts with practiced skill."],
  {"FARMING_DROP_MULTIPLIER":0.2,"MINING_DROP_MULTIPLIER":0.1,"LUCK_BONUS":0.1,"DURABILITY_BONUS":0.1})

C("lumberjack",9,"WOODEN_AXE:-1","&6","Lumberjack",
  ["&6Lumberjacks&7, masters of the forest who","&7fell trees with incredible speed. They","&7are the backbone of construction."],
  {"WOODCUTTING_EXP_GAIN":0.3,"DIG_SPEED":0.2,"MINING_EXP_GAIN":0.1,"HEALTH_BONUS":3})

C("mason",9,"STONE_PICKAXE:-1","&7","Mason",
  ["&7Masons&7, stone experts who shape rock","&7with ease. Their crafting skill is","&7unmatched in masonry."],
  {"MINING_EXP_GAIN":0.25,"DIG_SPEED":0.2,"MINING_DROP_MULTIPLIER":0.15,"CRAFTING_TIME_REDUCTION":0.1})

C("weaver",9,"STRING:-1","&d","Weaver",
  ["&dWeavers&7, textile artists who create","&7fine clothing and armor. Their crafted","&7garments are of superior quality."],
  {"CRAFTING_TIME_REDUCTION":0.2,"ENCHANTING_QUALITY":10,"DURABILITY_BONUS":0.2,"LUCK_BONUS":0.05})

C("brewer",9,"BREWING_STAND:-1","&3","Brewer",
  ["&3Brewers&7, masters of fermentation and","&7alchemy. They create potent brews","&7that enhance all who drink them."],
  {"ALCHEMY_EXP_GAIN":0.2,"ALCHEMY_QUALITY_GENERAL":20,"BREWING_SPEED_BONUS":0.25,"COOKING_SPEED_BONUS":0.15})

C("cartographer",9,"MAP:-1","&e","Cartographer",
  ["&eCartographers&7, mapmakers who chart the","&7unknown. Their knowledge of the world","&7grants exploration advantages."],
  {"LUCK_BONUS":0.2,"GLOBAL_EXP_GAIN":0.1,"FISHING_LUCK":2,"DIG_SPEED":0.1})

# Group 10 - Special/Unique
C("fate_weaver",10,"CLOCK:-1","&d","Fate Weaver",
  ["&dFate Weavers&7, mages who manipulate the","&7threads of destiny. They alter","&7probabilities and bend luck."],
  {"LUCK_BONUS":0.25,"COOLDOWN_REDUCTION":0.15,"CRIT_CHANCE":0.1,"DODGE_CHANCE":0.1})

C("void_walker",10,"OBSIDIAN:-1","&5","Void Walker",
  ["&5Void Walkers&7, dimensional travelers who","&7harness the power of the void. They","&7warp reality itself."],
  {"MAGIC_DAMAGE_DEALT":0.2,"DODGE_CHANCE":0.2,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-5})

C("time_mage",10,"CLOCK:-1","&e","Time Mage",
  ["&eTime Mages&7, chronomancers who slow and","&7hasten time. They control the pace","&7of battle with temporal magic."],
  {"COOLDOWN_REDUCTION":0.25,"MAGIC_DAMAGE_DEALT":0.15,"DODGE_CHANCE":0.1,"HEALTH_BONUS":-3})

C("dreamwalker",10,"COCOA_BEANS:-1","&d","Dreamwalker",
  ["&dDreamwalkers&7, beings who traverse the","&7realm of dreams. They wield illusory","&7magic and blur reality."],
  {"MAGIC_DAMAGE_DEALT":0.2,"DODGE_CHANCE":0.15,"COOLDOWN_REDUCTION":0.15,"HEALTH_BONUS":-4})

C("soul_binder",10,"SOUL_LANTERN:-1","&8","Soul Binder",
  ["&8Soul Binders&7, mages who bind and", "&7manipulate souls. They drain life","&7force and weaponize it against foes."],
  {"NECROTIC_DAMAGE_DEALT":0.25,"HEALING_BONUS":0.15,"COOLDOWN_REDUCTION":0.1,"RADIANT_RESISTANCE":-0.15})

C("starweaver",10,"NETHER_STAR:-1","&e","Starweaver",
  ["&eStarweavers&7, cosmic mages who channel","&7the power of stars. Their spells","&7are woven from starlight."],
  {"MAGIC_DAMAGE_DEALT":0.2,"RADIANT_DAMAGE_DEALT":0.15,"CRIT_DAMAGE":0.15,"COOLDOWN_REDUCTION":0.1})

C("chaos_mage",10,"DRAGON_BREATH:-1","&5","Chaos Mage",
  ["&5Chaos Mages&7, wild sorcerers who channel","&7pure entropy. Their spells are","&7unpredictable but devastating."],
  {"MAGIC_DAMAGE_DEALT":0.2,"FIRE_DAMAGE_DEALT":0.1,"LIGHTNING_DAMAGE_DEALT":0.1,"FREEZING_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-3})

C("blood_mage",10,"REDSTONE:-1","&4","Blood Mage",
  ["&4Blood Mages&7, dark sorcerers who fuel","&7spells with their own life force.","&7Their power has no limits,","&7but their bodies pay the price."],
  {"MAGIC_DAMAGE_DEALT":0.25,"COOLDOWN_REDUCTION":0.2,"NECROTIC_DAMAGE_DEALT":0.1,"HEALTH_BONUS":-8})

C("thaumaturge",10,"ENCHANTED_GOLDEN_APPLE:-1","&d","Thaumaturge",
  ["&dThaumaturges&7, miracle workers who","&7bend the laws of nature. Their","&7miracles can heal or destroy."],
  {"MAGIC_DAMAGE_DEALT":0.15,"HEALING_BONUS":0.2,"COOLDOWN_REDUCTION":0.15,"RADIANT_DAMAGE_DEALT":0.1})

C("geomancer",3,"STONE:-1","&6","Geomancer",
  ["&6Geomancers&7, earth mages who command","&7stone and soil. They create barriers","&7and crush foes with the earth."],
  {"BLUDGEONING_DAMAGE_DEALT":0.2,"ARMOR_MULTIPLIER_BONUS":0.15,"DAMAGE_RESISTANCE":0.1,"MAGIC_DAMAGE_DEALT":0.1})

C("warden_of_woods",4,"OAK_LEAVES:-1","&2","Warden of Woods",
  ["&2Wardens of the Woods&7, nature guardians","&7who protect the ancient forests.","&7They heal and fight with equal skill."],
  {"HEALING_BONUS":0.2,"MELEE_DAMAGE_DEALT":0.1,"FARMING_EXP_GAIN":0.15,"POISON_RESISTANCE":0.15})

C("shadow_blade",6,"NETHERITE_SWORD:-1","&8","Shadow Blade",
  ["&8Shadow Blades&7, rogues who fuse shadow","&7magic with bladework. They cut through","&7reality itself with each strike."],
  {"MELEE_DAMAGE_DEALT":0.15,"SNEAK_MOVEMENT_SPEED_BONUS":0.2,"NECROTIC_DAMAGE_DEALT":0.1,"CRIT_CHANCE":0.1})

C("sky_knight",1,"ELYTRA:-1","&b","Sky Knight",
  ["&bSky Knights&7, aerial warriors who fight","&7on the wing. They dive-bomb foes","&7with devastating force."],
  {"MELEE_DAMAGE_DEALT":0.15,"RANGED_DAMAGE_DEALT":0.1,"MOVEMENT_SPEED_BONUS":0.15,"FALLING_RESISTANCE":0.2})

C("runesmith",9,"ENCHANTED_BOOK:-1","&6","Runesmith",
  ["&6Runesmiths&7, magical blacksmiths who","&7inscribe runes into their creations.","&7Their items glow with arcane power."],
  {"SMITHING_QUALITY_GENERAL":25,"ENCHANTING_QUALITY":20,"CRAFTING_TIME_REDUCTION":0.15,"DURABILITY_BONUS":0.15})

assert len(CLASS_DEFS) == 100, f"Expected 100 classes, got {len(CLASS_DEFS)}"

# ─── GENERATE OUTPUT ────────────────────────────────────────────────────────

def generate():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate races_new.yml
    race_lines = []
    for i, (name, icon, color, display, lore, stats) in enumerate(RACE_DEFS):
        pos = 50 + i
        entry = make_race_yaml(name, pos, icon, color, display, lore, stats)
        race_lines.append(entry)

    with open(os.path.join(script_dir, "races_new.yml"), "w", encoding="utf-8") as f:
        f.write("# 200 New Races for ValhallaRaces\n")
        f.write("# Append these to the end of races.yml under the 'races:' section\n\n")
        f.write("\n".join(race_lines))
        f.write("\n")

    print(f"Created races_new.yml with {len(RACE_DEFS)} new races")

    # Generate classes_new.yml
    class_lines = []
    for i, (name, grp, icon, color, display, lore, stats) in enumerate(CLASS_DEFS):
        pos = 50 + i
        entry = make_class_yaml(name, grp, pos, icon, color, display, lore, stats)
        class_lines.append(entry)

    with open(os.path.join(script_dir, "classes_new.yml"), "w", encoding="utf-8") as f:
        f.write("# 100 New Classes for ValhallaRaces\n")
        f.write("# Append these to the end of classes.yml under the 'classes:' section\n\n")
        f.write("\n".join(class_lines))
        f.write("\n")

    print(f"Created classes_new.yml with {len(CLASS_DEFS)} new classes")

    # Generate website_data.json
    existing_races_data = {
        "dwarf": {"display_name": "Dwarf", "color": "&e", "category": "Humanoid"},
        "human": {"display_name": "Human", "color": "&a", "category": "Humanoid"},
        "elf": {"display_name": "Elf", "color": "&b", "category": "Fey"},
        "orc": {"display_name": "Orc", "color": "&2", "category": "Humanoid"},
        "undead": {"display_name": "Undead", "color": "&7", "category": "Undead"},
        "vampire": {"display_name": "Vampire", "color": "&c", "category": "Undead"},
        "werewolf": {"display_name": "Werewolf", "color": "&6", "category": "Beast"},
        "beastkin": {"display_name": "Beastkin", "color": "&d", "category": "Beast"},
        "fairy": {"display_name": "Fairy", "color": "&b", "category": "Fey"},
        "brethren": {"display_name": "Brethren", "color": "&a", "category": "Humanoid"},
        "hafis": {"display_name": "Hafis", "color": "&a", "category": "Humanoid"},
        "dragonkin": {"display_name": "Dragonkin", "color": "&c", "category": "Dragon"},
        "kitsune": {"display_name": "Kitsune", "color": "&d", "category": "Beast"},
        "titanborn": {"display_name": "Titanborn", "color": "&9", "category": "Giant"},
        "drow": {"display_name": "Drow", "color": "&5", "category": "Fey"},
        "celestial": {"display_name": "Celestial", "color": "&e", "category": "Divine"},
        "abyssal": {"display_name": "Abyssal", "color": "&4", "category": "Demonic"},
        "naga": {"display_name": "Naga", "color": "&2", "category": "Beast"},
        "djinn": {"display_name": "Djinn", "color": "&b", "category": "Elemental"},
        "satyr": {"display_name": "Satyr", "color": "&6", "category": "Fey"},
        "treant": {"display_name": "Treant", "color": "&2", "category": "Nature"},
        "dryad": {"display_name": "Dryad", "color": "&a", "category": "Nature"},
        "avian": {"display_name": "Avian", "color": "&f", "category": "Beast"},
        "tortle": {"display_name": "Tortle", "color": "&a", "category": "Beast"},
        "golemkin": {"display_name": "Golemkin", "color": "&7", "category": "Construct"},
        "frostborne": {"display_name": "Frostborne", "color": "&b", "category": "Elemental"},
        "wraith": {"display_name": "Wraith", "color": "&f", "category": "Undead"},
    }

    existing_classes_data = {
        "warrior": {"display_name": "Warrior", "color": "&c", "group": 1, "category": "Melee"},
        "barbarian": {"display_name": "Barbarian", "color": "&c", "group": 1, "category": "Melee"},
        "ranger": {"display_name": "Ranger", "color": "&c", "group": 1, "category": "Ranged"},
        "alchemist": {"display_name": "Alchemist", "color": "&d", "group": 2, "category": "Crafting"},
        "enchanter": {"display_name": "Enchanter", "color": "&b", "group": 2, "category": "Magic"},
        "blacksmith": {"display_name": "Blacksmith", "color": "&a", "group": 2, "category": "Crafting"},
        "miner": {"display_name": "Miner", "color": "&e", "group": 3, "category": "Gathering"},
        "farmer": {"display_name": "Farmer-Fisherman", "color": "&e", "group": 3, "category": "Gathering"},
        "terraformer": {"display_name": "Terraformer", "color": "&e", "group": 3, "category": "Gathering"},
        "berserker": {"display_name": "Berserker", "color": "&c", "group": 1, "category": "Melee"},
        "paladin": {"display_name": "Paladin", "color": "&e", "group": 1, "category": "Melee"},
        "death_knight": {"display_name": "Death Knight", "color": "&8", "group": 1, "category": "Melee"},
        "spellbreaker": {"display_name": "Spellbreaker", "color": "&5", "group": 1, "category": "Melee"},
        "assassin": {"display_name": "Assassin", "color": "&7", "group": 1, "category": "Stealth"},
        "monk": {"display_name": "Monk", "color": "&e", "group": 1, "category": "Melee"},
        "mage": {"display_name": "Mage", "color": "&b", "group": 2, "category": "Magic"},
        "warlock": {"display_name": "Warlock", "color": "&5", "group": 2, "category": "Magic"},
        "cleric": {"display_name": "Cleric", "color": "&e", "group": 2, "category": "Healer"},
        "druid": {"display_name": "Druid", "color": "&2", "group": 2, "category": "Nature"},
        "shaman": {"display_name": "Shaman", "color": "&3", "group": 2, "category": "Magic"},
        "void_knight": {"display_name": "Void Knight", "color": "&5", "group": 2, "category": "Melee"},
        "gunslinger": {"display_name": "Gunslinger", "color": "&6", "group": 3, "category": "Ranged"},
        "samurai": {"display_name": "Samurai", "color": "&c", "group": 3, "category": "Melee"},
        "ninja": {"display_name": "Ninja", "color": "&8", "group": 3, "category": "Stealth"},
        "bard": {"display_name": "Bard", "color": "&d", "group": 3, "category": "Support"},
        "warden": {"display_name": "Warden", "color": "&2", "group": 3, "category": "Defense"},
        "spellblade": {"display_name": "Spellblade", "color": "&b", "group": 3, "category": "Hybrid"},
    }

    race_categories = {
        "Elemental": ["fire_elemental","water_elemental","earth_elemental","air_elemental",
            "lightning_elemental","magma_lord","stormborn","tidal_dancer","glacial","volcanic",
            "dust_wraith","mistwalker","ashborn","cinder_spark","tempest_lord","sky_sovereign",
            "inferno_touched","void_essence","ember_knight","frost_kin","ember_soul",
            "dust_djinn","storm_caller","storm_spirit","sandstorm_beast"],
        "Beast": ["wolf_blooded","bear_folk","hawk_kin","serpent_blooded","spider_kin",
            "raven_folk","fox_blooded","stag_folk","shark_kin","lion_folk","owlkin",
            "raptor_kin","boar_folk","bat_folk","lupine_hunter","serpent_sages","wild_kin"],
        "Undead": ["lich","banshee","revenant","phantom","shade","specter","poltergeist",
            "ghost_kin","zombie_forged","bone_colossus","shadow_drake","soul_echo"],
        "Divine": ["seraph","archon","demigod","solar_angel","lunar_kin","starborn",
            "cherub","aasimar","aether_born"],
        "Demonic": ["imp","cambion","pit_fiend","balor","tiefling","shadow_demon",
            "nightmare","void_fiend","void_touched"],
        "Nature/Fey": ["sprite","pixie","centaur","sylph","gnome","leshy","mushroom_folk",
            "treant_sprout","faun","mossling","thornweaver"],
        "Aquatic": ["merfolk","sea_elf","kelpie","sahuagin","triton","deep_one",
            "abyssal_serpent","pearl_mermaid","abyssal_kraken"],
        "Construct": ["automaton","warforged","clockwork","crystal_golem","construct",
            "soulforged","iron_bound","ironheart"],
        "Giant": ["ogre","troll","jotun","cyclops","firbolg","goliath","half_giant",
            "verdant_giant","stone_warden"],
        "Exotic": ["astral","ethereal","planar","chrono","rune_carved","dream_walker",
            "null_kin","sand_wraith","blood_mage","rune_sorcerer","crystal_shard",
            "twilight_elf","crystal_nymph"],
        "Dragon": ["ember_drake","storm_dragon","void_serpent","iron_drake","frost_dragon",
            "shadow_drake"],
    }

    class_categories_map = {
        "Melee DPS": ["champion","duelist","marauder","gladiator","lancer","warmonger",
            "reaper","juggernaut","blade_dancer","pit_fighter"],
        "Ranged DPS": ["marksman","hunter","sniper","falconer","ballistae","slinger",
            "arbalist","sharpshooter","beastmaster","trapper"],
        "Magic DPS": ["sorcerer","elementalist","conjurer","illusionist","necromancer",
            "witch","battle_mage","pyromancer","cryomancer"],
        "Healing/Support": ["sage","apothecary","battle_medic","oracle","chanter",
            "priest","spirit_walker","life_binder","confessor","herbalist"],
        "Tank/Defense": ["sentinel","bulwark","guardian","fortress","aegis",
            "stone_warden","ironclad","phalanx","colossus"],
        "Stealth": ["shadow","infiltrator","nightblade","whisper","cutthroat",
            "phantom","renegade","deadeye","scoundrel","trickster"],
        "Summoner/Commander": ["beast_tamer","undead_commander","golemancer","banneret",
            "warlord","commander","ritualist","binder"],
        "Hybrid": ["spellthief","blade_mage","runic_warrior","hexblade","arcane_archer",
            "battle_cleric","spirit_knight","runepriest","mystic","adept"],
        "Crafting/Gathering": ["artificer","jeweler","tinker","skinner","lumberjack",
            "mason","weaver","brewer","cartographer"],
        "Special/Unique": ["fate_weaver","void_walker","time_mage","dreamwalker",
            "soul_binder","starweaver","chaos_mage","blood_mage","thaumaturge",
            "storm_caller"],
    }

    # Merge new race data
    new_races_data = {}
    for name, icon, color, display, lore, stats in RACE_DEFS:
        cat = "Other"
        for c, members in race_categories.items():
            if name in members:
                cat = c
                break
        new_races_data[name] = {
            "display_name": display,
            "color": color,
            "category": cat,
            "stats": {k: v for k, v in stats.items()}
        }

    all_races = {}
    all_races.update({k: {**v, "is_new": False} for k, v in existing_races_data.items()})
    all_races.update({k: {**v, "is_new": True} for k, v in new_races_data.items()})

    # Merge new class data
    new_classes_data = {}
    for name, grp, icon, color, display, lore, stats in CLASS_DEFS:
        cat = "Other"
        for c, members in class_categories_map.items():
            if name in members:
                cat = c
                break
        new_classes_data[name] = {
            "display_name": display,
            "color": color,
            "group": grp,
            "category": cat,
            "stats": {k: v for k, v in stats.items()}
        }

    all_classes = {}
    all_classes.update({k: {**v, "is_new": False} for k, v in existing_classes_data.items()})
    all_classes.update({k: {**v, "is_new": True} for k, v in new_classes_data.items()})

    website_data = {
        "races": {
            "total": len(all_races),
            "existing": len(existing_races_data),
            "new": len(new_races_data),
            "categories": race_categories,
            "entries": all_races
        },
        "classes": {
            "total": len(all_classes),
            "existing": len(existing_classes_data),
            "new": len(new_classes_data),
            "categories": class_categories_map,
            "entries": all_classes
        },
        "stats_used": {
            "combat": ["MELEE_DAMAGE_DEALT","RANGED_DAMAGE_DEALT","UNARMED_DAMAGE_DEALT",
                "DAMAGE_DEALT","MAGIC_DAMAGE_DEALT","FIRE_DAMAGE_DEALT","FREEZING_DAMAGE_DEALT",
                "LIGHTNING_DAMAGE_DEALT","NECROTIC_DAMAGE_DEALT","RADIANT_DAMAGE_DEALT",
                "POISON_DAMAGE_DEALT","BLUDGEONING_DAMAGE_DEALT","EXPLOSION_DAMAGE_DEALT"],
            "defense": ["ARMOR_MULTIPLIER_BONUS","DAMAGE_RESISTANCE","MELEE_RESISTANCE",
                "PROJECTILE_RESISTANCE","MAGIC_RESISTANCE","FIRE_RESISTANCE","FREEZING_RESISTANCE",
                "LIGHTNING_RESISTANCE","NECROTIC_RESISTANCE","RADIANT_RESISTANCE",
                "POISON_RESISTANCE","EXPLOSION_RESISTANCE","KNOCKBACK_RESISTANCE",
                "BLEED_RESISTANCE","STUN_RESISTANCE"],
            "health_movement": ["HEALTH_BONUS","MOVEMENT_SPEED_BONUS","SPRINT_MOVEMENT_SPEED_BONUS",
                "SNEAK_MOVEMENT_SPEED_BONUS","JUMP_HEIGHT_MULTIPLIER","FALLING_RESISTANCE",
                "SCALE","DODGE_CHANCE","CRIT_CHANCE","CRIT_DAMAGE"],
            "skills": ["GLOBAL_EXP_GAIN","MINING_EXP_GAIN","WOODCUTTING_EXP_GAIN",
                "FARMING_EXP_GAIN","FISHING_EXP_GAIN","ARCHERY_EXP_GAIN",
                "LIGHT_WEAPONS_EXP_GAIN","HEAVY_WEAPONS_EXP_GAIN","ENCHANTING_EXP_GAIN",
                "ALCHEMY_EXP_GAIN"],
            "utility": ["COOLDOWN_REDUCTION","HEALING_BONUS","HUNGER_SAVE_CHANCE",
                "DURABILITY_BONUS","FARMING_DROP_MULTIPLIER","MINING_DROP_MULTIPLIER",
                "FISHING_LUCK","FISHING_SPEED_MULTIPLIER","DIG_SPEED","LUCK_BONUS"],
            "crafting": ["SMITHING_QUALITY_GENERAL","ALCHEMY_QUALITY_GENERAL",
                "ENCHANTING_QUALITY","BREWING_SPEED_BONUS","CRAFTING_TIME_REDUCTION",
                "COOKING_SPEED_BONUS"]
        }
    }

    with open(os.path.join(script_dir, "website_data.json"), "w", encoding="utf-8") as f:
        json.dump(website_data, f, indent=2, ensure_ascii=False)

    print(f"Created website_data.json with {website_data['races']['total']} races and {website_data['classes']['total']} classes")
    print(f"\nSummary:")
    print(f"  Existing races: {len(existing_races_data)}")
    print(f"  New races:      {len(new_races_data)}")
    print(f"  Total races:    {website_data['races']['total']}")
    print(f"  Existing classes: {len(existing_classes_data)}")
    print(f"  New classes:      {len(new_classes_data)}")
    print(f"  Total classes:    {website_data['classes']['total']}")

if __name__ == "__main__":
    generate()
