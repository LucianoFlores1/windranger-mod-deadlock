import vpk
import re

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
vdata = dl_pak['scripts/heroes.vdata_c'].read()

# Let's search for hero identifiers in heroes.vdata_c
# Typically KV3 or binary KV3
printable = re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', vdata)
strings = [s.decode('utf-8', 'ignore') for s in printable]
print("Found strings containing archer or talon:")
for s in strings:
    if 'archer' in s.lower() or 'talon' in s.lower():
        print("  ", s)
