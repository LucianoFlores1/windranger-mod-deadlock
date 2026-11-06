import re

data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.dll", "rb").read()
# Find CJiggleBoneItem attribute table
pos = data.find(b'GetAttributeTable_Impl@CJiggleBoneItem')
if pos != -1:
    chunk = data[pos-1000:pos+3000]
    strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', chunk)]
    attrs = [s for s in strings if s.startswith('m_') or 'bone' in s.lower() or 'Attr' in s]
    print("CJiggleBoneItem attributes:")
    for a in attrs:
        print(" ", a)

