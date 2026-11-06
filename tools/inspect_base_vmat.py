import os
import re

vmat_path = r'custom_mod_source\models\heroes_staging\archer\materials\windranger_arcana_base.vmat_c'
with open(vmat_path, 'rb') as f:
    data = f.read()

# Inspect strings in binary KV3 / RERL
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', data)]
print("Strings in windranger_arcana_base.vmat_c:")
for s in strings:
    if any(s.endswith(ext) for ext in ['.vfx', '.vtex', '.vmat', '.png']):
        print("  ", s)
