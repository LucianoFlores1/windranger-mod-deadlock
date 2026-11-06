"""Blender <-> DMX (pulgadas de Source 2 para Archer/Grey Talon y Dota 2).
En DMX: el modelo mira hacia +Y (+X es Derecha, -X es Izquierda).
En Blender/glTF: el modelo mira hacia -Y (+X es Izquierda, -X es Derecha).
Relación física directa: rotación de 180° en Z: (-x, -y, z).
Escala: 1 metro = 39.37007874 pulgadas (1 pulgada = 0.0254 metros).
"""
import numpy as np

INCH = 0.0254

def dmx_to_blender(v):
    v = np.asarray(v, dtype=float)
    return np.stack([-v[..., 0], -v[..., 1], v[..., 2]], axis=-1) * INCH

def blender_dir_to_dmx(v):
    v = np.asarray(v, dtype=float)
    return np.stack([-v[..., 0], -v[..., 1], v[..., 2]], axis=-1)

def blender_to_dmx(v):
    return blender_dir_to_dmx(v) / INCH

def uv_blender_to_dmx(uv):
    uv = np.asarray(uv, dtype=float)
    return np.stack([uv[..., 0], 1.0 - uv[..., 1]], axis=-1)
