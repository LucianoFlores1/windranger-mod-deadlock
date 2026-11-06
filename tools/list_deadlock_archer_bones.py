import vpk
import re

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
data = dl_pak['models/heroes_staging/archer/archer.vmdl_c'].read()

strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', data)]
candidates = [s for s in sorted(set(strings)) if any(k in s.lower() for k in ['hair', 'cape', 'cloth', 'coat', 'skirt', 'tail', 'feather', 'quiver', 'strap', 'jiggle', 'chain', 'ponytail', 'belt'])]
print("Deadlock Archer native cloth/hair/jiggle bones:")
for c in candidates:
    print(" ", c)

