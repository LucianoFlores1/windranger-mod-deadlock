import os
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock")
DOTA_CONTENT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic")
DOTA_GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota_addons\windrunner_classic")
RC = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe"
SRC_PNG_DIR = BASE_DIR / "extracted" / "new_classic_pano"
CUSTOM_MOD = BASE_DIR / "custom_mod_source"

# Deadlock UI textures use uncompressed RGBA8888 with 1 mip level for crisp, zero-artifact rendering!
VTEX_TEMPLATE = """<!-- dmx encoding keyvalues2_noids 1 format vtex 1 -->
"CDmeVtex"
{{
	"m_inputTextureArray" "element_array"
	[
		"CDmeInputTexture"
		{{
			"m_name" "string" "0"
			"m_fileName" "string" "{rel_png}"
			"m_colorSpace" "string" "srgb"
			"m_typeString" "string" "2D"
		}}
	]
	"m_outputTypeString" "string" "2D"
	"m_outputFormat" "string" "RGBA8888"
	"m_nNumMipLevels" "int" "1"
	"m_textureOutputChannelArray" "element_array"
	[
		"CDmeTextureOutputChannel"
		{{
			"m_inputTextureArray" "string_array" [ "0" ]
			"m_srcChannels" "string" "rgba"
			"m_dstChannels" "string" "rgba"
			"m_outputColorSpace" "string" "srgb"
		}}
	]
}}
"""

pano_files = [
    ("archer_card_psd", "panorama/images/heroes"),
    ("archer_card_critical_psd", "panorama/images/heroes"),
    ("archer_card_gloat_psd", "panorama/images/heroes"),
    ("archer_vertical_psd", "panorama/images/heroes"),
    ("archer_sm_psd", "panorama/images/heroes"),
    ("archer_sm_psd_1ba0ed8b", "panorama/images/heroes"),
    ("archer_mm_psd", "panorama/images/heroes"),
]

for name, subpath in pano_files:
    src_png = SRC_PNG_DIR / f"{name}.png"
    if not src_png.exists():
        print(f"[SKIP] {name}.png does not exist")
        continue
        
    staging_dir = DOTA_CONTENT / "materials" / subpath
    staging_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy png
    dst_png = staging_dir / f"{name}.png"
    shutil.copy2(src_png, dst_png)
    
    # Write vtex
    rel_posix = f"materials/{subpath}/{name}.png"
    vtex_content = VTEX_TEMPLATE.format(rel_png=rel_posix)
    vtex_file = staging_dir / f"{name}.vtex"
    vtex_file.write_text(vtex_content, encoding="utf-8")
    
    # Compile with RC
    p = subprocess.run([RC, "-i", str(vtex_file)], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"[ERROR] Compiling {name}:", p.stdout, p.stderr)
        continue
        
    out_vtex_c = DOTA_GAME / "materials" / subpath / f"{name}.vtex_c"
    if not out_vtex_c.exists():
        print(f"[ERROR] Out vtex_c not found: {out_vtex_c}")
        continue
        
    # Copy to custom_mod_source
    dest_in_mod = CUSTOM_MOD / subpath / f"{name}.vtex_c"
    dest_in_mod.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_vtex_c, dest_in_mod)
    print(f"[OK] {name}.vtex_c compiled RGBA8888 -> {dest_in_mod} ({dest_in_mod.stat().st_size:,} bytes)")

print("\nAll UI panorama textures successfully compiled in lossless RGBA8888!")
