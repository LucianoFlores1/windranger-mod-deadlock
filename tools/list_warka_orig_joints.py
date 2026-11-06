import sys
sys.path.insert(0, "tools")
import datamodel

dm = datamodel.load("extracted/archer_warka3_orig.dmx")
root = dm.root
joints = [j.name for j in root['skeleton']['jointList']]
print(f"Total joints: {len(joints)}")

# Filter cloth, cape, skirt, jiggle, hair, coat, etc.
for j in joints:
    if any(k in j.lower() for k in ['cape', 'cloth', 'jiggle', 'quiver', 'hair', 'skirt', 'coat', 'ribbon', 'tassel', 'sleeve', 'flaps', 'flap', 'feather']):
        print("  Found:", j)

