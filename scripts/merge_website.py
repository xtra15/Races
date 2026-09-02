import yaml
import json
import re

STAT_LABELS = {
    'MELEE_DAMAGE_DEALT': 'Melee Damage',
    'RANGED_DAMAGE_DEALT': 'Ranged Damage',
    'UNARMED_DAMAGE_DEALT': 'Unarmed Damage',
    'DAMAGE_DEALT': 'Damage',
    'MAGIC_DAMAGE_DEALT': 'Magic Damage',
    'FIRE_DAMAGE_DEALT': 'Fire Damage',
    'FREEZING_DAMAGE_DEALT': 'Freezing Damage',
    'LIGHTNING_DAMAGE_DEALT': 'Lightning Damage',
    'NECROTIC_DAMAGE_DEALT': 'Necrotic Damage',
    'RADIANT_DAMAGE_DEALT': 'Radiant Damage',
    'POISON_DAMAGE_DEALT': 'Poison Damage',
    'BLUDGEONING_DAMAGE_DEALT': 'Bludgeoning Damage',
    'EXPLOSION_DAMAGE_DEALT': 'Explosion Damage',
    'ARMOR_MULTIPLIER_BONUS': 'Armor',
    'DAMAGE_RESISTANCE': 'Damage Resistance',
    'MELEE_RESISTANCE': 'Melee Resistance',
    'PROJECTILE_RESISTANCE': 'Projectile Resistance',
    'MAGIC_RESISTANCE': 'Magic Resistance',
    'FIRE_RESISTANCE': 'Fire Resistance',
    'FREEZING_RESISTANCE': 'Freezing Resistance',
    'LIGHTNING_RESISTANCE': 'Lightning Resistance',
    'NECROTIC_RESISTANCE': 'Necrotic Resistance',
    'RADIANT_RESISTANCE': 'Radiant Resistance',
    'POISON_RESISTANCE': 'Poison Resistance',
    'EXPLOSION_RESISTANCE': 'Explosion Resistance',
    'KNOCKBACK_RESISTANCE': 'Knockback Resistance',
    'BLEED_RESISTANCE': 'Bleed Resistance',
    'STUN_RESISTANCE': 'Stun Resistance',
    'HEALTH_BONUS': 'Maximum Health',
    'MOVEMENT_SPEED_BONUS': 'Movement Speed',
    'SPRINT_MOVEMENT_SPEED_BONUS': 'Sprint Speed',
    'SNEAK_MOVEMENT_SPEED_BONUS': 'Sneak Speed',
    'JUMP_HEIGHT_MULTIPLIER': 'Jump Height',
    'FALLING_RESISTANCE': 'Fall Resistance',
    'SCALE': 'Size',
    'DODGE_CHANCE': 'Dodge Chance',
    'CRIT_CHANCE': 'Critical Chance',
    'CRIT_DAMAGE': 'Critical Damage',
    'GLOBAL_EXP_GAIN': 'Skill Experience',
    'MINING_EXP_GAIN': 'Mining Experience',
    'WOODCUTTING_EXP_GAIN': 'Woodcutting Experience',
    'FARMING_EXP_GAIN': 'Farming Experience',
    'FISHING_EXP_GAIN': 'Fishing Experience',
    'ARCHERY_EXP_GAIN': 'Archery Experience',
    'LIGHT_WEAPONS_EXP_GAIN': 'Light Weapons Experience',
    'HEAVY_WEAPONS_EXP_GAIN': 'Heavy Weapons Experience',
    'ENCHANTING_EXP_GAIN': 'Enchanting Experience',
    'ALCHEMY_EXP_GAIN': 'Alchemy Experience',
    'COOLDOWN_REDUCTION': 'Cooldown Reduction',
    'HEALING_BONUS': 'Healing',
    'HUNGER_SAVE_CHANCE': 'Hunger Save',
    'DURABILITY_BONUS': 'Durability',
    'FARMING_DROP_MULTIPLIER': 'Farming Drops',
    'MINING_DROP_MULTIPLIER': 'Mining Drops',
    'FISHING_LUCK': 'Fishing Luck',
    'FISHING_SPEED_MULTIPLIER': 'Fishing Speed',
    'DIG_SPEED': 'Dig Speed',
    'LUCK_BONUS': 'Luck',
    'FOOD_BONUS_MEAT': 'Meat Food',
    'FOOD_BONUS_VEGETABLE': 'Vegetable Food',
    'FOOD_BONUS_SEAFOOD': 'Seafood Food',
    'FOOD_BONUS_FRUIT': 'Fruit Food',
    'FOOD_BONUS_GRAIN': 'Grain Food',
    'FOOD_BONUS_NUTS': 'Nuts Food',
    'FOOD_BONUS_DAIRY': 'Dairy Food',
    'FOOD_BONUS_SWEET': 'Sweet Food',
    'FOOD_BONUS_ALCOHOLIC': 'Alcoholic Food',
    'FOOD_BONUS_BEVERAGE': 'Beverage Food',
    'FOOD_BONUS_SPOILED': 'Spoiled Food',
    'FOOD_BONUS_MAGICAL': 'Magical Food',
    'FOOD_BONUS_SEASONING': 'Seasoning Food',
    'FOOD_BONUS_FATS': 'Fats Food',
    'SMITHING_QUALITY_GENERAL': 'Smithing Quality',
    'ALCHEMY_QUALITY_GENERAL': 'Alchemy Quality',
    'ENCHANTING_QUALITY': 'Enchanting Quality',
    'BREWING_SPEED_BONUS': 'Brewing Speed',
    'CRAFTING_TIME_REDUCTION': 'Crafting Speed',
    'COOKING_SPEED_BONUS': 'Cooking Speed',
    'ATTACK_SPEED_BONUS': 'Attack Speed',
    'TOTAL_HEAVY_ARMOR': 'Heavy Armor',
    'TOTAL_LIGHT_ARMOR': 'Light Armor',
    'KNOCKBACK_BONUS': 'Knockback',
    'EXPLOSION_RADIUS_MULTIPLIER': 'Explosion Radius',
    'THROW_VELOCITY_BONUS': 'Throw Velocity',
    'RANGED_VELOCITY_BONUS': 'Ranged Velocity',
    'RANGED_INACCURACY': 'Ranged Accuracy',
    'AMMO_SAVE_CHANCE': 'Ammo Save',
    'ALCHEMY_QUALITY_DEBUFF': 'Alchemy Debuff Quality',
    'ALCHEMY_QUALITY_BUFF': 'Alchemy Buff Quality',
    'ENCHANTING_VANILLA_EXP_GAIN': 'Enchanting Experience',
}

