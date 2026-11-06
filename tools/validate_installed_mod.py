import vpk
import re
from pathlib import Path

GAME_VPK = Path(r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\addons\pak02_dir.vpk")

print(f"=== VALIDATING INSTALLED MOD: {GAME_VPK} ===")
assert GAME_VPK.exists(), "pak02_dir.vpk no existe en addons!"

pak = vpk.open(str(GAME_VPK))
print(f"Total entries in VPK: {len(pak)}")

# 1. Model verification
model_data = pak['models/heroes_staging/archer/archer.vmdl_c'].read()
print(f"archer.vmdl_c size: {len(model_data):,} bytes")
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_\.\/\\]{3,}', model_data)]

for m in ["teteva", "bow", "arrowb", "warka"]:
    assert m in strings, f"Falta mesh {m} en archer.vmdl_c!"
print("[OK] All 4 clean meshes (teteva, bow, arrowb, warka) are present.")

for f in ["orion_hair", "orion_head", "models/heroes_staging/archer/archer.vmat"]:
    assert f not in strings, f"ERROR: Encontrado '{f}' en el modelo!"
print("[OK] CERO restos de Grey Talon en el cuerpo.")

# 2. Falcon / Owl verification
owl_model = pak['models/heroes_staging/grey_talon/grey_talon_owl.vmdl_c'].read()
print(f"[OK] Falcon/Owl model present: {len(owl_model):,} bytes")
owl_tex = pak['models/heroes_staging/grey_talon/materials/windranger_ti8_immortal_shoulders_style1_color_psd_3b3faa18_upscayl_4x_high-fidelity-4x_png_d62e4d57.vtex_c'].read()
print(f"[OK] Falcon 4K plumage texture present: {len(owl_tex):,} bytes")

# 3. Voice lines verification
vo_count = 0
for p in pak:
    if p.startswith('sounds/vo/orion/'):
        vo_count += 1
print(f"[OK] Classic Windrunner voice lines present: {vo_count} files")
assert vo_count >= 158, f"Se esperaban al menos 158 archivos de voz, pero se encontraron {vo_count}"

# 4. Dynamo mod check
dynamo_vpk = GAME_VPK.parent / "pak01_dir.vpk"
assert dynamo_vpk.exists(), "pak01_dir.vpk no existe!"
print(f"[OK] pak01_dir.vpk (mod Dynamo) está intacto: {dynamo_vpk.stat().st_size:,} bytes.")

print("\n[VALIDACION 100% EXITOSA]")
