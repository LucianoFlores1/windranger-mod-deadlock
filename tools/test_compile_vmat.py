import subprocess
from pathlib import Path

test_dir = Path(r"E:\CSDK12\content\citadel_addons\test_mat")
mat_dir = test_dir / "materials"
mat_dir.mkdir(parents=True, exist_ok=True)
vmat = mat_dir / "test.vmat"
vmat.write_text('''Layer0
{
    shader "pbr.vfx"
}
''', encoding="utf-8")

cmd = [
    r"E:\CSDK12\game\bin_cs2\win64\resourcecompiler.exe",
    "-game", r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel",
    "-i", str(vmat)
]
p = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", p.returncode)
print("STDOUT:", p.stdout)
print("STDERR:", p.stderr)
