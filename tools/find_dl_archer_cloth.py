import vpk

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
for p in sorted(dl_pak):
    if 'archer' in p.lower() and any(k in p.lower() for k in ['cloth', 'phys', 'anim', 'graph']):
        print(p)

