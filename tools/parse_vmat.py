from pathlib import Path
import struct

vmat_path = Path(r"custom_mod_source/models/heroes_staging/archer/materials/windranger_arcana_base.vmat_c")
data = vmat_path.read_bytes()

# Parse header
# Valve Resource header:
# 4 bytes size, 2 bytes headerVersion, 2 bytes version, 4 bytes blockOffset, 4 bytes blockCount
size, headerVer, ver, blockOff, blockCount = struct.unpack_from("<IHHII", data, 0)
print(f"Header: size={size}, headerVer={headerVer}, ver={ver}, blockOff={blockOff}, blockCount={blockCount}")

# Read blocks
blocks = []
for i in range(blockCount):
    tag, offset, bsize = struct.unpack_from("<4sII", data, 16 + i * 12)
    tag_str = tag.decode('latin1')
    blocks.append((tag_str, offset + 16 + i * 12, bsize))
    print(f"Block {tag_str}: offset={offset + 16 + i * 12}, size={bsize}")

# Check RERL (Resource External Reference List)
rerl = [b for b in blocks if b[0] == 'RERL'][0]
offset, bsize = rerl[1], rerl[2]
rerl_data = data[offset:offset+bsize]

entry_count = struct.unpack_from("<I", rerl_data, 0)[0]
print(f"RERL entries: {entry_count}")
pos = 4
for i in range(entry_count):
    res_id, str_offset = struct.unpack_from("<QQ", rerl_data, pos)
    # str_offset is relative to start of this entry
    str_pos = pos + 8 + str_offset
    end_pos = rerl_data.find(b'\x00', str_pos)
    res_name = rerl_data[str_pos:end_pos].decode('latin1')
    print(f" Entry {i}: id={res_id:016x}, name={res_name}")
    pos += 16
