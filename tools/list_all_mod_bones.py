import vpk
import re

pak = vpk.open("extracted_mod/pak22_dir.vpk")
vmdl_bytes = pak['models/heroes_staging/archer/archer.vmdl_c'].read()

# Let's search for bone names or inspect Skeleton
# In Source 2 model, bone names are in string table
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', vmdl_bytes)]
# Filter candidate bone names
bones = [s for s in sorted(set(strings)) if any(k in s.lower() for k in ['cape', 'cloth', 'hair', 'skirt', 'jiggle', 'quiver', 'bow', 'feather', 'string', 'wind', 'spine', 'shoulder', 'hand'])]
for b in bones:
    print(b)

