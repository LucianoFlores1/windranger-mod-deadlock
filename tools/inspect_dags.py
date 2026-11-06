import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo\tools')
import datamodel as dm

d = dm.load(r'extracted\archer\models\heroes_staging\archer\archer_body.dmx')
model = d.root['model']

dags = [c for c in model['children'] if c.type == 'DmeDag']
print(f"Total DmeDag children: {len(dags)}")
for i, c in enumerate(dags):
    shape = c.get('shape')
    shape_name = shape.name if shape else 'None'
    shape_type = shape.type if shape else 'None'
    print(f"Dag {i}: name='{c.name}', shape='{shape_name}' ({shape_type})")

