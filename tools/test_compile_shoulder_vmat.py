import subprocess
from pathlib import Path

DOTA_CONTENT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic")
DOTA_GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota_addons\windrunner_classic")
RC = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe"

vmat_text = """// THIS FILE IS AUTO-GENERATED
Layer0
{
	shader "global_lit_simple.vfx"

	//---- Color ----
	g_tColor "materials/classic_textures/windrunner_shoulders_color.vtex"
}
"""

vmat_path = DOTA_CONTENT / "materials" / "models" / "heroes_staging" / "archer" / "windrunner_shoulders.vmat"
vmat_path.parent.mkdir(parents=True, exist_ok=True)
vmat_path.write_text(vmat_text, encoding="utf-8")

cmd = [RC, "-i", str(vmat_path)]
p = subprocess.run(cmd, capture_output=True, text=True)
print(f"RC exit: {p.returncode}")
print(p.stdout)

out_vmat_c = DOTA_GAME / "materials" / "models" / "heroes_staging" / "archer" / "windrunner_shoulders.vmat_c"
print(f"Compiled vmat exists: {out_vmat_c.exists()} ({out_vmat_c.stat().st_size if out_vmat_c.exists() else 0} bytes)")

