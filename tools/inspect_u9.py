import vpk
import re

mod_vpk = vpk.open(r"custom_mod_source\maps\ui\hero_prefabs\archer.vpk")
u9 = mod_vpk['maps/ui/hero_prefabs/archer/entities/unnamed_9.vmdl_c'].read()
print("unnamed_9.vmdl_c size:", len(u9))
for s in re.findall(rb'[a-zA-Z0-9_\/\\.]{4,}', u9):
    print(" ", s.decode('latin1', errors='ignore'))
