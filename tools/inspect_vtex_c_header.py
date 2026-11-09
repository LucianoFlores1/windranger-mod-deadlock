import struct

with open(r"extracted\dl_orig_pano\panorama\images\heroes\archer_card_psd.png", "rb") as f:
    pass

with open(r"custom_mod_source\panorama\images\heroes\archer_card_psd.vtex_c", "rb") as f:
    mod_data = f.read()

print("Mod archer_card_psd.vtex_c size:", len(mod_data))
# Let's inspect strings or header
import re
print("Strings in mod vtex_c:")
for s in re.findall(rb'[\x20-\x7e]{4,}', mod_data[:500]):
    print(" ", s.decode('latin1'))
