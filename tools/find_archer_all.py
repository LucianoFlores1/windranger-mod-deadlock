import vpk
import re

d = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')

print("Searching for 'heroes_staging/archer' across all files in pak01_dir.vpk...")
for k in d:
    if k.endswith(('.vdata_c', '.vcfg_c', '.kv3', '.txt')):
        try:
            data = d[k].read()
            if b'heroes_staging/archer' in data:
                print(f"Found in: {k}")
                # print matching strings
                matches = [s.decode('latin1', errors='ignore') for s in re.findall(rb'[a-zA-Z0-9_\/\\.-]*heroes_staging\/archer[a-zA-Z0-9_\/\\.-]*', data)]
                for m in set(matches):
                    print(f"   {m}")
        except Exception:
            pass

