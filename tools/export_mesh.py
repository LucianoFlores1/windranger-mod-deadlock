import numpy as np

def export_npz(mesh_obj, armature_obj, path):
    """Exporta la malla en pose de reposo y coordenadas de mundo de Blender."""
    armature_obj.data.pose_position = "REST"
    me = mesh_obj.data
    me.calc_loop_triangles()
    me.calc_tangents(uvmap=me.uv_layers.active.name)
    mw = mesh_obj.matrix_world
    m3 = mw.to_3x3()
    nmat = m3.inverted().transposed()
    uv_data = me.uv_layers.active.data
    corner_normals = me.corner_normals
    group_names = {g.index: g.name for g in mesh_obj.vertex_groups}

    vert_weights = []
    sin_peso = []
    for v_idx, v in enumerate(me.vertices):
        ws = sorted(((g.weight, group_names[g.group]) for g in v.groups if g.weight > 1e-4), reverse=True)[:4]
        if not ws:
            sin_peso.append(v_idx)
            vert_weights.append(([""] * 4, [0.0] * 4))
        else:
            total = sum(w for w, _ in ws)
            names = [n for _, n in ws] + [""] * (4 - len(ws))
            vals = [w / total for w, _ in ws] + [0.0] * (4 - len(ws))
            vert_weights.append((names, vals))

    if sin_peso:
        raise RuntimeError(f"{len(sin_peso)} vértices sin peso en {mesh_obj.name} (ej. {sin_peso[:5]})")

    key_to_idx, loop_to_idx = {}, {}
    pos, nrm, tan, uvs, wb, wv = [], [], [], [], [], []
    for li, loop in enumerate(me.loops):
        vi = loop.vertex_index
        n = (nmat @ corner_normals[li].vector).normalized()
        u = uv_data[li].uv
        key = (vi, round(u[0], 6), round(u[1], 6), round(n.x, 4), round(n.y, 4), round(n.z, 4))
        idx = key_to_idx.get(key)
        if idx is None:
            idx = key_to_idx[key] = len(pos)
            pos.append(tuple(mw @ me.vertices[vi].co))
            nrm.append(tuple(n))
            t = (m3 @ loop.tangent).normalized()
            tan.append((t.x, t.y, t.z, loop.bitangent_sign))
            uvs.append((u[0], u[1]))
            wb.append(vert_weights[vi][0])
            wv.append(vert_weights[vi][1])
        loop_to_idx[li] = idx
    tris = [[loop_to_idx[l] for l in t.loops] for t in me.loop_triangles]
    tri_mats = [t.material_index for t in me.loop_triangles]
    mat_names = [m.name for m in mesh_obj.data.materials] if mesh_obj.data.materials else ["default"]
    np.savez(path,
             positions=np.array(pos, np.float64), normals=np.array(nrm, np.float64),
             tangents=np.array(tan, np.float64), uvs=np.array(uvs, np.float64),
             tris=np.array(tris, np.int32), weight_bones=np.array(wb, dtype="<U64"),
             weight_values=np.array(wv, np.float32),
             tri_materials=np.array(tri_mats, np.int32),
             material_names=np.array(mat_names, dtype="<U128"))
    return len(pos)
