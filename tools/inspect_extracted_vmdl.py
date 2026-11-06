from pathlib import Path
import re

vmdl_path = Path("extracted/archer_windrunner.vmdl")
text = vmdl_path.read_text(encoding="utf-8")

print(f"Total lines: {len(text.splitlines())}")

# Find top-level classes or blocks
classes = re.findall(r'_class\s*=\s*"([^"]+)"', text)
print("Unique classes:", sorted(set(classes)))

# Check for Cloth, Phys, Jiggle, Morph, Skeleton, etc.
for c in sorted(set(classes)):
    if any(k in c.lower() for k in ['cloth', 'phys', 'jiggle', 'anim', 'attach', 'bone', 'mesh']):
        print(f"Relevant class: {c}")

