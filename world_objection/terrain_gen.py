from noise import noise2, noise3
from random import random
from settings import *

@njit
def get_height(x, z):
    # 生成高度
    island = 1 / (pow(0.0025 * math.hypot(x - WORLD_CENTER_XZ, z - WORLD_CENTER_XZ), 20) + 0.0001)
    island = min(island, 1)
    a1 = WORLD_CENTER_Y
    f1 = 0.005
    a2, a4, a8 = a1 / 2, a1 / 4, a1 / 8
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    height = 0
    height += noise2(x*f1, z*f1) * a1 + a1
    height += noise2(x*f2, z*f2) * a2 - a2
    height += noise2(x*f4, z*f4) * a4 + a4
    height += noise2(x*f8, z*f8) * a8 - a8

    height = max(height, 2)
    height *= island
    return int(height)

@njit
def get_index(x, y, z):
    return x + CHUNK_SIZE * z + CHUNK_AREA * y

@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
    voxel_id = VOID
    if wy == 0:
        voxel_id = BEDROCK
    elif wy < world_height - 1:
        if wy < world_height - abs(random() * 5):
            voxel_id = STONE
        elif wy < SAND_LVL:
            voxel_id = SAND
        else:
            voxel_id = DIRT
    else:
        rng = int(7 * random())
        ry = wy - rng
        if SNOW_LVL <= ry:
            voxel_id = STONE
        elif STONE_LVL <= ry < SNOW_LVL:
            voxel_id = STONE
        elif DIRT_LVL <= ry < STONE_LVL:
            voxel_id = DIRT
        elif GRASS_DIRT <= ry < DIRT_LVL:
            voxel_id = GRASS
        else:
            voxel_id = SAND
        
    voxels[get_index(x, y, z)] = voxel_id
