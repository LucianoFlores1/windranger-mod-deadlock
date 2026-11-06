import re

data = open(r'dota2_extracted/models/heroes/windrunner/windrunner.vmdl_c', 'rb').read()
pos = data.find(b'BaseJigglebon')
if pos != -1:
    print("Found BaseJigglebon at:", pos)
    print("Context around pos (300 bytes):")
    chunk = data[max(0, pos-100):pos+300]
    # replace non-ascii with dot
    print("".join(chr(b) if 32 <= b <= 126 else '.' for b in chunk))
else:
    print("Not found")

