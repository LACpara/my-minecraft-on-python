from settings import *
from meshes.chunk_mesh import Chunk_mesh
from world_objection.terrain_gen import get_height
import glm

class Chunk():
    def __init__(self, world, position):
        self.world = world
        self.app = world.app
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None # 构建一个空的 voxels 数组
        self.mesh: Chunk_mesh = None # 块网格
        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum = self.app.player.frustum.is_on_frustum(self)

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model
    
    def set_uniform(self):
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self): # 外部调用
        self.mesh = Chunk_mesh(self) 

    def render(self):
        if self.app.player.frustum.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()
        
    def buid_voxels(self): # 外部调用
        """创建一个空的块"""
        # voxels = np.zeros(CHUNK_VOL, dtype=np.uint8)
        voxels = np.zeros(CHUNK_VOL, dtype=np.int8)

        # 填充数组
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
        self.getnerate_terrain(voxels, cx, cy, cz)
        return voxels
    
    
    @staticmethod
    @njit
    def getnerate_terrain(voxels, cx, cy, cz):
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                # for y in range(CHUNK_SIZE):
                    # voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = 1
                    # voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = \
                    # x + y + z if int(glm.simplex(glm.vec3(x, y, z) * 0.01) + 1) else 0
                wx = x + cx
                wz = z + cz
                # world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                world_height = get_height(wx, wz)
                local_height = min(world_height - cy, CHUNK_SIZE)
                y = -1
                for y in range(local_height):
                    wy = y + cy
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = DIRT
                if y < CHUNK_SIZE and y != -1:
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = GRASS