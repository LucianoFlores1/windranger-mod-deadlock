import vpk

pak = vpk.open(r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk")
found = []
for k in pak:
    if any(k.endswith(ext) for ext in ['.vxml_c', '.vjs_c', '.vcss_c', '.vdata_c']):
        data = pak[k].read()
        if b'archer_vertical' in data or b'archer_card' in data or b'archer_sm' in data:
            found.append(k)

print("Found in:")
for f in found:
    print(" ", f)
