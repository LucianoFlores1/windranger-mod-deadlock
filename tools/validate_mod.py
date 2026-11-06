import vpk

pak = vpk.open(r'e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted_mod\pak22_dir.vpk')
print(f"Total files in mod VPK: {len(pak)}")
corrupt = 0
for f in pak:
    try:
        data = pak[f].read()
        if len(data) == 0:
            print(f"Warning: {f} has 0 bytes")
    except Exception as e:
        print(f"Error reading {f}: {e}")
        corrupt += 1

print(f"Validation complete! Corrupted files: {corrupt}")
