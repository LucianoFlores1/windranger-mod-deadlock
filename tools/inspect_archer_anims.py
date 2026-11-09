import re

data = open(r"custom_mod_source\models\heroes_staging\archer\archer.vmdl_c", "rb").read()
# Find animation sequences
seqs = set()
for m in re.finditer(rb'models\/heroes_staging\/archer\/[a-zA-Z0-9_@\.-]+', data):
    seqs.add(m.group(0).decode('latin1'))

print("Total sequence references in archer.vmdl_c:", len(seqs))
for s in sorted(seqs)[:30]:
    print(" ", s)
