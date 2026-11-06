import shutil
from pathlib import Path

src = Path(r"extracted\archer\models\heroes_staging\archer")
dst = Path(r"E:\CSDK12\content\citadel_addons\windrunner_classic\models\heroes_staging\archer")

count = 0
for f in src.iterdir():
    if f.is_file() and f.suffix in (".dmx", ".vnmskel", ".vmdl"):
        # don't overwrite archer.vmdl or archer_windrunner_body.dmx
        if f.name in ("archer.vmdl", "archer_windrunner_body.dmx"):
            continue
        target = dst / f.name
        if not target.exists():
            shutil.copy2(f, target)
            count += 1
    elif f.is_dir():
        shutil.copytree(f, dst / f.name, dirs_exist_ok=True)

print(f"Copied {count} files and directories to {dst}")
