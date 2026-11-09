from pathlib import Path
import re

mat_dir = Path(r"custom_mod_source\models\heroes_staging\archer\materials")
for vmat in mat_dir.glob("*.vmat_c"):
    data = vmat.read_bytes()
    textures = re.findall(rb'[a-zA-Z0-9_\/\\.-]+\.vtex', data)
    print(vmat.name)
    for t in set(textures):
        print("  ->", t.decode('latin1'))
