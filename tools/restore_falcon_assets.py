import vpk
from pathlib import Path
import shutil

BASE_DIR = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock")
CUSTOM_MOD = BASE_DIR / "custom_mod_source"
ORIG_PAK = vpk.open(r"extracted_mod\pak22_dir.vpk")

falcon_files = [
    "models/heroes_staging/grey_talon/grey_talon_owl.vmdl_c",
    "models/heroes_staging/grey_talon/materials/windranger_arcana_armor_style1.vmat_c",
    "models/heroes_staging/grey_talon/materials/windranger_ti8_immortal_shoulders_style1_color_psd_3b3faa18_upscayl_4x_high-fidelity-4x_png_3dbdd27f.vtex_c",
    "models/heroes_staging/grey_talon/materials/windranger_ti8_immortal_shoulders_style1_color_psd_3b3faa18_upscayl_4x_high-fidelity-4x_png_d62e4d57.vtex_c",
    "models/heroes_staging/grey_talon/materials/windrunner_shoulderpads_normal_psd_72d84f0a_png_ebb635f9.vtex_c",
]

print("1. Restoring Falcon assets to custom_mod_source...")
for f in falcon_files:
    dest = CUSTOM_MOD / f
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(ORIG_PAK[f].read())
    print(f"  [RESTORED] {f} ({dest.stat().st_size:,} bytes)")

# Also update nested archer.vpk
nested_vpk_path = CUSTOM_MOD / "maps" / "ui" / "hero_prefabs" / "archer.vpk"
staging = BASE_DIR / "extracted" / "nested_archer_vpk_staging"
if staging.exists():
    shutil.rmtree(staging)
staging.mkdir(parents=True, exist_ok=True)

print("\n2. Updating nested archer.vpk with restored falcon assets...")
nested = vpk.open(str(nested_vpk_path))
for p in nested:
    dest = staging / p
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(nested[p].read())

for f in falcon_files:
    dest = staging / f
    if dest.exists():
        dest.write_bytes(ORIG_PAK[f].read())
        print(f"  [NESTED UPDATED] {f} ({dest.stat().st_size:,} bytes)")

# Repack nested vpk
new_nested = vpk.new(str(staging))
new_nested.save(str(nested_vpk_path))
print(f"[SUCCESS] Nested archer.vpk re-packed: {nested_vpk_path} ({nested_vpk_path.stat().st_size:,} bytes)")

