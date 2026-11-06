import re

data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.dll", "rb").read()
pos = data.find(b'Invalid bone name')
if pos != -1:
    chunk = data[pos-1000:pos+1000]
    strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', chunk)]
    print(strings)
else:
    # check modeldoc_utils
    data2 = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\modeldoc_utils.dll", "rb").read()
    pos2 = data2.find(b'Invalid bone name')
    if pos2 != -1:
        chunk = data2[pos2-1000:pos2+1000]
        strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', chunk)]
        print(strings)

