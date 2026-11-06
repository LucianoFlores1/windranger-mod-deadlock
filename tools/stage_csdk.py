import subprocess
import shutil
from pathlib import Path

# Setup addon dir in CSDK
addon_name = "windrunner_classic"
csdk_content = Path(r"E:\CSDK12\content\citadel_addons") / addon_name
model_dir = csdk_content / "models" / "heroes_staging" / "archer"
model_dir.mkdir(parents=True, exist_ok=True)

# Also create materials dir with stub materials so compiler is happy
mat_dir = model_dir / "materials"
mat_dir.mkdir(parents=True, exist_ok=True)
stub = '''Layer0
{
\tshader "global_lit_simple.vfx"
}
'''
(mat_dir / "windrunner_classic.vmat").write_text(stub, encoding="utf-8")
(mat_dir / "archer.vmat").write_text(stub, encoding="utf-8")

# Copy DMX and vmdl
shutil.copy2(r"extracted\archer_windrunner_body.dmx", model_dir / "archer_windrunner_body.dmx")
# Copy vnmskel
shutil.copy2(r"extracted\archer\models\heroes_staging\archer\archer.vnmskel", model_dir / "archer.vnmskel")

print("Files staged. Ready to test clean VMDL.")
