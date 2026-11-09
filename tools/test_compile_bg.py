import subprocess
from pathlib import Path

DOTA_CONTENT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic")
RC = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe"

test_dir = DOTA_CONTENT / "materials" / "panorama" / "images" / "heroes" / "backgrounds"
test_dir.mkdir(parents=True, exist_ok=True)

vtex = """<!-- dmx encoding keyvalues2_noids 1 format vtex 1 -->
"CDmeVtex"
{
	"m_inputTextureArray" "element_array"
	[
		"CDmeInputTexture"
		{
			"m_name" "string" "0"
			"m_fileName" "string" "materials/panorama/images/heroes/backgrounds/grey_talon_bg_psd.png"
			"m_colorSpace" "string" "srgb"
			"m_typeString" "string" "2D"
		}
	]
	"m_outputTypeString" "string" "2D"
	"m_outputFormat" "string" "DXT5"
	"m_nNumMipLevels" "int" "1"
	"m_textureOutputChannelArray" "element_array"
	[
		"CDmeTextureOutputChannel"
		{
			"m_inputTextureArray" "string_array" [ "0" ]
			"m_srcChannels" "string" "rgba"
			"m_dstChannels" "string" "rgba"
			"m_outputColorSpace" "string" "srgb"
		}
	]
}
"""
f = test_dir / "grey_talon_bg_psd.vtex"
f.write_text(vtex, encoding="utf-8")
p = subprocess.run([RC, "-i", str(f)], capture_output=True, text=True)
print(f"BG exit code: {p.returncode}")
if p.returncode != 0:
    print(p.stdout)
    print(p.stderr)
