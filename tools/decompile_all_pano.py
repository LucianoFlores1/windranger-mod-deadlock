import subprocess
from pathlib import Path
from PIL import Image

cli = r"E:\creacion-mods\enigma-dynamo\tools\vrf_cli\Source2Viewer-CLI.exe"
pano_dir = Path(r"custom_mod_source\panorama\images\heroes")
out_dir = Path(r"extracted\decompiled_pano")
out_dir.mkdir(parents=True, exist_ok=True)

for f in pano_dir.glob("*.vtex_c"):
    dst = out_dir / (f.stem + ".png")
    cmd = [cli, "-i", str(f), "-d", "-o", str(dst)]
    subprocess.run(cmd, capture_output=True)
    if dst.exists():
        im = Image.open(dst)
        print(f"{f.name} -> {dst.name}: size={im.size}")
