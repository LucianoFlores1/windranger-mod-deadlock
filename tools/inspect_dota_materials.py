import vpk
import re

dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')

def inspect_vmat(vmat_path):
    data = dota_pak[vmat_path].read()
    # find strings ending in .vfx, .vtex, etc.
    strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', data)]
    vfx = [s for s in strings if s.endswith('.vfx')]
    vtex = [s for s in strings if s.endswith('.vtex') or s.endswith('.vtex_c')]
    print(f"=== {vmat_path} ===")
    print("  Shader (.vfx):", vfx)
    print("  Referenced textures:")
    for t in sorted(set(vtex)):
        print("   -", t)

inspect_vmat('materials/models/items/windrunner/windrunner_arcana/windranger_arcana_base.vmat_c')
inspect_vmat('materials/models/items/windrunner/windrunner_arcana/windranger_arcana_bow.vmat_c')
inspect_vmat('materials/models/items/windrunner/windrunner_arcana/windranger_arcana_armor.vmat_c')
