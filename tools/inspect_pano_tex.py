from pathlib import Path
import struct

pano_dir = Path(r"custom_mod_source\panorama\images\heroes")
for f in pano_dir.glob("*.vtex_c"):
    data = f.read_bytes()
    # Check vtex header
    print(f.name, len(data), "bytes")
