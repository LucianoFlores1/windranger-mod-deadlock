import subprocess
from pathlib import Path

cli = r"E:\creacion-mods\enigma-dynamo\tools\vrf_cli\Source2Viewer-CLI.exe"
dota_vpk = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk"
out_dir = Path(r"extracted\dota_wr_pano")
out_dir.mkdir(parents=True, exist_ok=True)

files = [
    "panorama/images/heroes/npc_dota_hero_windrunner_png.vtex_c",
    "panorama/images/heroes/selection/npc_dota_hero_windrunner_png.vtex_c",
    "panorama/images/heroes/icons/npc_dota_hero_windrunner_png.vtex_c",
    "panorama/images/econ/sets/v2/npc_dota_hero_windrunner_0_png.vtex_c",
]

for f in files:
    cmd = [cli, "-i", dota_vpk, "-f", f, "-d", "-o", str(out_dir)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f, "->", res.returncode)
