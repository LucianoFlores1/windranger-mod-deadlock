import vpk
import re

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
data = dl_pak['models/heroes_staging/archer/archer.vmdl_c'].read()

pos = data.find(b'BaseJigglebon')
# Search in range pos-5000 to pos+50000
chunk = data[pos-2000:pos+30000]
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', chunk)]
candidates = [s for s in sorted(set(strings)) if any(k in s.lower() for k in ['hair', 'cape', 'cloth', 'coat', 'skirt', 'tail', 'feather', 'quiver', 'strap', 'jiggle', 'chain', 'ponytail', 'belt', 'spine', 'owl'])]
print("Simulated / dynamic bones in Deadlock archer:")
for c in candidates:
    print("  ", c)

