import vpk
import re

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')

for path in ['models/heroes_staging/archer/archer.vmdl_c', 'models/heroes_staging/archer_v2/archer_v2.vmdl_c']:
    data = dl_pak[path].read()
    print(f"=== {path} ({len(data)} bytes) ===")
    strings = [s.decode('utf-8', 'ignore') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{5,}', data)]
    # filter interesting strings like material, bone, anim, etc.
    vmats = [s for s in strings if s.endswith('.vmat')]
    print("  Referenced materials:", set(vmats))
    vskels = [s for s in strings if 'skel' in s.lower()]
    print("  Referenced skeletons:", set(vskels))
