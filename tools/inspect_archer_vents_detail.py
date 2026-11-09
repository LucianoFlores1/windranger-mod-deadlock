import vpk

orig_vpk = vpk.open(r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\maps\ui\hero_prefabs\archer.vpk")
mod_vpk = vpk.open(r"custom_mod_source\maps\ui\hero_prefabs\archer.vpk")

def find_context(data, needle):
    res = []
    pos = 0
    while True:
        idx = data.find(needle, pos)
        if idx == -1:
            break
        start = max(0, idx - 40)
        end = min(len(data), idx + 80)
        res.append(data[start:end])
        pos = idx + len(needle)
    return res

print("=== ORIG VPK ===")
data = orig_vpk['maps/ui/hero_prefabs/archer/entities/default_ents.vents_c'].read()
for c in find_context(data, b'vmdl'):
    print(" ", repr(c))

print("\n=== MOD VPK ===")
data2 = mod_vpk['maps/ui/hero_prefabs/archer/entities/default_ents.vents_c'].read()
for c in find_context(data2, b'vmdl'):
    print(" ", repr(c))
