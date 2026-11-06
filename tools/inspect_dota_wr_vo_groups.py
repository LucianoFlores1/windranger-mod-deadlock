import vpk
import collections

dota_pak = vpk.open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk")
wr_lines = [p for p in dota_pak if p.lower().startswith('sounds/vo/windrunner/')]

print(f"Total Windrunner lines: {len(wr_lines)}")
groups = collections.defaultdict(list)
for p in wr_lines:
    name = p.split('/')[-1].replace('.vsnd_c', '')
    # Prefix usually describes event, e.g. wind_kill, wind_ability, wind_laugh, wind_spawn, etc.
    parts = name.split('_')
    prefix = f"{parts[0]}_{parts[1]}" if len(parts) > 1 else parts[0]
    groups[prefix].append(p)

for g in sorted(groups):
    print(f"  {g:25}: {len(groups[g])} lines (e.g. {groups[g][0].split('/')[-1]})")

