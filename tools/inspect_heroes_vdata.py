import vpk

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
data = dl_pak['scripts/heroes.vdata_c'].read()

# Let's inspect where 'archer' appears in heroes.vdata_c
idx = 0
while True:
    idx = data.lower().find(b'archer', idx)
    if idx == -1:
        break
    start = max(0, idx - 150)
    end = min(len(data), idx + 250)
    chunk = data[start:end]
    # filter non-printable characters for readability
    clean_chunk = "".join([chr(b) if 32 <= b < 127 else "." for b in chunk])
    print(f"Match at {idx}:")
    print("  ", clean_chunk)
    idx += len(b'archer')
