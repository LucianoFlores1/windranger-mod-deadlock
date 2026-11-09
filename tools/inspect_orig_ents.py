import vpk
import re

orig_vpk = vpk.open(r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\maps\ui\hero_prefabs\archer.vpk")
ents = orig_vpk['maps/ui/hero_prefabs/archer/entities/default_ents.vents_c'].read()

# Let's inspect all readable chunks of 5+ chars
words = re.findall(rb'[\x20-\x7e]{4,}', ents)
print("Total words in orig vents_c:", len(words))
for w in words:
    s = w.decode('latin1')
    if any(k in s.lower() for k in ['hero', 'model', 'archer', 'camera', 'light', 'picker', 'target', 'entity', 'class']):
        print(" ", s)
