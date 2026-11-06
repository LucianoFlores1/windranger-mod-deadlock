from pathlib import Path
import collections

vo_dir = Path(r"custom_mod_source\sounds\vo\orion")
files = [f.name for f in vo_dir.glob("*.vsnd_c")]

cats = collections.defaultdict(list)
for f in sorted(files):
    parts = f.replace(".vsnd_c", "").split("_")
    cat = parts[1] if len(parts) > 1 else parts[0]
    cats[cat].append(f)

print(f"Total VO files in mod: {len(files)}")
for c, flist in cats.items():
    print(f"  Category '{c:15}': {len(flist)} files (e.g. {flist[0]})")

