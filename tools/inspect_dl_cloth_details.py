import vpk

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
data = dl_pak['models/heroes_staging/archer/archer.vmdl_c'].read()

for target in [b'skirt', b'cloth_m0p', b'tail', b'gtail']:
    pos = 0
    while True:
        pos = data.find(target, pos)
        if pos == -1:
            break
        print(f"Found {target} at {pos}:")
        chunk = data[max(0, pos-40):pos+60]
        print(" ", "".join(chr(b) if 32 <= b <= 126 else '.' for b in chunk))
        pos += len(target)

