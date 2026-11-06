import vpk

dota_pak = vpk.open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk")
print("Searching Dota 2 VPK for Windrunner voice lines...")

vo_files = []
for p in dota_pak:
    if 'windrunner' in p.lower() and ('sounds/vo' in p.lower() or 'sound/vo' in p.lower() or 'vo/windrunner' in p.lower()):
        vo_files.append(p)

print(f"Total Windrunner VO files found: {len(vo_files)}")
# Separate classic from arcana
classic_vo = [f for f in vo_files if 'arcana' not in f.lower()]
arcana_vo = [f for f in vo_files if 'arcana' in f.lower()]

print(f"Classic Windrunner VO files: {len(classic_vo)}")
print(f"Arcana Windrunner VO files: {len(arcana_vo)}")

for f in classic_vo[:20]:
    print("  ", f)

