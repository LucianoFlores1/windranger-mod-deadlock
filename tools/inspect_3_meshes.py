import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo\tools')
import datamodel as dm

d = dm.load(r'extracted\archer\models\heroes_staging\archer\archer_body.dmx')
model = d.root['model']

dags = [c for c in model['children'] if c.type == 'DmeDag']
for i, c in enumerate(dags):
    mesh = c['shape']
    vd = mesh['currentState']
    pos = vd.get('position$0')
    pos_count = len(pos) if pos else 0
    mats = [fs['material']['mtlName'] for fs in mesh.get('faceSets', [])]
    print(f"Mesh {i}: verts={pos_count}, materials={mats}")

