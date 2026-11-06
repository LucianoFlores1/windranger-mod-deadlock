s = open(r'extracted\mod_archer_gltf', 'r', encoding='utf-8').read()
for key in ['BodyGroupList', 'LODGroupList', 'AnimationList', 'AnimGraph2List', 'NmSkeletonList']:
    idx = s.find(key)
    print(f"=== {key} (found at {idx}) ===")
    if idx != -1:
        print(s[idx:idx+400])

