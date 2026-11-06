import vpk

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
staging_archer = [f for f in dl_pak if 'models/heroes_staging/archer' in f.lower() and not f.endswith('.vnmclip_c')]
for f in sorted(staging_archer):
    print(f)
