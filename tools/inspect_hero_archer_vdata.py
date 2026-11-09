import vpk
import re

pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
data = pak['scripts/heroes.vdata_c'].read()
idx = data.find(b'hero_archer')
if idx != -1:
    print('Found hero_archer at', idx)
    chunk = data[idx:idx+4000]
    for s in re.findall(rb'[\x20-\x7e]{4,}', chunk):
        text = s.decode('ascii', errors='ignore')
        if any(w in text for w in ['model', 'vmdl', 'prefab', 'map', 'archer', 'talon', 'grey']):
            print(' ', text)
