import vpk
import re

dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')

wr_base = [f for f in dota_pak if f.startswith('models/heroes/windrunner/')]
print(f"Base Windrunner files: {len(wr_base)}")
for f in sorted(wr_base):
    if not f.endswith('.vnmclip_c') and not f.endswith('.vanim_c'):
        print(f)
