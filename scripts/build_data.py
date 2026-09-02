#!/usr/bin/env python3
"""
Builds site data from ValhallaRaces config files.
Reads ../../races.yml and ../../classes.yml, writes ../assets/data/data.json

Usage: run from anywhere; paths are resolved relative to this script.
"""
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
RACES_PATH = SCRIPT_DIR.parent.parent / "races.yml"
CLASSES_PATH = SCRIPT_DIR.parent.parent / "classes.yml"
OUT_PATH = ROOT / "assets" / "data" / "data.json"

try:
    import yaml
except ImportError as exc:
    sys.exit("PyYAML is required: python -m pip install pyyaml")

# --- human-facing stat labels ------------------------------------------------
STAT_LABELS = {
    "GLOBAL_EXP_GAIN": "Skill Experience",
    "ARMOR_TOTAL": "Armor",
    "TOTAL_LIGHT_ARMOR": "Total Light Armor",
    "LIGHT_ARMOR": "Light Armor",
    "LIGHT_ARMOR_MULTIPLIER": "Light Armor Effectiveness",
    "TOTAL_HEAVY_ARMOR": "Total Heavy Armor",
    "HEAVY_ARMOR": "Heavy Armor",
    "HEAVY_ARMOR_MULTIPLIER": "Heavy Armor Effectiveness",
    "TOTAL_WEIGHTLESS_ARMOR": "Total Weightless Armor",
    "WEIGHTLESS_ARMOR": "Weightless Armor",
    "ARMOR_MULTIPLIER_BONUS": "Armor Effectiveness",
    "TOUGHNESS": "Toughness",
    "LIGHT_ARMOR_FLAT_IGNORED": "Light Armor Flat Ignored",
    "LIGHT_ARMOR_FRACTION_IGNORED": "Light Armor % Ignored",
    "HEAVY_ARMOR_FLAT_IGNORED": "Heavy Armor Flat Ignored",
    "HEAVY_ARMOR_FRACTION_IGNORED": "Heavy Armor % Ignored",
    "ARMOR_FLAT_IGNORED": "Armor Flat Ignored",
    "ARMOR_FRACTION_IGNORED": "Armor % Ignored",
    "HEALTH_BONUS": "Maximum Health",
    "HEALTH_MULTIPLIER_BONUS": "Maximum Health",
    "MOVEMENT_SPEED_BONUS": "Movement Speed",
    "KNOCKBACK_RESISTANCE": "Knockback Resistance",
    "TOUGHNESS_BONUS": "Toughness",
    "ATTACK_DAMAGE_BONUS": "Attack Damage",
    "ATTACK_SPEED_BONUS": "Attack Speed",
    "LUCK_BONUS": "Luck",
    "BLOCK_REACH": "Block Reach",
    "STEP_HEIGHT": "Step Height",
    "SCALE": "Size",
    "GRAVITY": "Gravity",
    "SAFE_FALLING_DISTANCE": "Safe Fall Distance",
    "FALL_DAMAGE_MULTIPLIER": "Fall Damage",
    "DAMAGE_DEALT": "Damage Dealt",
    "MELEE_DAMAGE_DEALT": "Melee Damage",
    "RANGED_DAMAGE_DEALT": "Ranged Damage",
    "UNARMED_DAMAGE_DEALT": "Unarmed Damage",
    "VELOCITY_DAMAGE_BONUS": "Velocity Damage",
    "LIGHT_ARMOR_DAMAGE_BONUS": "Light Armor Damage",
    "HEAVY_ARMOR_DAMAGE_BONUS": "Heavy Armor Damage",
    "FIRE_DAMAGE_BONUS": "Fire Damage",
    "EXPLOSION_DAMAGE_BONUS": "Explosion Damage",
    "POISON_DAMAGE_BONUS": "Poison Damage",
    "MAGIC_DAMAGE_BONUS": "Magic Damage",
    "LIGHTNING_DAMAGE_BONUS": "Lightning Damage",
    "FREEZING_DAMAGE_BONUS": "Freezing Damage",
    "RADIANT_DAMAGE_BONUS": "Radiant Damage",
    "NECROTIC_DAMAGE_BONUS": "Necrotic Damage",
    "BLUDGEONING_DAMAGE_BONUS": "Bludgeoning Damage",
    "FIRE_DAMAGE_DEALT": "Fire Damage",
    "EXPLOSION_DAMAGE_DEALT": "Explosion Damage",
    "POISON_DAMAGE_DEALT": "Poison Damage",
    "BLUDGEONING_DAMAGE_DEALT": "Bludgeoning Damage",
    "MAGIC_DAMAGE_DEALT": "Magic Damage",
    "LIGHTNING_DAMAGE_DEALT": "Lightning Damage",
    "FREEZING_DAMAGE_DEALT": "Freezing Damage",
    "RADIANT_DAMAGE_DEALT": "Radiant Damage",
    "NECROTIC_DAMAGE_DEALT": "Necrotic Damage",
    "POWER_ATTACK_DAMAGE_MULTIPLIER": "Power Attack Damage",
    "POWER_ATTACK_RADIUS": "Power Attack Radius",
    "POWER_ATTACK_DAMAGE_FRACTION": "Power Attack Fraction",
    "ATTACK_REACH_BONUS": "Attack Reach",
    "ATTACK_REACH_MULTIPLIER": "Attack Reach",
    "RANGED_INACCURACY": "Ranged Accuracy",
    "RANGED_VELOCITY_BONUS": "Ranged Velocity",
    "KNOCKBACK_BONUS": "Knockback",
    "IMMUNITY_FRAME_BONUS": "Immunity Frames",
    "IMMUNITY_FRAME_MULTIPLIER": "Immunity Frames",
    "BLEED_CHANCE": "Bleed Chance",
    "BLEED_DAMAGE": "Bleed Damage",
    "BLEED_DURATION": "Bleed Duration",
    "DODGE_CHANCE": "Dodge Chance",
    "REFLECT_CHANCE": "Reflect Chance",
    "REFLECT_FRACTION": "Reflect Fraction",
    "DISMOUNT_CHANCE": "Dismount Chance",
    "STUN_CHANCE": "Stun Chance",
    "STUN_DURATION_BONUS": "Stun Duration",
    "CRIT_CHANCE": "Critical Chance",
    "CRIT_DAMAGE": "Critical Damage",
    "CROSSBOW_MAGAZINE": "Crossbow Magazine",
    "PARRY_EFFECTIVENESS_DURATION": "Parry Effectiveness",
    "PARRY_VULNERABLE_DURATION": "Parry Vulnerable",
    "PARRY_ENEMY_DEBUFF_DURATION": "Parry Enemy Debuff",
    "PARRY_SELF_DEBUFF_DURATION": "Parry Self Debuff",
    "PARRY_DAMAGE_REDUCTION": "Parry Damage Reduction",
    "PARRY_COOLDOWN": "Parry Cooldown",
    "PARRY_SUCCESS_COOLDOWN_REDUCTION": "Parry Success Cooldown",
    "DAMAGE_RESISTANCE": "Damage Resistance",
    "MELEE_RESISTANCE": "Melee Resistance",
    "PROJECTILE_RESISTANCE": "Projectile Resistance",
    "BLUDGEONING_RESISTANCE": "Bludgeoning Resistance",
    "FIRE_RESISTANCE": "Fire Resistance",
    "EXPLOSION_RESISTANCE": "Explosion Resistance",
    "MAGIC_RESISTANCE": "Magic Resistance",
    "POISON_RESISTANCE": "Poison Resistance",
    "FREEZING_RESISTANCE": "Freezing Resistance",
    "LIGHTNING_RESISTANCE": "Lightning Resistance",
    "RADIANT_RESISTANCE": "Radiant Resistance",
    "NECROTIC_RESISTANCE": "Necrotic Resistance",
    "FALLING_RESISTANCE": "Fall Resistance",
    "STUN_RESISTANCE": "Stun Resistance",
    "BLEED_RESISTANCE": "Bleed Resistance",
    "CRIT_CHANCE_RESISTANCE": "Crit Chance Resistance",
    "CRIT_DAMAGE_RESISTANCE": "Crit Damage Resistance",
    "HEALING_BONUS": "Healing",
    "HUNGER_SAVE_CHANCE": "Hunger Save Chance",
    "COOLDOWN_REDUCTION": "Cooldown Reduction",
    "CRAFTING_TIME_REDUCTION": "Crafting Time",
    "COOKING_SPEED_BONUS": "Cooking Speed",
    "AMMO_SAVE_CHANCE": "Ammo Save Chance",
    "DURABILITY_BONUS": "Durability",
    "ENTITY_DROPS": "Entity Drops",
    "ENTITY_DROP_LUCK": "Entity Drop Luck",
    "JUMP_HEIGHT_MULTIPLIER": "Jump Height",
    "JUMPS_BONUS": "Extra Jumps",
    "SNEAK_MOVEMENT_SPEED_BONUS": "Sneak Speed",
    "SPRINT_MOVEMENT_SPEED_BONUS": "Sprint Speed",
    "DIG_SPEED": "Dig Speed",
    "BLOCK_SPECIFIC_DIG_SPEED": "Block Dig Speed",
    "FISHING_LUCK": "Fishing Luck",
    "FISHING_SPEED_MULTIPLIER": "Fishing Speed",
    "EXPLOSION_RADIUS_MULTIPLIER": "Explosion Radius",
    "FOOD_BONUS_VEGETABLE": "Vegetable Food",
    "FOOD_BONUS_SEASONING": "Seasoning Food",
    "FOOD_BONUS_ALCOHOLIC": "Alcoholic Food",
    "FOOD_BONUS_BEVERAGE": "Beverage Food",
    "FOOD_BONUS_SPOILED": "Spoiled Food",
    "FOOD_BONUS_SEAFOOD": "Seafood",
    "FOOD_BONUS_MAGICAL": "Magical Food",
    "FOOD_BONUS_SWEET": "Sweet Food",
    "FOOD_BONUS_GRAIN": "Grain Food",
    "FOOD_BONUS_FRUIT": "Fruit Food",
    "FOOD_BONUS_NUTS": "Nut Food",
    "FOOD_BONUS_DAIRY": "Dairy Food",
    "FOOD_BONUS_MEAT": "Meat Food",
    "FOOD_BONUS_FATS": "Fat Food",
    "SMITHING_QUALITY_GENERAL": "Smithing Quality",
    "SMITHING_QUALITY_WOOD": "Wood Smithing Quality",
    "SMITHING_QUALITY_LEATHER": "Leather Smithing Quality",
    "SMITHING_QUALITY_STONE": "Stone Smithing Quality",
    "SMITHING_QUALITY_CHAINMAIL": "Chainmail Smithing Quality",
    "SMITHING_QUALITY_GOLD": "Gold Smithing Quality",
    "SMITHING_QUALITY_IRON": "Iron Smithing Quality",
    "SMITHING_QUALITY_DIAMOND": "Diamond Smithing Quality",
    "SMITHING_QUALITY_NETHERITE": "Netherite Smithing Quality",
    "SMITHING_QUALITY_BOW": "Bow Smithing Quality",
    "SMITHING_QUALITY_CROSSBOW": "Crossbow Smithing Quality",
    "SMITHING_QUALITY_PRISMARINE": "Prismarine Smithing Quality",
    "SMITHING_QUALITY_ENDERIC": "Enderic Smithing Quality",
    "SMITHING_FRACTION_QUALITY_GENERAL": "Smithing Quality",
    "SMITHING_FRACTION_QUALITY_WOOD": "Wood Smithing Quality",
    "SMITHING_FRACTION_QUALITY_LEATHER": "Leather Smithing Quality",
    "SMITHING_FRACTION_QUALITY_STONE": "Stone Smithing Quality",
    "SMITHING_FRACTION_QUALITY_CHAINMAIL": "Chainmail Smithing Quality",
    "SMITHING_FRACTION_QUALITY_GOLD": "Gold Smithing Quality",
    "SMITHING_FRACTION_QUALITY_IRON": "Iron Smithing Quality",
    "SMITHING_FRACTION_QUALITY_DIAMOND": "Diamond Smithing Quality",
    "SMITHING_FRACTION_QUALITY_NETHERITE": "Netherite Smithing Quality",
    "SMITHING_FRACTION_QUALITY_BOW": "Bow Smithing Quality",
    "SMITHING_FRACTION_QUALITY_CROSSBOW": "Crossbow Smithing Quality",
    "SMITHING_FRACTION_QUALITY_PRISMARINE": "Prismarine Smithing Quality",
    "SMITHING_FRACTION_QUALITY_ENDERIC": "Enderic Smithing Quality",
    "SMITHING_EXP_GAIN_GENERAL": "Smithing Experience",
    "SMITHING_EXP_GAIN_WOOD": "Wood Smithing Experience",
    "SMITHING_EXP_GAIN_LEATHER": "Leather Smithing Experience",
    "SMITHING_EXP_GAIN_STONE": "Stone Smithing Experience",
    "SMITHING_EXP_GAIN_CHAINMAIL": "Chainmail Smithing Experience",
    "SMITHING_EXP_GAIN_GOLD": "Gold Smithing Experience",
    "SMITHING_EXP_GAIN_IRON": "Iron Smithing Experience",
    "SMITHING_EXP_GAIN_DIAMOND": "Diamond Smithing Experience",
    "SMITHING_EXP_GAIN_NETHERITE": "Netherite Smithing Experience",
    "SMITHING_EXP_GAIN_BOW": "Bow Smithing Experience",
    "SMITHING_EXP_GAIN_CROSSBOW": "Crossbow Smithing Experience",
    "SMITHING_EXP_GAIN_PRISMARINE": "Prismarine Smithing Experience",
    "SMITHING_EXP_GAIN_ENDERIC": "Enderic Smithing Experience",
    "ALCHEMY_QUALITY_GENERAL": "Alchemy Quality",
    "ALCHEMY_QUALITY_DEBUFF": "Alchemy Quality (Debuff)",
    "ALCHEMY_QUALITY_BUFF": "Alchemy Quality (Buff)",
    "ALCHEMY_FRACTION_QUALITY_GENERAL": "Alchemy Quality",
    "ALCHEMY_FRACTION_QUALITY_DEBUFF": "Alchemy Quality (Debuff)",
    "ALCHEMY_FRACTION_QUALITY_BUFF": "Alchemy Quality (Buff)",
    "ALCHEMY_BREW_SPEED": "Brewing Speed",
    "BREWING_SPEED_BONUS": "Brewing Speed",
    "BREWING_INGREDIENT_SAVE_CHANCE": "Ingredient Save Chance",
    "POTION_SAVE_CHANCE": "Potion Save Chance",
    "THROW_VELOCITY_BONUS": "Throw Velocity",
    "ALCHEMY_EXP_GAIN": "Alchemy Experience",
    "SPLASH_INTENSITY_MINIMUM": "Splash Intensity",
    "LINGERING_DURATION_MULTIPLIER": "Lingering Duration",
    "LINGERING_RADIUS_MULTIPLIER": "Lingering Radius",
    "ENCHANTING_QUALITY": "Enchanting Quality",
    "ENCHANTING_FRACTION_QUALITY": "Enchanting Quality",
    "ENCHANTING_QUALITY_ANVIL": "Anvil Quality",
    "ENCHANTING_FRACTION_QUALITY_ANVIL": "Anvil Quality",
    "ENCHANTING_AMPLIFY_CHANCE": "Amplify Chance",
    "ENCHANTING_LAPIS_SAVE_CHANCE": "Lapis Save Chance",
    "ENCHANTING_VANILLA_EXP_GAIN": "Vanilla Enchanting Experience",
    "ENCHANTING_REFUND_CHANCE": "Enchant Refund Chance",
    "ENCHANTING_REFUND_AMOUNT": "Enchant Refund Amount",
    "ENCHANTING_EXP_GAIN": "Enchanting Experience",
    "BUTCHERY_DROP_MULTIPLIER": "Butchery Drops",
    "FARMING_DROP_MULTIPLIER": "Farming Drops",
    "FARMING_LUCK": "Farming Luck",
    "FARMING_EXP_GAIN": "Farming Experience",
    "MINING_DROP_MULTIPLIER": "Mining Drops",
    "MINING_LUCK": "Mining Luck",
    "BLASTING_DROP_MULTIPLIER": "Blasting Drops",
    "BLASTING_LUCK": "Blasting Luck",
    "MINING_EXP_GAIN": "Mining Experience",
    "DIGGING_DROP_MULTIPLIER": "Digging Drops",
    "DIGGING_LUCK": "Digging Luck",
    "DIGGING_ARCHAEOLOGY_LUCK": "Archaeology Luck",
    "DIGGING_EXP_GAIN": "Digging Experience",
    "WOODCUTTING_DROP_MULTIPLIER": "Woodcutting Drops",
    "WOODCUTTING_LUCK": "Woodcutting Luck",
    "WOODCUTTING_EXP_GAIN": "Woodcutting Experience",
    "FISHING_EXP_GAIN": "Fishing Experience",
    "ARCHERY_EXP_GAIN": "Archery Experience",
    "LIGHT_ARMOR_EXP_GAIN": "Light Armor Experience",
    "HEAVY_ARMOR_EXP_GAIN": "Heavy Armor Experience",
    "LIGHT_WEAPONS_EXP_GAIN": "Light Weapons Experience",
    "HEAVY_WEAPONS_EXP_GAIN": "Heavy Weapons Experience",
    # perk rewards (lowercase keys)
    "mining_miningdrops_add": "Mining Drops",
    "mining_miningspeedbonus_add": "Mining Speed",
    "farming_farmingdrops_add": "Farming Drops",
    "woodcutting_woodcuttingdrops_add": "Woodcutting Drops",
    "woodcutting_woodcuttingspeedbonus_add": "Woodcutting Speed",
    "digging_diggingspeedbonus_add": "Digging Speed",
}

