import glob
import re

for pattern in ['E:/SteamLibrary/steamapps/common/Deadlock/game/bin/win64/*.dll', 'C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/bin/win64/*.dll']:
    for f in glob.glob(pattern):
        try:
            data = open(f, 'rb').read()
            matches = [m.start() for m in re.finditer(rb'Invalid bone name', data)]
            for m in matches:
                chunk = data[m-20:m+60]
                print(f"{f}:", "".join(chr(b) if 32 <= b <= 126 else '.' for b in chunk))
        except:
            pass

