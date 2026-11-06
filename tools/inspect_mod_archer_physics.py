from pathlib import Path
import re

text = Path("extracted/mod_archer_gltf").read_text(encoding="utf-8")

classes = re.findall(r'_class\s*=\s*"([^"]+)"', text)
print("All classes in mod_archer_gltf:")
for c in sorted(set(classes)):
    print(" -", c)

print("\n--- Any Physics or Jiggle or Cloth blocks? ---")
lines = text.splitlines()
for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['phys', 'jiggle', 'cloth', 'joint', 'spring', 'dynamic']):
        print(f"Line {i+1}: {l}")

