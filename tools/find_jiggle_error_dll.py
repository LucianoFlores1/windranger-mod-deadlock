import glob
import re

for pattern in ['E:/SteamLibrary/steamapps/common/Deadlock/game/bin/win64/*.dll', 'C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/bin/win64/*.dll']:
    for f in glob.glob(pattern):
        try:
            data = open(f, 'rb').read()
            if b'Invalid bone name' in data:
                pos = data.find(b'Invalid bone name')
                chunk = data[pos-100:pos+150]
                text = "".join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                if 'Jiggle' in text or 'jiggle' in text:
                    print(f"{f}: {text}")
        except:
            pass

