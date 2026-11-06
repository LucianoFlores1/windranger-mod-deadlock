import vpk
from pathlib import Path

mod_pak = vpk.open(r'extracted_mod\pak22_dir.vpk')
for p in sorted(mod_pak):
    if 'grey_talon/materials' in p:
        sz = len(mod_pak[p].read())
        print(f"{p} ({sz:,} bytes)")

