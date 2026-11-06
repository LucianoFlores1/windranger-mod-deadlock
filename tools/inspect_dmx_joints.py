import sys
from pathlib import Path
sys.path.insert(0, 'tools')
import datamodel as dm

dmx_path = r'extracted\archer\models\heroes_staging\archer\archer_body.dmx'
d = dm.load(dmx_path)
model = d.root["model"]
joints = [j.name for j in model["jointList"]]
print(f"Archer DMX jointList count: {len(joints)}")
print("Joints sample:", joints[:40])
