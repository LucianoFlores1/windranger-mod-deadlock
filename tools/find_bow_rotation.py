from mathutils import Matrix, Vector
import math

# We want:
# (1, 0, 0) [+X, upper limb] -> (0, 0, 1) [+Z, upper limb]
# (-1, 0, 0) [-X, lower limb] -> (0, 0, -1) [-Z, lower limb]
# (0, 1, 0) [+Y, curve] -> (0, -1, 0) [-Y, curve]

# Let's test combinations of 90-degree rotations
found = []
for rx in [-180, -90, 0, 90, 180]:
    for ry in [-180, -90, 0, 90, 180]:
        for rz in [-180, -90, 0, 90, 180]:
            mx = Matrix.Rotation(math.radians(rx), 3, 'X')
            my = Matrix.Rotation(math.radians(ry), 3, 'Y')
            mz = Matrix.Rotation(math.radians(rz), 3, 'Z')
            m = mz @ my @ mx
            
            p_upper = m @ Vector((1, 0, 0))
            p_curve = m @ Vector((0, 1, 0))
            
            if (p_upper - Vector((0, 0, 1))).length < 1e-4 and (p_curve - Vector((0, -1, 0))).length < 1e-4:
                found.append((rx, ry, rz))

print("Rotations that map upper limb to +Z and curve to -Y:")
for r in found:
    print(" ", r)

