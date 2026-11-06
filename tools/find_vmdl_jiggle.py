import vpk
import re

dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')

# Search for any vmdl_c that has JiggleBone
found = 0
for p in dota_pak:
    if p.endswith('.vmdl_c'):
        data = dota_pak[p].read()
        if b'JiggleBone' in data:
            print("Found JiggleBone in:", p)
            found += 1
            if found >= 5:
                break

