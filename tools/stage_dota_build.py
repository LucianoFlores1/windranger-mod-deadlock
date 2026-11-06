import shutil
from pathlib import Path
import subprocess

base = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock")
dota_content = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic")
model_dir = dota_content / "models" / "heroes_staging" / "archer"

# 1. Copy DMX
shutil.copy2(base / r"extracted\archer_windrunner_body.dmx", model_dir / "archer_windrunner_body.dmx")
print("Copied DMX to dota content")

# 2. Stub materials for all 6 face sets
stub_vmat = '''Layer0
{
	shader "global_lit_simple.vfx"
}
'''
mats = [
    dota_content / "models/heroes_staging/archer/materials/windranger_arcana_base.vmat",
    dota_content / "models/heroes_staging/archer/materials/windranger_arcana_hair.vmat",
    dota_content / "models/heroes_staging/archer/materials/windranger_arcana_head.vmat",
    dota_content / "models/heroes_staging/grey_talon/materials/windranger_arcana_armor_style1.vmat",
    dota_content / "models/heroes_staging/archer/materials/windranger_arcana_arrow.vmat",
    dota_content / "models/heroes_staging/archer/materials/windranger_arcana_bow.vmat",
]
for m in mats:
    m.parent.mkdir(parents=True, exist_ok=True)
    m.write_text(stub_vmat, encoding="utf-8")
print("Staged stub materials")

# 3. Compile archer.vmdl
vmdl_path = model_dir / "archer.vmdl"
cmd = [
    r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe",
    "-i", str(vmdl_path)
]
print("Running resourcecompiler...")
p = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", p.returncode)
print(p.stdout)
if p.stderr:
    print("STDERR:", p.stderr)
