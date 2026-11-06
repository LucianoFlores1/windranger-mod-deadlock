from pathlib import Path
import re

text = Path("extracted/archer_windrunner.vmdl").read_text(encoding="utf-8")

# Find RenderMeshList
m = re.search(r'_class\s*=\s*"RenderMeshList".*?children\s*=\s*\[(.*?)\]\s*\}', text, re.DOTALL)
if m:
    print("RenderMeshList children:")
    print(m.group(1)[:2000])
else:
    print("Not found with regex, searching line by line")
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if 'RenderMeshList' in l:
            print("\n".join(lines[i:i+40]))
            break

