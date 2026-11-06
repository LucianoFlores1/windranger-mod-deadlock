import vpk
import re

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
skel_data = dl_pak['models/heroes_staging/archer/archer.vnmskel_c'].read()

# strings in skeleton
bones = re.findall(rb'[a-zA-Z0-9_]{3,30}', skel_data)
unique_bones = []
for b in bones:
    s = b.decode('latin1')
    if s not in unique_bones and ('bone' in s.lower() or 'root' in s.lower() or 'arm' in s.lower() or 'hand' in s.lower() or 'leg' in s.lower() or 'spine' in s.lower() or 'head' in s.lower() or 'clav' in s.lower()):
        unique_bones.append(s)

print("Archer bone names (sample):", unique_bones[:30])

dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')
wr_data = dota_pak['models/heroes/windrunner/windrunner.vmdl_c'].read()
wr_bones = re.findall(rb'[a-zA-Z0-9_]{3,30}', wr_data)
unique_wr_bones = []
for b in wr_bones:
    s = b.decode('latin1')
    if s not in unique_wr_bones and ('bone' in s.lower() or 'root' in s.lower() or 'arm' in s.lower() or 'hand' in s.lower() or 'leg' in s.lower() or 'spine' in s.lower() or 'head' in s.lower() or 'clav' in s.lower()):
        unique_wr_bones.append(s)

print("Windrunner bone names (sample):", unique_wr_bones[:30])
