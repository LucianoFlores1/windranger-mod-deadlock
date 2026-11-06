import os
import subprocess

cli = r"E:\creacion-mods\enigma-dynamo\tools\vrf_cli\Source2Viewer-CLI.exe"
out_dir = r"extracted\gltf\windrunner"
os.makedirs(out_dir, exist_ok=True)

models = [
    r"e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner.vmdl_c",
    r"e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_head.vmdl_c",
    r"e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_cape.vmdl_c",
    r"e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_shoulderpads.vmdl_c",
    r"e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_quiver.vmdl_c",
    r"e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_bow.vmdl_c",
]

for m in models:
    name = os.path.basename(m)
    print(f"Decompiling {name} -> GLB...")
    cmd = [cli, "-i", m, "-o", out_dir, "-d", "--gltf_export_format", "glb"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error decompiling {name}:", res.stderr)
    else:
        print(f"  OK {name}")

print("\nFiles in GLB directory:")
for f in os.listdir(out_dir):
    print("  ", f)
