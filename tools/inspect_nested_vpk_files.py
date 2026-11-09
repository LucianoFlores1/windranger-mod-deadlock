import vpk

mod_vpk = vpk.open(r"custom_mod_source\maps\ui\hero_prefabs\archer.vpk")
print("Files in custom_mod_source/maps/ui/hero_prefabs/archer.vpk:")
for f in sorted(mod_vpk):
    print(" ", f, f"({len(mod_vpk[f].read()):,} bytes)")
