import vpk

dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')
all_vmdls = [f for f in dota_pak if ('windrunner' in f.lower() or 'windranger' in f.lower()) and f.endswith('.vmdl_c')]

print(f"Total Windranger .vmdl_c in Dota 2: {len(all_vmdls)}")
for f in all_vmdls:
    size = len(dota_pak[f].read())
    if size > 1_000_000: # larger models are usually complete models
        print(f"  {f} ({size:,} bytes)")
