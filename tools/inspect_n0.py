import vpk

mod_vpk = vpk.open(r"custom_mod_source\maps\ui\hero_prefabs\archer.vpk")
n0 = mod_vpk['maps/ui/hero_prefabs/archer/worldnodes/n0.vwnod_c'].read()
idx = n0.find(b'lashgym_ring')
print("Index in n0:", idx)
if idx != -1:
    print(repr(n0[max(0, idx-50):min(len(n0), idx+100)]))
