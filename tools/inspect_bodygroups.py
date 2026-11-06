vmdl = open(r'extracted\archer\models\heroes_staging\archer\archer.vmdl', 'r', encoding='utf-8').read()
idx = vmdl.find('BodyGroupList')
if idx != -1:
    print("BodyGroupList:")
    print(vmdl[idx:idx+1200])
else:
    print("No BodyGroupList found")
