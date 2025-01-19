from numba import njit
import numpy as np
import glm
import math
import pygetwindow as gw

# 获取当前窗口大小
window = gw.getActiveWindow()
# width, height = window.width, window.height
width, height = 800, 600

# 游戏窗口大小
WIN_RES = glm.vec2(width * 0.98, height * 0.95)

# 窗口背景色
BG_COLOR = glm.vec3(0.1, 0.16, 0.25)

SEED = 16 # 种子

# 玩家投射参数
#   最大投射距离
MAX_RAY_DIST = 6

# 相机视觉相关参数
ASPECT_RATIO = WIN_RES.x / WIN_RES.y # 窗口宽高比
FOV_DEG = 60
V_FOV = glm.radians(FOV_DEG) 
H_FOV = 2 * math.atan(math.tan(V_FOV / 2) * ASPECT_RATIO) # 水平视角
NEAR = 0.1 # 近裁剪面 / 摄像机与最近物体的距离
FAR = 1000.0 # 远裁剪面 / 摄像机与最远物体的距离
PITCH_MAX = glm.radians(89.0) # 摄像机上下旋转的最大角度

# 立方体
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE ** 2
CHUNK_VOL = CHUNK_SIZE ** 3
CHUNK_SPASE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)

# 世界
WORLD_W, WORLD_H = 20, 3
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# 世界立方中心位置
WORLD_CENTER_XZ = WORLD_W * H_CHUNK_SIZE
WORLD_CENTER_Y = WORLD_H * H_CHUNK_SIZE

# 角色
PLAYER_SPEED = 0.01 # 角色移动速度
PLAYER_ROT_SPEED = 0.003 # 角色旋转速度
PLAYER_POS = glm.vec3(WORLD_CENTER_XZ, WORLD_H * CHUNK_SIZE, WORLD_CENTER_XZ) # 角色位置
MOUSE_SENSITIVITY = 0.002 # 鼠标灵敏度

# 文档系统
# 日志路径
DNINARY_PATH = "F:\\the_save_place\\vsPython3_11\\MyMc\\log"
DNINARY_DEFAULT_NAME = "latest.txt"

# 纹理参数
ASSETS_DIR_PATH = "F:\\the_save_place\\vsPython3_11\MyMc\\assets"
# 纹理 id （暂行方案）
VOID = 0
SAND = 1
BEDROCK = 2
DIRT = 3
GRASS = 4
OKA_LOG = 5
OKA_LEAF = -6
TNT = 7
HAY_BLOCK = 8
BRICKS = 9
STONE = 10
STRUCTURE_BLOCK_SAVE = 11
STRUCTURE_BLOCK_LOAD = 12
GLASS = -13


# 地形参数
SNOW_LVL = 55
STONE_LVL = 50
DIRT_LVL = 45
GRASS_DIRT = 10
SAND_LVL = 7