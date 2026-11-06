import vpk

pak = vpk.open(r'extracted_mod\pak22_dir.vpk')
print(f"Total files in mod: {len(pak)}")
for p in sorted(pak):
    p_lower = p.lower()
    if any(k in p_lower for k in ['owl', 'hawk', 'bird', 'phoenix', 'fenix', 'alcon', 'falcon', 'guided', 'ability_4', 'ult']):
        print(f"  {p} ({len(pak[p].read()):,} bytes)")

