import shutil
from pathlib import Path

src = Path(r"E:\CSDK12\content\citadel_addons\windrunner_classic")
dst = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic")

if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst)
print("Copied to dota content addon:", dst.exists())
