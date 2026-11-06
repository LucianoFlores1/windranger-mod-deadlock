import json

def get_glb_bones(glb_path):
    with open(glb_path, 'rb') as f:
        f.read(12)
        chunk_len = int.from_bytes(f.read(4), 'little')
        f.read(4)
        json_data = json.loads(f.read(chunk_len).decode('utf-8'))
        nodes = json_data.get('nodes', [])
        skins = json_data.get('skins', [])
        joint_names = []
        if skins:
            joints = skins[0].get('joints', [])
            for j in joints:
                joint_names.append(nodes[j].get('name', f'node_{j}'))
        else:
            joint_names = [n.get('name') for n in nodes]
        return joint_names

wr_bones = get_glb_bones(r'extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb')
print(f"Windrunner joints count: {len(wr_bones)}")
print("Windrunner joints:", wr_bones[:30])

archer_bones = get_glb_bones(r'extracted\gltf\archer.glb')
print(f"\nArcher joints count: {len(archer_bones)}")
print("Archer joints:", archer_bones[:30])
