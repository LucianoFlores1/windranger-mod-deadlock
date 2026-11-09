import subprocess

code = """
import bpy
import numpy as np

# Load the objects and check right arm vertices in body_main
import sys
sys.path.append(r"E:\\Antigravity-consultas-y-pruebas\\windranger-mod-deadlock\\tools")
from build_restored_perfect_windrunner import build_body_main, clean_scene, import_reference_warka

clean_scene()
ref_warka = import_reference_warka()
body_main = build_body_main(ref_warka)

print("=== CHECKING RIGHT ARM (X < -0.20) ===")
bad_spines = []
for v in body_main.data.vertices:
    if v.co.x < -0.20 and 0.8 < v.co.z < 1.4:
        for g in v.groups:
            g_name = body_main.vertex_groups[g.group].name
            if 'spine' in g_name or 'clavicle' in g_name or 'neck' in g_name or 'head' in g_name:
                if g.weight > 0.01:
                    bad_spines.append((v.index, v.co.x, v.co.y, v.co.z, g_name, g.weight))

print(f"Total bad weights on right arm: {len(bad_spines)}")
for item in bad_spines[:25]:
    print(f"  Vert {item[0]} at ({item[1]:.2f}, {item[2]:.2f}, {item[3]:.2f}): {item[4]} = {item[5]:.3f}")
"""

with open(r"extracted\check_r_arm.py", "w", encoding="utf-8") as f:
    f.write(code)

cmd = [r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe", "-b", "-P", r"extracted\check_r_arm.py"]
p = subprocess.run(cmd, capture_output=True, text=True)
print(p.stdout)
if p.stderr:
    print("STDERR:", p.stderr)
