import json

def get_glb_bones(glb_path):
    with open(glb_path, 'rb') as f:
        magic = f.read(4)
        version = f.read(4)
        length = f.read(4)
        chunk_len = int.from_bytes(f.read(4), 'little')
        chunk_type = f.read(4)
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

wr_bones = get_glb_bones(r'dota2_extracted\models\heroes\windrunner\windrunner.glb')
print(f"Windrunner bones count: {len(wr_bones)}")
print("Windrunner bones (first 40):", wr_bones[:40])

archer_bones = get_glb_bones(r'extracted\archer_clean.glb')
print(f"\nArcher bones count: {len(archer_bones)}")
print("Archer bones (first 40):", archer_bones[:40])
