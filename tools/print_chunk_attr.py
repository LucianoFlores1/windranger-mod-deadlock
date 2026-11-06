data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.dll", "rb").read()
pos = data.find(b"Invalid bone name '%s'")
chunk = data[pos-1000:pos+1000]
print("".join(chr(b) if 32 <= b <= 126 else '.' for b in chunk))

