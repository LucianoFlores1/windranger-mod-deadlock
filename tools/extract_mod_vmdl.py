import vpk
from pathlib import Path

pak = vpk.open(r'extracted_mod\pak22_dir.vpk')
entry = pak['models/heroes_staging/archer/archer.vmdl_c']
out_path = Path(r'extracted\mod_archer.vmdl_c')
out_path.write_bytes(entry.read())
print(f"Extracted {out_path} ({out_path.stat().st_size:,} bytes)")

