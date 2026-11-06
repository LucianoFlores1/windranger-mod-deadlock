import vpk

dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')
arcana = [f for f in dota_pak if 'windrunner' in f.lower() and ('arcana' in f.lower() or 'compass' in f.lower())]
print(f"Arcana files: {len(arcana)}")
for f in arcana:
    if f.endswith('.vmdl_c'):
        print("  ", f)
