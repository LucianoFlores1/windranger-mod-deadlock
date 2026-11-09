import vpk
import re

mod_vpk = vpk.open(r"custom_mod_source\maps\ui\hero_prefabs\archer.vpk")
mod_ents = mod_vpk['maps/ui/hero_prefabs/archer/entities/default_ents.vents_c'].read()

# find position of lashgym_ring
idx = mod_ents.find(b'lashgym_ring')
print("Found at:", idx)
if idx != -1:
    print(repr(mod_ents[max(0, idx-100):min(len(mod_ents), idx+150)]))
