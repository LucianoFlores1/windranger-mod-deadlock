import vpk
import re

p = vpk.open(r'custom_mod_source\maps\ui\hero_prefabs\archer.vpk')
data = p['maps/ui/hero_prefabs/archer/entities/default_ents.vents_c'].read()
strings = [s.decode('latin1', errors='ignore') for s in re.findall(rb'[a-zA-Z0-9_\/\\.-]{4,}', data)]
print("Strings in default_ents.vents_c:")
for s in strings:
    if any(x in s.lower() for x in ['model', 'archer', 'hero', 'vmdl', 'attach']):
        print(" ", s)

