import re

data = open(r'dota2_extracted/models/heroes/windrunner/windrunner.vmdl_c', 'rb').read()
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.]{4,}', data)]
print(f"windrunner.vmdl_c size: {len(data)}")
cape_bones = [s for s in set(strings) if any(k in s.lower() for k in ['cloth', 'cape', 'jiggle', 'chain', 'phys', 'spring', 'dynamic'])]
print("Physics/bones strings in windrunner.vmdl_c:", sorted(cape_bones))

