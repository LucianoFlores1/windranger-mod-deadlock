import subprocess
from pathlib import Path
import vpk

cli = r"E:\creacion-mods\enigma-dynamo\tools\vrf_cli\Source2Viewer-CLI.exe"
pak_path = r"extracted_mod\pak22_dir.vpk"
out_dir = Path(r"extracted\orig_mod_pano")
out_dir.mkdir(parents=True, exist_ok=True)

pak = vpk.open(pak_path)
for k in pak:
    if "panorama/images/heroes/archer" in k:
        # Extract raw vtex_c first
        dest_vtex = out_dir / Path(k).name
        dest_vtex.write_bytes(pak[k].read())
        # Decompile with cli
        cmd = [cli, "-i", str(dest_vtex), "-d", "-o", str(out_dir)]
        subprocess.run(cmd, capture_output=True)
        print("Decompiled:", k)
