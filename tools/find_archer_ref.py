import vpk

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
target = b'models/heroes_staging/archer/archer.vmdl'

candidates = [f for f in dl_pak if f.startswith('scripts/') or f.startswith('animgraphs/') or 'hero' in f.lower() or f.endswith('.vdata_c')]
print(f"Scanning {len(candidates)} candidate files...")

found_in = []
for fname in candidates:
    try:
        data = dl_pak[fname].read()
        if target in data:
            found_in.append(fname)
    except Exception as e:
        pass

print("Target found in candidate files:")
for f in found_in:
    print("  ", f)
