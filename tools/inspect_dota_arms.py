import sys
sys.path.insert(0, "tools")
import datamodel

dm = datamodel.load("extracted/windrunner/models/heroes/windrunner/windrunner_windranger_base_arms2.dmx")
root = dm.root
joints = [j.name for j in root['skeleton']['jointList']]
print(f"Total joints in Dota 2 base_arms2: {len(joints)}")
for j in joints:
    print("  ", j)

