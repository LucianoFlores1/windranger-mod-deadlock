import re

data = open(r"custom_mod_source\models\heroes_staging\archer\archer.vmdl_c", "rb").read()
vmats = set()
for match in re.finditer(rb'materials\/[a-zA-Z0-9_\/\\.-]+\.vmat', data):
    vmats.add(match.group(0).decode('latin1'))

print("Materials referenced by archer.vmdl_c:")
for m in sorted(vmats):
    print("  ->", m)
