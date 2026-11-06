import vpk
import re

mod_pak = vpk.open(r'extracted_mod\pak22_dir.vpk')

def inspect_mod_vmat(vmat_path):
    data = mod_pak[vmat_path].read()
    strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', data)]
    vfx = [s for s in strings if s.endswith('.vfx')]
    vtex = [s for s in strings if s.endswith('.vtex') or s.endswith('.vtex_c')]
    print(f"=== Mod {vmat_path} ===")
    print("  Shader (.vfx):", set(vfx))
    print("  Referenced textures:")
    for t in sorted(set(vtex)):
        print("   -", t)

inspect_mod_vmat('models/heroes_staging/archer/materials/windranger_arcana_base.vmat_c')
inspect_mod_vmat('models/heroes_staging/archer/materials/windranger_arcana_bow.vmat_c')
