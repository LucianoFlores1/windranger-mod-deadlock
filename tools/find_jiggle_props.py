import re

data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\modeldoc_utils.dll", "rb").read()
pos = data.find(b'JiggleBone')
while pos != -1:
    chunk = data[pos:pos+1000]
    strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', chunk)]
    print(strings[:15])
    pos = data.find(b'JiggleBone', pos + 10)
    if pos > 1000000: break

