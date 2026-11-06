import vpk
import re

pak = vpk.open("extracted_mod/pak22_dir.vpk")
vmdl_bytes = pak['models/heroes_staging/archer/archer.vmdl_c'].read()

# Find strings in binary
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{4,}', vmdl_bytes)]
print("Total strings:", len(strings))

print("\n--- Cloth / Phys / Jiggle strings ---")
for s in strings:
    if any(k in s.lower() for k in ['cloth', 'phys', 'jiggle', 'spring', 'simulat', 'dynamic', 'chain', 'wind']):
        print(s)

print("\n--- Meshes / DMX references ---")
for s in strings:
    if any(k in s.lower() for k in ['.dmx', '.smd', '.fbx', 'mesh', 'group']):
        print(s)

print("\n--- Attachment / Bones ---")
bow_bones = [s for s in set(strings) if any(k in s.lower() for k in ['bow', 'weapon', 'arrow', 'string', 'teteva', 'hand', 'quiver'])]
print("Weapon/Hand bones & attachments:", bow_bones)

