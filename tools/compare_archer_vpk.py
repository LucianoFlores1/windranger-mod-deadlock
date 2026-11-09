import vpk

orig_vpk = vpk.open(r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\maps\ui\hero_prefabs\archer.vpk")
mod_vpk = vpk.open(r"custom_mod_source\maps\ui\hero_prefabs\archer.vpk")

print("Files in original archer.vpk:")
for f in sorted(orig_vpk):
    print(" ", f, f"({len(orig_vpk[f].read()):,} bytes)")
