import os
import vpk
import shutil

source_dir = r'e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\custom_mod_source'
build_dir = r'e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\build'
output_vpk = os.path.join(build_dir, 'pak02_dir.vpk')
game_addons_dir = r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\addons'
game_vpk = os.path.join(game_addons_dir, 'pak02_dir.vpk')

os.makedirs(build_dir, exist_ok=True)
os.makedirs(game_addons_dir, exist_ok=True)

print(f"Empaquetando nuevo VPK desde: {source_dir}...")
new_pak = vpk.new(source_dir)
print(f"Total de archivos indexados: {new_pak.file_count}")

print(f"Guardando VPK en: {output_vpk}...")
new_pak.save(output_vpk)
print(f"[OK] VPK generado con éxito ({os.path.getsize(output_vpk):,} bytes).")

print(f"Copiando a addons de Deadlock: {game_vpk}...")
shutil.copy2(output_vpk, game_vpk)
print(f"[ÉXITO] Mod instalado en Deadlock ({os.path.getsize(game_vpk):,} bytes).")
