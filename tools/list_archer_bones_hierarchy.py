import vpk
import re

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
data = dl_pak['models/heroes_staging/archer/archer.vmdl_c'].read()

# Let's inspect extracted/mod_archer_gltf which has the full Bone hierarchy in ModelDoc format!
from pathlib import Path
text = Path("extracted/mod_archer_gltf").read_text(encoding="utf-8")

# Extract all Bone names
bones = re.findall(r'_class\s*=\s*"Bone"\s*name\s*=\s*"([^"]+)"', text)
print(f"Total bones in mod_archer_gltf: {len(bones)}")
for b in sorted(bones):
    print("Bone:", b)

