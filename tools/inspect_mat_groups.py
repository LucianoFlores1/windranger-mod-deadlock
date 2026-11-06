from pathlib import Path
import re

text = Path("extracted/mod_archer_gltf").read_text(encoding="utf-8")
for m in re.finditer(r'(_class\s*=\s*"[^"]*Material[^"]*")', text):
    print(m.group(0))

for l in text.splitlines()[:60]:
    print(l)

