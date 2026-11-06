import subprocess
from pathlib import Path

RC = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe"
test_dir = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic\models\test")
test_dir.mkdir(parents=True, exist_ok=True)

# Test 1: Simple vmdl with JiggleBone or ClothChain
vmdl_template = '''<!-- kv3 encoding:text:version{e21c7f3c-8a33-41c5-9977-a76d3a32aa0d} format:modeldoc28:version{fb63b6ca-f435-4aa0-a2c7-c66ddc651dca} -->
{
	rootNode = 
	{
		_class = "RootNode"
		children = 
		[
			{
				_class = "JiggleBoneList"
				children = 
				[
					{
						_class = "JiggleBone"
						name = "cape_jiggle"
						m_boneName = "hair_L_0"
					}
				]
			}
		]
	}
}
'''

test_vmdl = test_dir / "test_jiggle.vmdl"
test_vmdl.write_text(vmdl_template, encoding="utf-8")

cmd = [RC, "-i", str(test_vmdl)]
res = subprocess.run(cmd, capture_output=True, text=True)
print("RC exit:", res.returncode)
print("STDOUT:", res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)
