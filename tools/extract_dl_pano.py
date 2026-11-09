import subprocess
from pathlib import Path
from PIL import Image

cli = r"E:\creacion-mods\enigma-dynamo\tools\vrf_cli\Source2Viewer-CLI.exe"
dl_vpk = r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk"
out_dir = Path(r"extracted\dl_orig_pano")
out_dir.mkdir(parents=True, exist_ok=True)

targets = [
    "panorama/images/heroes/archer_card_critical_psd.vtex_c",
    "panorama/images/heroes/archer_card_gloat_psd.vtex_c",
    "panorama/images/heroes/archer_card_psd.vtex_c",
    "panorama/images/heroes/archer_mm_psd.vtex_c",
    "panorama/images/heroes/archer_sm_psd.vtex_c",
    "panorama/images/heroes/archer_vertical_psd.vtex_c",
    "panorama/images/heroes/backgrounds/grey_talon_bg_psd.vtex_c",
]

for t in targets:
    subprocess.run([cli, "-i", dl_vpk, "-f", t, "-d", "-o", str(out_dir)], capture_output=True)

for p in out_dir.rglob("*.png"):
    print(p.name, Image.open(p).size)
