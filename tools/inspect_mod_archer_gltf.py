from pathlib import Path

text = Path("extracted/mod_archer_gltf").read_text(encoding="utf-8")
lines = text.splitlines()
print(f"Total lines: {len(lines)}")
print("First 50 lines:")
print("\n".join(lines[:50]))

