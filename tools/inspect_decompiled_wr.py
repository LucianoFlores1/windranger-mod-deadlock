from pathlib import Path
import re

text = Path("extracted/dota_wr_decompiled").read_text(encoding="utf-8")
print(f"Total lines: {len(text.splitlines())}")

# Find all classes
classes = re.findall(r'_class\s*=\s*"([^"]+)"', text)
print("Classes in dota_wr_decompiled:")
for c in sorted(set(classes)):
    print(" -", c)

print("\n--- Any Cloth / Phys / Jiggle in dota_wr_decompiled? ---")
for i, l in enumerate(text.splitlines()):
    if any(k in l.lower() for k in ['cloth', 'phys', 'jiggle', 'cape', 'spring']):
        print(f"L{i+1}: {l}")