def stat_to_dict(key, value):
    is_flat = key in ('HEALTH_BONUS', 'FISHING_LUCK', 'TOTAL_HEAVY_ARMOR',
                       'TOTAL_LIGHT_ARMOR', 'ALCHEMY_QUALITY_GENERAL',
                       'ENCHANTING_QUALITY', 'SMITHING_QUALITY_GENERAL',
                       'ALCHEMY_QUALITY_DEBUFF', 'ALCHEMY_QUALITY_BUFF', 'SCALE')
    magnitude = abs(value) * 100 if not is_flat else abs(value)
    return {
        'key': key,
        'label': STAT_LABELS.get(key, key.replace('_', ' ').title()),
        'value': value,
        'magnitude': magnitude,
        'flat': is_flat,
        'percent': not is_flat,
        'kind': 'buff' if value > 0 else 'debuff'
    }

# Read existing data
with open('E:/NewServer/plugins/ValhallaRaces/site/assets/data/data.json', 'r') as f:
    existing_data = json.load(f)

existing_race_keys = {r['key'] for r in existing_data['races']}
existing_class_keys = {c['key'] for c in existing_data['classes']}

print(f"Existing: {len(existing_data['races'])} races, {len(existing_data['classes'])} classes")

# Read new YAML
with open('E:/NewServer/plugins/ValhallaRaces/races_new.yml', 'r') as f:
    new_races_yaml = f.read()

with open('E:/NewServer/plugins/ValhallaRaces/classes_new.yml', 'r') as f:
    new_classes_yaml = f.read()

