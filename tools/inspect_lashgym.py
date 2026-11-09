import vpk
import re

mod_vpk = vpk.open(r"custom_mod_source\maps\ui\hero_prefabs\archer.vpk")
data = mod_vpk['models/gym/lashgym_ring.vmdl_c'].read()
print("lashgym_ring size:", len(data))

# Find materials referenced in lashgym_ring
for match in re.finditer(rb'materials\/[a-zA-Z0-9_\/\\.-]+\.vmat', data):
    print("  ->", match.group(0).decode('latin1'))

# Find bones/joints
print("Sample strings:")
for s in re.findall(rb'[a-zA-Z0-9_]{4,}', data)[:30]:
    print("  ", s.decode('latin1'))
