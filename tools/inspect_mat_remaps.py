from pathlib import Path

text = Path("extracted/mod_archer_gltf").read_text(encoding="utf-8")
lines = text.splitlines()

for i, l in enumerate(lines):
    if 'material' in l.lower() or 'remap' in l.lower():
        print(f"Line {i+1}: {l}")

