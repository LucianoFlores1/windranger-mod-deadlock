import numpy as np

data = np.load(r'extracted\windrunner_classic_mesh.npz', allow_pickle=True)
bones = data['weight_bones']
weights = data['weight_values']
positions = data['positions']
tri_mats = data['tri_materials']
mat_names = data['material_names']

print("Mesh summary:")
print(f"Total vertices: {len(positions)}")
print(f"Z range: {positions[:, 2].min():.2f} to {positions[:, 2].max():.2f}")
print(f"Y range: {positions[:, 1].min():.2f} to {positions[:, 1].max():.2f}")
print(f"X range: {positions[:, 0].min():.2f} to {positions[:, 0].max():.2f}")

# Unique bones used
all_bones = set(b for row in bones for b in row if b)
print(f"Unique bones used ({len(all_bones)}):")
for b in sorted(all_bones):
    # count vertices weighted to this bone
    count = sum(1 for row in bones if b in row)
    print(f"  {b}: {count} vertices")

