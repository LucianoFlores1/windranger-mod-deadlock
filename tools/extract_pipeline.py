import os
import subprocess

cli = r"E:\creacion-mods\enigma-dynamo\tools\vrf_cli\Source2Viewer-CLI.exe"
deadlock_vpk = r"E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk"
dota_vpk = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk"

os.makedirs("extracted/archer", exist_ok=True)
os.makedirs("extracted/windrunner", exist_ok=True)
os.makedirs("extracted/windrunner_materials", exist_ok=True)
os.makedirs("extracted/gltf", exist_ok=True)

print("1. Descompilando Grey Talon original de Deadlock (vmdl, dmx, texturas)...")
cmd = [cli, "-i", deadlock_vpk, "-f", "models/heroes_staging/archer/", "-d", "-o", "extracted/archer", "--threads", "8"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("   Salida:", res.stdout[-200:] if res.stdout else "OK")

print("2. Descompilando Windrunner clásica de Dota 2 (vmdl, dmx, texturas)...")
cmd = [cli, "-i", dota_vpk, "-f", "models/heroes/windrunner/", "-d", "-o", "extracted/windrunner", "--threads", "8"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("   Salida:", res.stdout[-200:] if res.stdout else "OK")

print("3. Descompilando Materiales y Texturas de Windrunner clásica...")
cmd = [cli, "-i", dota_vpk, "-f", "materials/models/heroes/windrunner/", "-d", "-o", "extracted/windrunner_materials", "--threads", "8"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("   Salida:", res.stdout[-200:] if res.stdout else "OK")

print("4. Exportando GLB con esqueleto y animaciones...")
cmd1 = [cli, "-i", deadlock_vpk, "-f", "models/heroes_staging/archer/archer.vmdl_c", "-d", "-o", "extracted/gltf/archer",
        "--gltf_export_format", "glb", "--gltf_export_animations", "--gltf_animation_list", "ability_charged_shot_idle"]
subprocess.run(cmd1, capture_output=True, text=True)

cmd2 = [cli, "-i", dota_vpk, "-f", "models/heroes/windrunner/windrunner.vmdl_c", "-d", "-o", "extracted/gltf/windrunner",
        "--gltf_export_format", "glb", "--gltf_export_animations", "--gltf_animation_list", "idle,attack"]
subprocess.run(cmd2, capture_output=True, text=True)

print("[COMPLETADO] Extracción de pipeline lista.")
