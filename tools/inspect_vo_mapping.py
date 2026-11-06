from pathlib import Path
import vpk

orion_vo_dir = Path(r"custom_mod_source\sounds\vo\orion")
orion_files = sorted([f.name for f in orion_vo_dir.glob("*.vsnd_c")])

dota_pak = vpk.open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk")
dota_lines = sorted([p for p in dota_pak if p.lower().startswith('sounds/vo/windrunner/wind_')])

print(f"Target Orion voice files: {len(orion_files)}")
print(f"Source Dota 2 classic lines: {len(dota_lines)}")

# Let's inspect some of orion files
print("\nSample Orion files:")
for f in orion_files[:15]:
    print(" ", f)

print("\nSample Dota 2 lines:")
for f in dota_lines[:15]:
    print(" ", f.split('/')[-1])

