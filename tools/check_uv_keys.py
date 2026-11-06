import datamodel as dm
from pathlib import Path

for name in ['archer_warka3_orig.dmx', 'archer_bow1_orig.dmx']:
    d = dm.load(str(Path('extracted') / name))
    c = next(c for c in d.root['model']['children'] if c.type == 'DmeDag')
    vd = c['shape']['currentState']
    uv_keys = [k for k in vd.keys() if 'tex' in k.lower()]
    print(name, "UV keys:", uv_keys)

