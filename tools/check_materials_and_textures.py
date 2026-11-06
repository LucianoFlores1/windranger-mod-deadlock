import re
from pathlib import Path

CUSTOM_MOD = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\custom_mod_source")

vmats = [
    r"models/heroes_staging/archer/materials/teteva.vmat",
    r"models/heroes_staging/archer/materials/windranger_arcana_arrow.vmat",
    r"models/heroes_staging/archer/materials/windranger_arcana_base.vmat",
    r"models/heroes_staging/archer/materials/windranger_arcana_bow.vmat",
    r"models/heroes_staging/archer/materials/windranger_arcana_hair.vmat",
    r"models/heroes_staging/archer/materials/windranger_arcana_head.vmat",
    r"models/heroes_staging/grey_talon/materials/windranger_arcana_armor_style1.vmat",
]

missing_mats = []
missing_texs = []

print("=== CHECKING MATERIALS & TEXTURES IN CUSTOM_MOD_SOURCE ===")
for vmat in vmats:
    vmat_c_path = CUSTOM_MOD / (vmat + "_c")
    if not vmat_c_path.exists():
        print(f"[MISSING MATERIAL] {vmat_c_path}")
        missing_mats.append(vmat)
        continue
    
    data = vmat_c_path.read_bytes()
    strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', data)]
    vtex = [s for s in strings if s.endswith('.vtex') or s.endswith('.vtex_c')]
    print(f"\nMaterial: {vmat} ({vmat_c_path.stat().st_size:,} bytes)")
    for t in sorted(set(vtex)):
        # Normalize path
        t_clean = t.replace('/', '\\')
        if not t_clean.endswith('_c'):
            t_clean += '_c'
        t_path = CUSTOM_MOD / t_clean
        exists = t_path.exists()
        size_str = f"{t_path.stat().st_size:,} bytes" if exists else "NOT FOUND!"
        print(f"  -> Texture: {t_clean} [{'OK' if exists else 'MISSING'}] ({size_str})")
        if not exists:
            missing_texs.append(t_clean)

print("\n=== SUMMARY ===")
print(f"Missing materials: {len(missing_mats)}")
print(f"Missing textures: {len(missing_texs)}")

