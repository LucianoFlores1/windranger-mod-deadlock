import json

def get_nodes(glb_path):
    with open(glb_path, 'rb') as f:
        f.read(12)
        chunk_len = int.from_bytes(f.read(4), 'little')
        f.read(4)
        json_data = json.loads(f.read(chunk_len).decode('utf-8'))
        return [n.get('name') for n in json_data.get('nodes', [])]

print("Windrunner GLB nodes (sample 30):")
print(get_nodes(r'dota2_extracted\models\heroes\windrunner\windrunner.glb')[:30])

print("\nArcher GLB nodes (sample 30):")
print(get_nodes(r'extracted\archer_clean.glb')[:30])
