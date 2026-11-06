import re

s = open(r"extracted\archer_windrunner.vmdl", "r", encoding="utf-8").read()
refs = re.findall(r'"([a-zA-Z0-9_/\.\\]+\.(?:dmx|vmdl|vmat|vnmskel|vdata|vanim|vmesh))"', s)
print(f"Total references found: {len(refs)}")
for r in sorted(set(refs)):
    print(" -", r)
