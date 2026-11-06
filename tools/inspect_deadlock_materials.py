import vpk
import re

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')

def inspect_vmat_dl(vmat_path):
    data = dl_pak[vmat_path].read()
    strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', data)]
    vfx = [s for s in strings if s.endswith('.vfx')]
    vtex = [s for s in strings if s.endswith('.vtex') or s.endswith('.vtex_c')]
    print(f"=== Deadlock {vmat_path} ===")
    print("  Shader (.vfx):", set(vfx))
    print("  Referenced textures:")
    for t in sorted(set(vtex)):
        print("   -", t)

inspect_vmat_dl('models/heroes_staging/archer/materials/archer.vmat_c')
inspect_vmat_dl('models/heroes_staging/archer/bow/materials/archer_bow.vmat_c')
