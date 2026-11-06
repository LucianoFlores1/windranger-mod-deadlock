import re

for dll in [r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\modeldoc_utils.dll", r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.dll"]:
    data = open(dll, "rb").read()
    pos = 0
    while True:
        pos = data.find(b'JiggleBone', pos)
        if pos == -1: break
        chunk = data[pos-200:pos+400]
        strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', chunk)]
        for s in strings:
            if any(k in s.lower() for k in ['bone', 'target', 'name', 'jiggle', 'length', 'tip', 'yaw', 'pitch', 'damping', 'stiffness']):
                print(s)
        pos += 10
        if pos > 3000000: break

