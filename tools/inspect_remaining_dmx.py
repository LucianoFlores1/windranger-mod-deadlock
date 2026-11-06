import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
import datamodel as dm

for name in ['archer_teteva.dmx', 'archer_arrowb2.dmx', 'archer_respawn_countdown_idle.dmx']:
    d = dm.load(f'extracted/{name}')
    model = d.root.get('model')
    if model:
        dags = [c for c in model['children'] if c.type == 'DmeDag' and c.get('shape')]
        for c in dags:
            shape = c['shape']
            vd = shape['currentState']
            print(name, c.name, len(vd['position$0']), [fs['material']['mtlName'] for fs in shape['faceSets']])
    else:
        print(name, 'keys:', list(d.root.keys()))

