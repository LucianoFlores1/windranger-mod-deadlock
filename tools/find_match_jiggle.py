import re

data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.dll", "rb").read()
matches = [m.start() for m in re.finditer(rb'Invalid bone name', data)]
for m in matches:
    chunk = data[m-100:m+200]
    print("Match at", m, ":", chunk)
