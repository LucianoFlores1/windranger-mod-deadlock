import vpk
import re

pak = vpk.open(r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk")
data = pak['scripts/heroes.vdata_c'].read()

for match in re.finditer(rb'm_str[a-zA-Z0-9_]+|m_s[a-zA-Z0-9_]+Image[a-zA-Z0-9_]*', data):
    pass

# Search for the block around archer_card
pos = data.find(b'archer_card_psd')
print("Position:", pos)
if pos != -1:
    chunk = data[max(0, pos-400):min(len(data), pos+400)]
    print(repr(chunk))
    # extract strings
    for s in re.findall(rb'[\x20-\x7e]{3,}', chunk):
        print(" ", s.decode('latin1'))
