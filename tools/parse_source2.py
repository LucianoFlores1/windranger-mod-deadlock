import vpk
import struct

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')

def inspect_res(data, name):
    file_size, header_ver, res_ver = struct.unpack_from('<III', data, 0)
    print(f"=== {name}: size={file_size}, header_ver={header_ver}, res_ver={res_ver} ===")
    
    # In Source 2 resource header:
    # 0x00: FileSize (uint32)
    # 0x04: HeaderVersion (uint16)
    # 0x06: Version (uint16)
    # 0x08: BlockOffset (uint32)
    # 0x0C: BlockCount (uint32)
    block_offset = struct.unpack_from('<I', data, 8)[0]
    block_count = struct.unpack_from('<I', data, 12)[0]
    curr = block_offset + 8 # relative to header or absolute?
    # Actually offset is from the start of block table or from field position
    # Let's inspect bytes around 0x08..0x20:
    print("Header bytes (32):", data[:32].hex())
    
inspect_res(dl_pak['models/heroes_staging/archer/archer.vmdl_c'].read(), 'Deadlock Archer')
inspect_res(dota_pak['models/heroes/windrunner/windrunner.vmdl_c'].read(), 'Dota Windrunner')
