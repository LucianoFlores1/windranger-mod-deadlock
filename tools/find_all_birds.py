import vpk
import re

pak = vpk.open(r'extracted_mod\pak22_dir.vpk')
for p in sorted(pak):
    if p.endswith('.vmdl_c'):
        data = pak[p].read()
        strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', data)]
        has_bird = any('owl' in s.lower() or 'hawk' in s.lower() or 'bird' in s.lower() for s in strings)
        print(f"Model {p}: has_bird={has_bird}")

