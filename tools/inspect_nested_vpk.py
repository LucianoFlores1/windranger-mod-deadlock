import vpk

pak = vpk.open(r'custom_mod_source\maps\ui\hero_prefabs\archer.vpk')
for p in sorted(pak):
    data = pak[p].read()
    print(f"{p} ({len(data):,} bytes)")

