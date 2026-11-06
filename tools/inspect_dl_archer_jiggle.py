import vpk

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
data = dl_pak['models/heroes_staging/archer/archer.vmdl_c'].read()

pos = data.find(b'BaseJigglebon')
if pos != -1:
    print("Found BaseJigglebon in Deadlock archer.vmdl_c at:", pos)
    chunk = data[max(0, pos-100):pos+300]
    print("".join(chr(b) if 32 <= b <= 126 else '.' for b in chunk))
else:
    print("Not found in Deadlock archer.vmdl_c")

