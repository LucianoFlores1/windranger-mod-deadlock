import re

data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.dll", "rb").read()
# Find "Invalid bone name"
pos = data.find(b'Invalid bone name')
while pos != -1:
    chunk = data[pos-300:pos+200]
    strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', chunk)]
    print(strings)
    pos = data.find(b'Invalid bone name', pos+10)
    if pos > 40000000: break

