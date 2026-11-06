import shutil
from pathlib import Path
import vpk

BASE_DIR = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock")
CUSTOM_MOD = BASE_DIR / "custom_mod_source"
NESTED_VPK = CUSTOM_MOD / "maps" / "ui" / "hero_prefabs" / "archer.vpk"
STAGING = BASE_DIR / "extracted" / "nested_archer_vpk_staging"

if STAGING.exists():
    shutil.rmtree(STAGING)
STAGING.mkdir(parents=True, exist_ok=True)

print("1. Extracting nested archer.vpk...")
pak = vpk.open(str(NESTED_VPK))
for file_path in pak:
    entry = pak[file_path]
    dest = STAGING / file_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(entry.read())

print(f"Extracted {len(pak)} files to {STAGING}")

print("2. Replacing with classic textures from custom_mod_source...")
replaced = 0
for file_path in pak:
    if file_path.endswith('.vtex_c'):
        source_tex = CUSTOM_MOD / file_path
        if source_tex.exists():
            dest = STAGING / file_path
            shutil.copy2(source_tex, dest)
            print(f"  [REPLACED] {file_path} ({source_tex.stat().st_size:,} bytes)")
            replaced += 1
        else:
            print(f"  [WARNING] Not found in custom_mod_source: {file_path}")

print(f"Replaced {replaced} textures in staging.")

print("3. Re-packing archer.vpk...")
new_pak = vpk.new(str(STAGING))
new_pak.save(str(NESTED_VPK))
print(f"[SUCCESS] Re-packed archer.vpk: {NESTED_VPK} ({NESTED_VPK.stat().st_size:,} bytes)")

