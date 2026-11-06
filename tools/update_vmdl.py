import sys
from pathlib import Path

sys.path.insert(0, r"E:\creacion-mods\enigma-dynamo")
from pipeline.make_vmdl import replace_meshes

vmdl_path = Path(r"extracted\archer\models\heroes_staging\archer\archer.vmdl")
text = vmdl_path.read_text(encoding="utf-8")

new_vmdl = replace_meshes(text, "windrunner_classic", "models/heroes_staging/archer/archer_windrunner_body.dmx")
print("New RenderMeshList:")
idx = new_vmdl.find("RenderMeshList")
print(new_vmdl[idx:idx+500])

out_vmdl = Path(r"extracted\archer_windrunner.vmdl")
out_vmdl.write_text(new_vmdl, encoding="utf-8")
print(f"[EXITO] VMDL modificado guardado en {out_vmdl}")
