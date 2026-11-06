import re

data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\animationsystem.dll", "rb").read()
pos = data.find(b'CJiggleBone')
while pos != -1:
    chunk = data[pos:pos+500]
    strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', chunk)]
    print(strings[:10])
    pos = data.find(b'CJiggleBone', pos+10)
    if pos > 2000000: break

