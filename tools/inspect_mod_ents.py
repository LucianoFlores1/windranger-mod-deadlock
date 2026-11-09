import vpk
import re

mod_vpk = vpk.open(r"custom_mod_source\maps\ui\hero_prefabs\archer.vpk")
ents = mod_vpk['maps/ui/hero_prefabs/archer/entities/default_ents.vents_c'].read()

words = re.findall(rb'[\x20-\x7e]{4,}', ents)
print("Total words in mod vents_c:", len(words))
for w in words:
    s = w.decode('latin1')
    if any(k in s.lower() for k in ['hero', 'model', 'archer', 'camera', 'light', 'picker', 'target', 'entity', 'class', 'lash', 'ring']):
        print(" ", s)
