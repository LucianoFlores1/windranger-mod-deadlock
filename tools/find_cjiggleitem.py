import re

for dll in [r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.dll", r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\modeldoc_utils.dll"]:
    data = open(dll, "rb").read()
    pos = data.find(b'CJiggleBoneItem')
    if pos != -1:
        print(f"Found CJiggleBoneItem in {dll} at {pos}")
        chunk = data[pos-200:pos+1500]
        strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{2,}', chunk)]
        print(strings)