# Parse new races
new_races = []
for match in re.finditer(r'^  (\w+):\s*$', new_races_yaml, re.MULTILINE):
    key = match.group(1)
    if key in existing_race_keys:
        continue
    start = match.start()
    next_match = re.search(r'^  \w+:', new_races_yaml[start+10:], re.MULTILINE)
    end = start + 10 + next_match.start() if next_match else len(new_races_yaml)
    block = new_races_yaml[start:end]

    name_match = re.search(r"display_name:\s*'[^']*?(\w[^']*?)'", block)
    icon_match = re.search(r'icon:\s*(\S+:-?\d+)', block)
    pos_match = re.search(r'position:\s*(\d+)', block)

    name = name_match.group(1) if name_match else key.replace('_', ' ').title()
    icon = icon_match.group(1) if icon_match else 'DIAMOND_SWORD:-1'
    position = int(pos_match.group(1)) if pos_match else 0

    description = []
    desc_match = re.search(r'description:\s*\n((?:\s+-\s+.+\n)+)', block)
    if desc_match:
        for line in desc_match.group(1).strip().split('\n'):
            cleaned = re.sub(r"^- '", '', line.strip())
            cleaned = re.sub(r"'$", '', cleaned)
            cleaned = re.sub(r'&[0-9a-fk-or]', '', cleaned)
            cleaned = cleaned.lstrip('- ')
            if cleaned.startswith("'"):
                cleaned = cleaned[1:]
            description.append(cleaned)

    stats = []
    stat_section = re.search(r'stat_buffs:\s*\n((?:\s+\w+:.*\n)+)', block)
    if stat_section:
        for stat_line in stat_section.group(1).strip().split('\n'):
            parts = stat_line.strip().split(':')
            if len(parts) == 2:
                skey = parts[0].strip()
                sval = parts[1].strip()
                try:
                    stats.append(stat_to_dict(skey, float(sval)))
                except:
                    pass

    new_races.append({
        'key': key,
        'name': name,
        'prefix': f'[{name}]',
        'icon': icon,
        'position': position,
        'description': description,
        'stats': stats
    })

# Parse new classes
new_classes = []
for match in re.finditer(r'^  (\w+):\s*$', new_classes_yaml, re.MULTILINE):
    key = match.group(1)
    if key in existing_class_keys:
        continue
    start = match.start()
    next_match = re.search(r'^  \w+:', new_classes_yaml[start+10:], re.MULTILINE)
    end = start + 10 + next_match.start() if next_match else len(new_classes_yaml)
    block = new_classes_yaml[start:end]

    name_match = re.search(r"display_name:\s*'[^']*?(\w[^']*?)'", block)
    icon_match = re.search(r'icon:\s*(\S+:-?\d+)', block)
    pos_match = re.search(r'position:\s*(\d+)', block)
    group_match = re.search(r'group:\s*(\d+)', block)

    name = name_match.group(1) if name_match else key.replace('_', ' ').title()
    icon = icon_match.group(1) if icon_match else 'IRON_SWORD:-1'
    position = int(pos_match.group(1)) if pos_match else 0
    group = int(group_match.group(1)) if group_match else 1

    description = []
    desc_match = re.search(r'description:\s*\n((?:\s+-\s+.+\n)+)', block)
    if desc_match:
        for line in desc_match.group(1).strip().split('\n'):
            cleaned = re.sub(r"^- '", '', line.strip())
            cleaned = re.sub(r"'$", '', cleaned)
            cleaned = re.sub(r'&[0-9a-fk-or]', '', cleaned)
            cleaned = cleaned.lstrip('- ')
            if cleaned.startswith("'"):
                cleaned = cleaned[1:]
            description.append(cleaned)

    stats = []
    stat_section = re.search(r'stat_buffs:\s*\n((?:\s+\w+:.*\n)+)', block)
    if stat_section:
        for stat_line in stat_section.group(1).strip().split('\n'):
            parts = stat_line.strip().split(':')
            if len(parts) == 2:
                skey = parts[0].strip()
                sval = parts[1].strip()
                try:
                    stats.append(stat_to_dict(skey, float(sval)))
                except:
                    pass

    new_classes.append({
        'key': key,
        'name': name,
        'group': group,
        'icon': icon,
        'position': position,
        'description': description,
        'stats': stats
    })

existing_data['races'].extend(new_races)
existing_data['classes'].extend(new_classes)
existing_data['generated'] = 'Auto-generated - 227 races, 127 classes'

with open('E:/NewServer/plugins/ValhallaRaces/site/assets/data/data.json', 'w') as f:
    json.dump(existing_data, f, indent=1)

print(f"Updated: {len(existing_data['races'])} races, {len(existing_data['classes'])} classes")
print(f"Added: {len(new_races)} new races, {len(new_classes)} new classes")