# stats that are flat additions rather than percentages
FLAT_STATS = {
    "HEALTH_BONUS", "HEALTH_MULTIPLIER_BONUS", "LUCK_BONUS", "BLOCK_REACH",
    "STEP_HEIGHT", "SAFE_FALLING_DISTANCE", "FISHING_LUCK", "FARMING_LUCK",
    "MINING_LUCK", "BLASTING_LUCK", "DIGGING_LUCK", "DIGGING_ARCHAEOLOGY_LUCK",
    "WOODCUTTING_LUCK", "ATTACK_DAMAGE_BONUS", "ATTACK_REACH_BONUS",
    "RANGED_INACCURACY", "CROSSBOW_MAGAZINE", "IMMUNITY_FRAME_BONUS",
    "BLEED_DURATION", "STUN_DURATION_BONUS", "FOOD_BONUS_VEGETABLE",
    "FOOD_BONUS_SEASONING", "FOOD_BONUS_ALCOHOLIC", "FOOD_BONUS_BEVERAGE",
    "FOOD_BONUS_SPOILED", "FOOD_BONUS_SEAFOOD", "FOOD_BONUS_MAGICAL",
    "FOOD_BONUS_SWEET", "FOOD_BONUS_GRAIN", "FOOD_BONUS_FRUIT",
    "FOOD_BONUS_NUTS", "FOOD_BONUS_DAIRY", "FOOD_BONUS_MEAT",
    "FOOD_BONUS_FATS", "SMITHING_QUALITY_GENERAL", "SMITHING_QUALITY_WOOD",
    "SMITHING_QUALITY_LEATHER", "SMITHING_QUALITY_STONE",
    "SMITHING_QUALITY_CHAINMAIL", "SMITHING_QUALITY_GOLD",
    "SMITHING_QUALITY_IRON", "SMITHING_QUALITY_DIAMOND",
    "SMITHING_QUALITY_NETHERITE", "SMITHING_QUALITY_BOW",
    "SMITHING_QUALITY_CROSSBOW", "SMITHING_QUALITY_PRISMARINE",
    "SMITHING_QUALITY_ENDERIC", "ALCHEMY_QUALITY_GENERAL",
    "ALCHEMY_QUALITY_DEBUFF", "ALCHEMY_QUALITY_BUFF",
    "ENCHANTING_QUALITY", "ENCHANTING_QUALITY_ANVIL",
    "ENCHANTING_REFUND_AMOUNT", "TOUGHNESS_BONUS", "PARRY_COOLDOWN",
    "TOUGHNESS", "ARMOR_TOTAL", "TOTAL_LIGHT_ARMOR", "LIGHT_ARMOR",
    "TOTAL_HEAVY_ARMOR", "HEAVY_ARMOR", "TOTAL_WEIGHTLESS_ARMOR",
    "WEIGHTLESS_ARMOR",
}

