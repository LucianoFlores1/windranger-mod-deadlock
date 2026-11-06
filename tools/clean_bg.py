import re
from pathlib import Path

vmdl_path = Path(r"extracted\archer_windrunner.vmdl")
text = vmdl_path.read_text(encoding="utf-8")

# Let's clean up BodyGroupList so that only windrunner_classic is referenced in default body
# Replace meshes = [ ... ] in default body with [ "windrunner_classic" ]
# And empty out the other bodygroup meshes
def clean_bodygroups(text):
    # Find BodyGroupList
    idx = text.find('BodyGroupList')
    if idx == -1: return text
    # Clean up meshes in BodyGroupList:
    # Instead of complex parsing, replace all meshes = [ ... ] inside BodyGroupList with meshes = [ "windrunner_classic" ] for default, and meshes = [  ] for others
    # Or simpler: remove BodyGroupList entirely! Does Source 2 require BodyGroupList?
    # In Source 2, if a model has no BodyGroupList, LODGroupList defines the default mesh!
    return text

print("BodyGroupList preview:")
idx = text.find('BodyGroupList')
print(text[idx:idx+1500])
