import vpk

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
all_archer = [f for f in dl_pak if 'archer' in f.lower()]
print(f"Total archer entries: {len(all_archer)}")

by_ext = {}
for f in all_archer:
    ext = f.split('.')[-1]
    by_ext.setdefault(ext, []).append(f)

for ext, files in by_ext.items():
    print(f"Extension .{ext}: {len(files)} files")
    for sample in files[:5]:
        print(f"   {sample}")
