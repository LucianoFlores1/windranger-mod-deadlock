import os
import shutil
from pathlib import Path
import vpk

BASE_DIR = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock")
CUSTOM_MOD = BASE_DIR / "custom_mod_source"
BUILD_VPK = BASE_DIR / "build" / "pak02_dir.vpk"
DEADLOCK_ADDONS = Path(r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\addons")
GAME_VPK = DEADLOCK_ADDONS / "pak02_dir.vpk"

DOTA_COMPILED = Path(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota_addons\windrunner_classic\models\heroes_staging\archer\archer.vmdl_c")

print("=== PASO 0: Actualizando archer.vmdl_c en custom_mod_source ===")
if DOTA_COMPILED.exists():
    target_vmdl = CUSTOM_MOD / "models" / "heroes_staging" / "archer" / "archer.vmdl_c"
    shutil.copy2(DOTA_COMPILED, target_vmdl)
    print(f"[OK] archer.vmdl_c actualizado: {target_vmdl} ({target_vmdl.stat().st_size:,} bytes)")
else:
    print(f"[ERROR] No se encontró el modelo compilado en {DOTA_COMPILED}")
    exit(1)

print("\n=== PASO 1: Creando pak02_dir.vpk desde custom_mod_source ===")
BUILD_VPK.parent.mkdir(parents=True, exist_ok=True)
pak = vpk.new(str(CUSTOM_MOD))
pak.save(str(BUILD_VPK))
print(f"[OK] pak02_dir.vpk guardado en {BUILD_VPK} ({BUILD_VPK.stat().st_size:,} bytes)")

print("\n=== PASO 2: Verificando contenido del paquete ===")
pak_check = vpk.open(str(BUILD_VPK))
count = 0
found_model = False
found_ui_vpk = False
for p in sorted(pak_check):
    count += 1
    if p == "models/heroes_staging/archer/archer.vmdl_c":
        found_model = True
        print(f" -> Modelo: {p} ({len(pak_check[p].read()):,} bytes)")
    elif p == "maps/ui/hero_prefabs/archer.vpk":
        found_ui_vpk = True
        print(f" -> UI Prefab VPK: {p} ({len(pak_check[p].read()):,} bytes)")

print(f"Total de archivos en VPK: {count}")
assert found_model, "ERROR: archer.vmdl_c no encontrado en el paquete!"
assert found_ui_vpk, "ERROR: archer.vpk no encontrado en el paquete!"

print("\n=== PASO 3: Copiando a directorio de addons de Deadlock ===")
DEADLOCK_ADDONS.mkdir(parents=True, exist_ok=True)
shutil.copy2(BUILD_VPK, GAME_VPK)
print(f"[OK] Mod copiado exitosamente a: {GAME_VPK} ({GAME_VPK.stat().st_size:,} bytes)")

print("\n=== PASO 4: Verificando otros mods en addons ===")
for item in DEADLOCK_ADDONS.iterdir():
    print(f" -> Addon: {item.name} ({item.stat().st_size:,} bytes)")

print("\n[COMPLETADO EXITOSAMENTE]")

