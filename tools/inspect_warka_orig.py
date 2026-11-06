import sys
sys.path.insert(0, "tools")
import datamodel

dm = datamodel.load("extracted/archer_warka3_orig.dmx")
print("Format:", dm.format)
root = dm.root
print("Root name:", root.name)

# Inspect skeleton / joints
skeleton = root.get("skeleton")
if skeleton:
    joints = skeleton.get("joints")
    print(f"Total joints in orig warka3: {len(joints)}")
    for j in joints[:25]:
        print("Joint:", j.name)
    # Check for cloth / cape / jiggle joints
    cloth_joints = [j.name for j in joints if any(k in j.name.lower() for k in ['cape', 'cloth', 'jiggle', 'quiver', 'hair', 'skirt', 'coat'])]
    print("Cloth / Cape joints in orig warka3:", cloth_joints)

# Inspect combination / channels or delta states
mesh = root.get("combinationOperator")
if mesh:
    print("Combination targets:", [t.name for t in mesh.get("targets", [])])

