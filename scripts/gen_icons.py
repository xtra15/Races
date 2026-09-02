import json
import re

# Load the data.json to get all keys
with open('E:/NewServer/plugins/ValhallaRaces/site/assets/data/data.json', 'r') as f:
    data = json.load(f)

# Read existing icons.js
with open('E:/NewServer/plugins/ValhallaRaces/site/assets/js/icons.js', 'r') as f:
    icons_js = f.read()

# Get existing icon keys
existing_keys = set(re.findall(r'^  (\w+):', icons_js, re.MULTILINE))
existing_keys.discard('_default')

# Get all race and class keys from data
all_keys = []
for r in data['races']:
    key = re.sub(r'^[^a-z]+', '', r['key'])
    all_keys.append((key, 'race'))
for c in data['classes']:
    key = re.sub(r'^[^a-z]+', '', c['key'])
    all_keys.append((key, 'class'))

# Find missing keys
missing = [(k, t) for k, t in all_keys if k not in existing_keys]
print(f"Existing icons: {len(existing_keys)}")
print(f"Missing icons: {len(missing)}")

# Generate placeholder icons - a generic diamond sigil shape with subtle variation by index
# These are placeholders that DeepSeek will replace later
placeholder = """  {key}: /* placeholder - replace with {type} icon */
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
     <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
     <circle cx="32" cy="32" r="7" opacity=".6"/>`,"""

# Generate a few distinct base shapes for variety so the placeholders aren't all identical
shapes = [
    # diamond with facets
    """<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
     <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
     <circle cx="32" cy="32" r="6" opacity=".6"/>""",
    # circle with inner cross
    """<circle cx="32" cy="32" r="22"/>
     <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>""",
    # up-pointing triangle
    """<path d="M32 10 L52 52 L12 52 Z"/>
     <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
     <path d="M32 44 L32 36"/>""",
    # hexagon with circle
    """<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
     <circle cx="32" cy="32" r="10"/>
     <circle cx="32" cy="32" r="3"/>""",
    # shield
    """<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
     <path d="M27 30 L32 38 L38 26"/>""",
    # crossed lines with diamond
    """<path d="M18 18 L46 46 M46 18 L18 46"/>
     <circle cx="32" cy="32" r="6"/>
     <path d="M32 22 L32 42 M22 32 L42 32"/>""",
    # star
    """<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
     <circle cx="32" cy="32" r="5" opacity=".7"/>""",
    # flame
    """<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
     <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>""",
]

# Also generate per-key derived colors for the comment
for i, (key, typ) in enumerate(missing):
    shape = shapes[i % len(shapes)]
    entry = f"  {key}: /* placeholder - {typ} icon */\n    `<path d=\"M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z\"/>\n     ...`,\n"
    # Just use the shape directly
    entry = f"  {key}: /* TODO: {typ} - replace with custom SVG */\n    `{shape}`,\n"
    # Insert into icons.js before the _default section
    icons_js = icons_js.replace("\n  _default:", "\n" + entry + "\n  _default:")

with open('E:/NewServer/plugins/ValhallaRaces/site/assets/js/icons.js', 'w') as f:
    f.write(icons_js)

print(f"Added {len(missing)} placeholder icons")

# Also add a JS comment at top documenting the format for DeepSeek
with open('E:/NewServer/plugins/ValhallaRaces/site/assets/js/icons.js', 'r') as f:
    icons_js = f.read()

# Count keys
final_keys = set(re.findall(r'^  (\w+):', icons_js, re.MULTILINE))
final_keys.discard('_default')
print(f"Total icons: {len(final_keys)}")
