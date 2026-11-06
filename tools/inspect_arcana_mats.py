import os
import re

mat_dir = r"custom_mod_source/models/heroes_staging/archer/materials"
for f in os.listdir(mat_dir):
    if f.endswith('.vmat_c'):
        path = os.path.join(mat_dir, f)
        data = open(path, 'rb').read()
        strings = [s.decode('latin1', errors='ignore') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', data)]
        vtex = [s for s in strings if s.endswith('.vtex') or s.endswith('.vtex_c') or s.endswith('.png')]
        print(f"=== {f} ===")
        for t in sorted(set(vtex)):
            print("  ", t)
