import os
import shutil
import subprocess
from pathlib import Path
import vpk

BASE_DIR = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock")
DOTA_CONTENT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic")
DOTA_GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota_addons\windrunner_classic")
RC = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\bin\win64\resourcecompiler.exe"
CUSTOM_MOD = BASE_DIR / "custom_mod_source"
BUILD_VPK = BASE_DIR / "build" / "pak02_dir.vpk"
DEADLOCK_ADDONS = Path(r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\addons")

VTEX_TEMPLATE = """<!-- dmx encoding keyvalues2_noids 1 format vtex 1 -->
"CDmeVtex"
{{
	"m_inputTextureArray" "element_array"
	[
		"CDmeInputTexture"
		{{
			"m_name" "string" "0"
			"m_fileName" "string" "{rel_png}"
			"m_colorSpace" "string" "{space}"
			"m_typeString" "string" "2D"
		}}
	]
	"m_outputTypeString" "string" "2D"
	"m_outputFormat" "string" "{fmt}"
	"m_textureOutputChannelArray" "element_array"
	[
		"CDmeTextureOutputChannel"
		{{
			"m_inputTextureArray" "string_array" [ "0" ]
			"m_srcChannels" "string" "rgba"
			"m_dstChannels" "string" "rgba"
			"m_mipAlgorithm" "CDmeImageProcessor"
			{{
				"m_algorithm" "string" "Box"
				"m_stringArg" "string" ""
				"m_vFloat4Arg" "vector4" "0 0 0 0"
			}}
			"m_outputColorSpace" "string" "{space}"
		}}
	]
}}
"""

# Texture definitions: (name, source_png, fmt, space, targets_in_custom_mod)
TEXTURES = [
    # 1. Base color (Classic Green Outfit & Body)
    (
        "windrunner_color",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_color_psd_cb3528ab.png",
        "DXT5",
        "srgb",
        [r"models\heroes_staging\archer\materials\windranger_arcana_base_color_psd_46fd4962_png_8291da6e.vtex_c"]
    ),
    # 2. Base normal
    (
        "windrunner_normal",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_normal_psd_38977de9.png",
        "DXT5",
        "linear",
        [r"models\heroes_staging\archer\materials\normal_3_test_png_e0a6d093.vtex_c"]
    ),
    # 3. Hair color (Classic Orange Hair)
    (
        "windrunner_hair_color",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_hair_color_psd_c0ea3acd.png",
        "DXT5",
        "srgb",
        [r"models\heroes_staging\archer\materials\windranger_arcana_hair_color_psd_b2989f4_png_3ce3d8ad.vtex_c"]
    ),
    # 4. Cape color (Classic Green Cloak)
    (
        "windrunner_cape_color",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_cape_color_psd_ee80fad1.png",
        "DXT5",
        "srgb",
        [r"models\heroes_staging\archer\materials\windranger_arcana_head_color_psd_f637e891_png_e225de03.vtex_c"]
    ),
    # 5. Cape normal
    (
        "windrunner_cape_normal",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_cape_normal_psd_dac85abd.png",
        "DXT5",
        "linear",
        [r"models\heroes_staging\archer\materials\windranger_arcana_head_normal_psd_234e7d68_png_59a39bb2.vtex_c"]
    ),
    # 6. Shoulderpads color (Classic Shoulders)
    (
        "windrunner_shoulders_color",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_shoulderpads_color_psd_e4854e6a.png",
        "DXT5",
        "srgb",
        [
            r"models\heroes_staging\grey_talon\materials\windranger_ti8_immortal_shoulders_style1_color_psd_3b3faa18_upscayl_4x_high-fidelity-4x_png_3dbdd27f.vtex_c",
            r"models\heroes_staging\grey_talon\materials\windranger_ti8_immortal_shoulders_style1_color_psd_3b3faa18_upscayl_4x_high-fidelity-4x_png_d62e4d57.vtex_c"
        ]
    ),
    # 7. Shoulderpads normal
    (
        "windrunner_shoulders_normal",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_shoulderpads_normal_psd_111971b6.png",
        "DXT5",
        "linear",
        [r"models\heroes_staging\grey_talon\materials\windrunner_shoulderpads_normal_psd_72d84f0a_png_ebb635f9.vtex_c"]
    ),
    # 8. Quiver color (Classic Quiver)
    (
        "windrunner_quiver_color",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_quiver_color_psd_929ce458.png",
        "DXT5",
        "srgb",
        [r"models\heroes_staging\archer\materials\windranger_arcana_arrow_color_psd_ad40efda_png_7fc07158.vtex_c"]
    ),
    # 9. Quiver normal
    (
        "windrunner_quiver_normal",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_quiver_normal_psd_448fbfc1.png",
        "DXT5",
        "linear",
        [r"models\heroes_staging\archer\materials\windranger_arcana_arrow_normal_psd_67ebacc2_png_eb48dea.vtex_c"]
    ),
    # 10. Bow color (Classic Wooden Bow)
    (
        "windrunner_bow_color",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_bow_color_psd_252ad508.png",
        "DXT5",
        "srgb",
        [r"models\heroes_staging\archer\materials\windranger_arcana_bow_color_psd_1684a33b_png_f75e3560.vtex_c"]
    ),
    # 11. Bow normal
    (
        "windrunner_bow_normal",
        r"extracted\windrunner_materials\materials\models\heroes\windrunner\windrunner_bow_normal_psd_5a3f1eae.png",
        "DXT5",
        "linear",
        [r"models\heroes_staging\archer\materials\windranger_arcana_bow_normal_psd_7083fef5_png_34f70c96.vtex_c"]
    ),
]

def main():
    print("=== PASO 1: Compilando Texturas Clásicas de Windranger ===")
    staging_tex_dir = DOTA_CONTENT / "materials" / "classic_textures"
    staging_tex_dir.mkdir(parents=True, exist_ok=True)

    for name, src_rel, fmt, space, targets in TEXTURES:
        src_png = BASE_DIR / src_rel
        dst_png = staging_tex_dir / f"{name}.png"
        shutil.copy2(src_png, dst_png)
        
        rel_posix = f"materials/classic_textures/{name}.png"
        vtex_content = VTEX_TEMPLATE.format(rel_png=rel_posix, space=space, fmt=fmt)
        vtex_file = staging_tex_dir / f"{name}.vtex"
        vtex_file.write_text(vtex_content, encoding="utf-8")
        
        # Compile vtex
        p = subprocess.run([RC, "-i", str(vtex_file)], capture_output=True, text=True)
        if p.returncode != 0:
            print(f"[ERROR] Falló compilación de {name}:", p.stdout)
            return
        
        out_vtex_c = DOTA_GAME / "materials" / "classic_textures" / f"{name}.vtex_c"
        if not out_vtex_c.exists():
            print(f"[ERROR] No se encontró salida compilada {out_vtex_c}")
            return
        
        # Copy to each target in custom_mod_source
        for tgt in targets:
            dest = CUSTOM_MOD / tgt
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(out_vtex_c, dest)
            print(f" [OK] Textura {name} -> {tgt} ({os.path.getsize(dest):,} bytes)")

    print("\n=== PASO 2: Instalando Modelo Clásico Compilado ===")
    compiled_model = DOTA_GAME / "models" / "heroes_staging" / "archer" / "archer.vmdl_c"
    if not compiled_model.exists():
        print(f"[ERROR] No se encontró el modelo compilado {compiled_model}")
        return
    
    target_model = CUSTOM_MOD / "models" / "heroes_staging" / "archer" / "archer.vmdl_c"
    shutil.copy2(compiled_model, target_model)
    print(f" [OK] archer.vmdl_c instalado ({os.path.getsize(target_model):,} bytes)")

    print("\n=== PASO 3: Empaquetando VPK ===")
    BUILD_VPK.parent.mkdir(parents=True, exist_ok=True)
    pak = vpk.new(str(CUSTOM_MOD))
    pak.save(str(BUILD_VPK))
    print(f" [OK] pak02_dir.vpk generado: {BUILD_VPK} ({os.path.getsize(BUILD_VPK):,} bytes)")

    print("\n=== PASO 4: Instalando en Deadlock ===")
    DEADLOCK_ADDONS.mkdir(parents=True, exist_ok=True)
    game_vpk = DEADLOCK_ADDONS / "pak02_dir.vpk"
    shutil.copy2(BUILD_VPK, game_vpk)
    print(f" [OK] pak02_dir.vpk copiado exitosamente a: {game_vpk} ({os.path.getsize(game_vpk):,} bytes)")

    print("\n=== PASO 5: Verificando Integridad del Mod ===")
    installed = vpk.open(str(game_vpk))
    count = 0
    archer_found = False
    for path in installed:
        count += 1
        if "archer.vmdl_c" in path:
            archer_found = True
            entry = installed[path]
            print(f" -> Modelo verificado en VPK: {path} ({len(entry.read()):,} bytes)")
    print(f" -> Total de archivos en VPK: {count}")
    assert archer_found, "El modelo archer.vmdl_c no se encontró en el VPK"
    print("\n[EXITO TOTAL] El mod clásico de Windranger ha sido compilado e instalado correctamente.")

if __name__ == "__main__":
    main()
