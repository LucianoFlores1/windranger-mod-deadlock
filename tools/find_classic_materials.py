import vpk
import re

dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')

files = [f for f in dota_pak if 'windrunner' in f and f.endswith('.vmat_c') and 'arcana' not in f]
print("Classic Windrunner vmat_c in Dota 2 pak:")
for f in sorted(files):
    print(" ", f)

parts = [
    'models/heroes/windrunner/windrunner.vmdl_c',
    'models/heroes/windrunner/windrunner_head.vmdl_c',
    'models/heroes/windrunner/windrunner_cape.vmdl_c',
    'models/heroes/windrunner/windrunner_shoulderpads.vmdl_c',
    'models/heroes/windrunner/windrunner_quiver.vmdl_c',
    'models/heroes/windrunner/windrunner_bow.vmdl_c',
]

print("\nMaterials referenced in models:")
for part in parts:
    if part in dota_pak:
        data = dota_pak[part].read()
        strings = [s.decode('latin1', errors='ignore') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', data)]
        vmats = [s for s in strings if s.endswith('.vmat')]
        print(f" {part}:")
        for m in sorted(set(vmats)):
            print(f"    -> {m}")
