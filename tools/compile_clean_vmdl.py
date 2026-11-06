import os
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock")
DOTA_CONTENT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic")
DOTA_GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota_addons\windrunner_classic")
RC = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe"

model_dir = DOTA_CONTENT / "models" / "heroes_staging" / "archer"
model_dir.mkdir(parents=True, exist_ok=True)

# 1. Copy the clean DMX files
dmx_files = [
    "archer_teteva.dmx",
    "archer_bow1.dmx",
    "archer_arrowb2.dmx",
    "archer_warka3.dmx",
    "archer_respawn_countdown_idle.dmx"
]

for dmx_name in dmx_files:
    src = BASE_DIR / "extracted" / dmx_name
    dst = model_dir / dmx_name
    shutil.copy2(src, dst)
    print(f"Copied {dmx_name} ({dst.stat().st_size:,} bytes)")

# 2. Write clean vmdl
vmdl_text = (BASE_DIR / "extracted" / "mod_archer_gltf").read_text(encoding="utf-8")
(model_dir / "archer.vmdl").write_text(vmdl_text, encoding="utf-8")
print("Wrote archer.vmdl")

# 3. Create stub materials
stub = 'Layer0\n{\n\tshader "global_lit_simple.vfx"\n}\n'
archer_mats = [
    "teteva.vmat",
    "windranger_arcana_arrow.vmat",
    "windranger_arcana_base.vmat",
    "windranger_arcana_bow.vmat",
    "windranger_arcana_hair.vmat",
    "windranger_arcana_head.vmat",
]
for m in archer_mats:
    p = model_dir / "materials" / m
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(stub, encoding="utf-8")

gt_mat = DOTA_CONTENT / "models" / "heroes_staging" / "grey_talon" / "materials" / "windranger_arcana_armor_style1.vmat"
gt_mat.parent.mkdir(parents=True, exist_ok=True)
gt_mat.write_text(stub, encoding="utf-8")

# 4. Compile with Dota 2 resourcecompiler
cmd = [RC, "-i", str(model_dir / "archer.vmdl")]
print("Compiling archer.vmdl...")
p = subprocess.run(cmd, capture_output=True, text=True)
print(f"RC exit: {p.returncode}")
print("STDOUT:", p.stdout)
if p.stderr:
    print("STDERR:", p.stderr)

out_vmdl_c = DOTA_GAME / "models" / "heroes_staging" / "archer" / "archer.vmdl_c"
if out_vmdl_c.exists():
    print(f"[SUCCESS] Compiled archer.vmdl_c exists: {out_vmdl_c} ({out_vmdl_c.stat().st_size:,} bytes)")
else:
    print("[ERROR] Output archer.vmdl_c not found!")

