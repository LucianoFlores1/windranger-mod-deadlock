import vpk

pak = vpk.open("extracted_mod/pak22_dir.vpk")
data = pak['models/heroes_staging/archer/archer.vmdl_c'].read()

pos = data.find(b'BaseJigglebon')
if pos != -1:
    print("Found BaseJigglebon in mod pak22 at:", pos)
else:
    print("Not found in mod pak22")