# stat keys whose display is inverted in meaning (higher number = worse)
INVERTED_STATS = {"RANGED_INACCURACY", "PARRY_VULNERABLE_DURATION", "PARRY_SELF_DEBUFF_DURATION"}


def strip_mc_codes(text):
    """Remove Minecraft color codes (&x or &lx where x is a hex char)."""
    return re.sub(r"&[0-9a-fA-FklmnorKLMNOR]", "", text)


def stat_to_entry(key, value):
    percent = key not in FLAT_STATS
    label = STAT_LABELS.get(key, key.replace("_", " ").title())
    magnitude = abs(value) if not percent else abs(value) * 100
    is_buff = value > 0
    if key in INVERTED_STATS:
        is_buff = not is_buff
    return {
        "key": key,
        "label": label,
        "value": round(value, 4),
        "magnitude": round(magnitude, 2 if percent else 1),
        "flat": not percent,
        "percent": percent,
        "kind": "buff" if is_buff else "debuff",
    }


def parse_entry(key, data):
    stats = []
    for sk, sv in (data.get("stat_buffs") or {}).items():
        stats.append(stat_to_entry(sk, sv))
    for sk, sv in (data.get("perk_rewards") or {}).items():
        stats.append(stat_to_entry(sk, sv))
    return {
        "key": key,
        "name": strip_mc_codes(data.get("display_name", key)),
        "prefix": strip_mc_codes(data.get("prefix", "")),
        "icon": data.get("icon", "BARRIER"),
        "position": data.get("position", 0),
        "description": [strip_mc_codes(l) for l in data.get("description", [])],
        "stats": stats,
    }


def main():
    with open(RACES_PATH, encoding="utf-8") as f:
        races_yaml = yaml.safe_load(f)
    with open(CLASSES_PATH, encoding="utf-8") as f:
        classes_yaml = yaml.safe_load(f)

    groups = {1: "Combat", 2: "Specialist", 3: "Harvester"}

    races = [parse_entry(k, v) for k, v in (races_yaml.get("races") or {}).items()]
    classes = []
    for k, v in (classes_yaml.get("classes") or {}).items():
        entry = parse_entry(k, v)
        entry["group"] = v.get("group", 0)
        entry["group_name"] = groups.get(entry["group"], "Unknown")
        entry["group_label"] = f"Group {entry['group']}" if entry["group"] else ""
        classes.append(entry)

    races.sort(key=lambda r: r["position"])
    classes.sort(key=lambda r: (r["group"], r["position"]))

    payload = {
        "generated": "Auto-generated by scripts/build_data.py — do not edit.",
        "races": races,
        "classes": classes,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(races)} races, {len(classes)} classes)")


if __name__ == "__main__":
    main()