import subprocess
from pathlib import Path
import shutil

dota_content = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic")
tex_dir = dota_content / "materials" / "models" / "heroes_staging" / "archer" / "materials"
tex_dir.mkdir(parents=True, exist_ok=True)

# Copy windrunner_color.png from extracted
src_png = Path(r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_color_psd_cb3528ab.png")
dst_png = tex_dir / "windrunner_color.png"
shutil.copy2(src_png, dst_png)

VTEX_TEMPLATE = """<!-- dmx encoding keyvalues2_noids 1 format vtex 1 -->
"CDmeVtex"
{
	"m_inputTextureArray" "element_array"
	[
		"CDmeInputTexture"
		{
			"m_name" "string" "0"
			"m_fileName" "string" "materials/models/heroes_staging/archer/materials/windrunner_color.png"
			"m_colorSpace" "string" "srgb"
			"m_typeString" "string" "2D"
		}
	]
	"m_outputTypeString" "string" "2D"
	"m_outputFormat" "string" "DXT5"
	"m_textureOutputChannelArray" "element_array"
	[
		"CDmeTextureOutputChannel"
		{
			"m_inputTextureArray" "string_array" [ "0" ]
			"m_srcChannels" "string" "rgba"
			"m_dstChannels" "string" "rgba"
			"m_mipAlgorithm" "CDmeImageProcessor"
			{
				"m_algorithm" "string" "Box"
				"m_stringArg" "string" ""
				"m_vFloat4Arg" "vector4" "0 0 0 0"
			}
			"m_outputColorSpace" "string" "srgb"
		}
	]
}
"""

vtex_path = tex_dir / "windrunner_color.vtex"
vtex_path.write_text(VTEX_TEMPLATE, encoding="utf-8")

cmd = [
    r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe",
    "-i", str(vtex_path)
]
p = subprocess.run(cmd, capture_output=True, text=True)
print("RC exit:", p.returncode)
print(p.stdout)
if p.stderr:
    print("STDERR:", p.stderr)
