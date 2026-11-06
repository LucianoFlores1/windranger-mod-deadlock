import os
import shutil
import vpk

source_mod = r'extracted_mod\pak22_dir.vpk'
dota_extracted = r'e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted'
output_folder = r'e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\custom_mod_source'

if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder, exist_ok=True)

# 1. Extraer los archivos del mod de referencia a custom_mod_source
pak = vpk.open(source_mod)
print(f"Extrayendo {len(pak)} archivos base del paquete a {output_folder}...")

for filepath in pak:
    dest_path = os.path.join(output_folder, filepath)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb') as f:
        f.write(pak[filepath].read())

print("[OK] Base de archivos lista en custom_mod_source.")
