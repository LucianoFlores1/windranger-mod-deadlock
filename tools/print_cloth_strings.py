data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.dll", "rb").read()
chunk = data[44858000:44861000]
import re
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.]{3,}', chunk)]
for s in strings:
    print(s)

