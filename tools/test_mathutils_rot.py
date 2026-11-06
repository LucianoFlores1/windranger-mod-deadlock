from mathutils import Matrix, Vector, Euler
import math

v_x = Vector((1, 0, 0)) # Bow length
v_y = Vector((0, 1, 0)) # Bow curve
v_z = Vector((0, 0, 1)) # Bow thickness

for ax in ['X', 'Y', 'Z']:
    for deg in [-90, 90, 180]:
        m = Matrix.Rotation(math.radians(deg), 3, ax)
        print(f"Rot {ax}={deg:4d}: X -> {m @ v_x}, Y -> {m @ v_y}, Z -> {m @ v_z}")

