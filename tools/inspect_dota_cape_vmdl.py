import re

data = open(r'dota2_extracted/models/heroes/windrunner/windrunner_cape.vmdl_c', 'rb').read()
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.]{4,}', data)]
print(f"Cape vmdl_c size: {len(data)}")
print("Cape strings count:", len(strings))
cape_bones = [s for s in set(strings) if any(k in s.lower() for k in ['cloth', 'cape', 'jiggle', 'chain', 'phys', 'spring'])]
print("Cape physics/bones strings:", cape_bones)

# Check classes in cape vmdl_c
classes = [s for s in set(strings) if s.startswith('C') or 'Node' in s or 'List' in s]
print("Classes/nodes in cape:", classes[:20])

