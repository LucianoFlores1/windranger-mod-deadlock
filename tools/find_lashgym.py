import vpk

mod_vpk = vpk.open(r"custom_mod_source\maps\ui\hero_prefabs\archer.vpk")
for f in mod_vpk:
    content = mod_vpk[f].read()
    if b'lashgym_ring' in content:
        print(f"Found 'lashgym_ring' in: {f}")
