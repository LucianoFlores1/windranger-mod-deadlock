import vpk
import re

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
data = dl_pak['models/heroes_staging/archer/archer.vmdl_c'].read()

# Let's search in bone list
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', data)]
bones = [s for s in sorted(set(strings)) if any(k in s.lower() for k in ['cloth', 'tail', 'skirt', 'coat', 'flap', 'cape', 'ribbon', 'hair', 'quiver', 'tassel'])]
for b in bones:
    print(b)

