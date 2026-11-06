import vpk
import os

dota_vpk_path = r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk'
output_dir = r'e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted'

print(f"Abriendo VPK de Dota 2: {dota_vpk_path}")
dota_pak = vpk.open(dota_vpk_path)

# Filtrar todos los archivos relevantes de Windranger Arcana y armas/modelos base
targets = [
    f for f in dota_pak 
    if ('windrunner_arcana' in f.lower() or 'wr_arcana' in f.lower() or 'heroes/windrunner' in f.lower())
    and not f.endswith('.vanim_c') and not f.endswith('.vnmclip_c')
]

print(f"Archivos encontrados en Dota 2: {len(targets)}")

extracted_count = 0
for rel_path in targets:
    dest_path = os.path.join(output_dir, rel_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb') as f:
        f.write(dota_pak[rel_path].read())
    extracted_count += 1
    if extracted_count % 50 == 0:
        print(f"  Extraídos {extracted_count}/{len(targets)} archivos...")

print(f"\n[ÉXITO] Extracción completada: {extracted_count} archivos extraídos directamente de tu Dota 2.")
