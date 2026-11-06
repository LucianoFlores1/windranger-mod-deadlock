import vpk

dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')

arcana_files = [f for f in dota_pak if 'windrunner_arcana' in f.lower() or 'wr_arcana' in f.lower()]
print(f"Total Arcana files in Dota 2: {len(arcana_files)}")

by_ext = {}
for f in arcana_files:
    ext = f.split('.')[-1]
    by_ext.setdefault(ext, []).append(f)

for ext, flist in by_ext.items():
    print(f"  .{ext}: {len(flist)} files")

print("\n--- Model files (.vmdl_c):")
for f in sorted(by_ext.get('vmdl_c', [])):
    if 'base' in f or 'head' in f or 'cape' in f or 'shoulder' in f or 'weapon' in f or 'quiver' in f or 'arrow' in f:
        print("  ", f)

print("\n--- Material files (.vmat_c) sample:")
for f in sorted(by_ext.get('vmat_c', []))[:15]:
    print("  ", f)
