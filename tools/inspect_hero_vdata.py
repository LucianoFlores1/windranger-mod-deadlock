import vpk
import re

d = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')

print("Searching vdata for hero models...")
for k in d:
    if 'hero' in k and k.endswith('.vdata_c'):
        data = d[k].read()
        matches = [s.decode('latin1', errors='ignore') for s in re.findall(rb'[a-zA-Z0-9_\/\\.]+\.vmdl', data)]
        archer_matches = [m for m in matches if 'archer' in m or 'talon' in m]
        if archer_matches:
            print(f"File: {k}")
            for m in set(archer_matches):
                print(f"  -> {m}")

