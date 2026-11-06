import re

data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.dll", "rb").read()
matches = [m.start() for m in re.finditer(rb'JiggleBone', data)]
for m in matches:
    chunk = data[m-100:m+250]
    text = "".join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
    if 'Invalid' in text or 'bone' in text:
        print(text)

