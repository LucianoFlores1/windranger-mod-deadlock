from pathlib import Path
import shutil
import subprocess

dota_content = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic")
model_dir = dota_content / "models" / "heroes_staging" / "archer"

# 1. Copy the 4 dmx files to dota content
for dmx_name in ["archer_teteva.dmx", "archer_bow1.dmx", "archer_arrowb2.dmx", "archer_warka3.dmx", "archer_respawn_countdown_idle.dmx"]:
    src = Path(f"extracted\\{dmx_name}")
    shutil.copy2(src, model_dir / dmx_name)

# 2. Write vmdl using modder's clean structure
vmdl_text = Path("extracted/mod_archer_gltf").read_text(encoding="utf-8")
(model_dir / "archer.vmdl").write_text(vmdl_text, encoding="utf-8")

# 3. Create stub materials for all referenced vmats
stub = 'Layer0\n{\n\tshader "global_lit_simple.vfx"\n}\n'
for m_name in ["teteva.vmat", "windranger_arcana_arrow.vmat", "windranger_arcana_base.vmat", "windranger_arcana_bow.vmat", "windranger_arcana_hair.vmat", "windranger_arcana_head.vmat"]:
    p = model_dir / "materials" / m_name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(stub, encoding="utf-8")

# 4. Compile with Dota 2 resourcecompiler
rc = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe"
cmd = [rc, "-i", str(model_dir / "archer.vmdl")]
print("Compiling clean archer.vmdl...")
p = subprocess.run(cmd, capture_output=True, text=True)
print(f"RC exit: {p.returncode}")
print(p.stdout)
if p.stderr:
    print("STDERR:", p.stderr)

