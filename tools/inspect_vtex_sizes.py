import struct
import os

def inspect_vtex(path):
    with open(path, 'rb') as f:
        data = f.read()
    # Source 2 VTEX_C format:
    # 0x00: File size (uint32)
    # Header format: search for DATA block
    idx = data.find(b'DATA')
    if idx != -1:
        # DATA block offset
        # In VTEX, DATA block contains width, height, depth, num_levels, format
        # Format descriptor at data_offset:
        data_block = data[idx:]
        print(f"{os.path.basename(path)}: total_size={len(data):,} bytes")

for root, _, files in os.walk(r'custom_mod_source\models\heroes_staging\archer\materials'):
    for f in files:
        if f.endswith('.vtex_c'):
            inspect_vtex(os.path.join(root, f))
