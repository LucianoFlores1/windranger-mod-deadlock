from mathutils import Matrix, Vector
import math

m = Matrix.Rotation(math.radians(-90), 3, 'Y')
print("Rot Y = -90:")
print("  (1, 0, 0) [upper limb] ->", m @ Vector((1, 0, 0)))
print("  (0, 1, 0) [curve]      ->", m @ Vector((0, 1, 0)))
print("  (0, 0, 1) [thickness]  ->", m @ Vector((0, 0, 1)))

