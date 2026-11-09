import vpk

orig_vpk = vpk.open(r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\maps\ui\hero_prefabs\archer.vpk")
print("Does orig archer.vpk have lashgym_ring?")
for f in orig_vpk:
    content = orig_vpk[f].read()
    if b'lashgym_ring' in content:
        print(f"Found 'lashgym_ring' in: {f}")
print("Done check.")
