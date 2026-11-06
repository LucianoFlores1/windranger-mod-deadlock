import vpk
from pathlib import Path

pak_path = Path("extracted_mod/pak22_dir.vpk")
pak = vpk.open(str(pak_path))

print(f"=== Files in {pak_path} ===")
for p in sorted(pak):
    if any(k in p.lower() for k in ['vmdl', 'cloth', 'phys', 'archer', 'skeleton', 'anim', 'model']):
        print(f"{p}: {len(pak[p].read()):,} bytes")

