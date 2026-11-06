import re

vmdl = open(r'extracted\archer\models\heroes_staging\archer\archer.vmdl', 'r', encoding='utf-8').read()
classes = re.findall(r'_class\s*=\s*"(\w+)"', vmdl)
print("Unique classes in archer.vmdl:", set(classes))

# RenderMeshList
idx = vmdl.find('RenderMeshList')
if idx != -1:
    print("\nRenderMeshList snippet:")
    print(vmdl[idx:idx+800])
