import vpk
import re

d = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
data = d['scripts/heroes.vdata_c'].read()

# find all strings
strings = [s.decode('latin1', errors='ignore') for s in re.findall(rb'[a-zA-Z0-9_\/\\.-]{3,}', data)]

print("Strings in heroes.vdata_c containing archer or talon:")
for s in sorted(set(strings)):
    if 'archer' in s.lower() or 'talon' in s.lower():
        print(" ", s)

