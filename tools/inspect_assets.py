import vpk
import re

deadlock_vpk = r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk'
dl_pak = vpk.open(deadlock_vpk)

print("Files in Deadlock containing 'archer':")
archer_vdata = [f for f in dl_pak if 'archer' in f.lower() and (f.endswith('.vdata_c') or f.endswith('.vcfg_c') or f.endswith('.txt'))]
for f in archer_vdata:
    print("  ", f)

archer_all = [f for f in dl_pak if 'heroes_staging/archer' in f.lower() or 'heroes/archer' in f.lower() or 'grey_talon' in f.lower()]
print(f"Total archer/grey_talon files: {len(archer_all)}")
for f in archer_all:
    if f.endswith('.vmdl_c'):
        print("  Model:", f)
