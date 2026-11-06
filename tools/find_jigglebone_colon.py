import glob
import re

for pattern in ['E:/SteamLibrary/steamapps/common/Deadlock/game/bin/win64/*.dll', 'C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/bin/win64/*.dll']:
    for f in glob.glob(pattern):
        try:
            data = open(f, 'rb').read()
            # search for "JiggleBone:"
            if b'JiggleBone:' in data:
                print(f"Found 'JiggleBone:' in {f}")
                pos = data.find(b'JiggleBone:')
                chunk = data[pos-200:pos+300]
                print("".join(chr(b) if 32 <= b <= 126 else '.' for b in chunk))
        except:
            pass

