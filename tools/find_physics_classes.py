import glob
import re

for pattern in ['E:/SteamLibrary/steamapps/common/Deadlock/game/bin/win64/*.dll', 'C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/bin/win64/*.dll']:
    for f in glob.glob(pattern):
        try:
            content = open(f, 'rb').read()
            matches = re.findall(rb'(?:C_?)?(?:Jiggle|Cloth|Procedural|DynamicBone|Spring)[a-zA-Z0-9_]+', content)
            if matches:
                names = set(m.decode('latin1') for m in matches)
                useful = [n for n in names if any(k in n.lower() for k in ['jiggle', 'clothchain', 'dynamicbone', 'procedural'])]
                if useful:
                    print(f"{f}: {useful[:5]}")
        except:
            pass

