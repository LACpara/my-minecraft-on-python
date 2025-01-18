from settings import *
from meshes.chunk_mesh_builder import get_chunk_index
from world_objection.chunk import Chunk
import glm

class VoxelHandler():
    def __init__(self, world):
        self.app = world.app
        self.chunks = world.chunks

        # 射线检测需要返回的一些结果
        self.chunk = None           # 射线检测到的块
        self.voxel_index = None     # 射线检测到的块内索引
        self.voxel_local_pos = None # 射线检测到的块内坐标: 局部坐标
        self.voxel_world_pos = None # 射线检测到的大块坐标： 世界坐标
        self.voxel_normal = None    # 射线检测到的体素的法向量

        self.interation_mode = 0 # 放置 1 ; 删除 0
        self.new_voxel_id = GLASS

    def remove_voxel(self):
        if self.voxel_id:
            self.chunk.voxels[self.voxel_index] = 0
            self.chunk.mesh.rebuild()
            self.rebuild_adjacent_chunks()
    
    def add_voxel(self):
        if self.voxel_id:
            # 沿着法向量检查体素
            result = self.get_voxel_id(self.voxel_world_pos + self.voxel_normal)
            # print(result[2], id(result[3]))
            if not result[0]:
                voxel_id, voxel_index, voxel_local_pos, chunk = result
                if isinstance(chunk, Chunk):
                    # print(voxel_id, voxel_local_pos, id(chunk))
                    chunk.voxels[voxel_index] = self.new_voxel_id
                    chunk.mesh.rebuild()

    def rebuild_adj_chunk(self, add_voxel_pos):
        index = get_chunk_index(add_voxel_pos)
        if index != -1:
            self.chunks[index].mesh.rebuild()

    def rebuild_adjacent_chunks(self):
        lx, ly, lz = self.voxel_local_pos
        wx, wy, wz = self.voxel_world_pos

        if lx == 0:
            self.rebuild_adj_chunk((wx-1, wy, wz))
        elif lx == CHUNK_SIZE-1:
            self.rebuild_adj_chunk((wx+1, wy, wz))

        if ly == 0:
            self.rebuild_adj_chunk((wx, wy-1, wz))
        elif ly == CHUNK_SIZE-1:
            self.rebuild_adj_chunk((wx, wy-1, wz))

        if lz == 0:
            self.rebuild_adj_chunk((wx, wy, wz-1))
        elif lz== CHUNK_SIZE-1:
            self.rebuild_adj_chunk((wx, wy, wz+1))

    def set_voxel(self):
        if self.interation_mode:
            self.add_voxel()
        else:
            self.remove_voxel()

    def switch_mode(self):
        self.interation_mode = not self.interation_mode

    def update(self):
        self.ray_cast()

    def ray_cast(self):
        # 起始位置
        x1, y1, z1 = self.app.player.position
        # 终止位置
        x2, y2, z2 = self.app.player.position + self.app.player.FORWARD * MAX_RAY_DIST

        current_voxel_pos = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)
        step_dir = -1

        # 计算射线在各个轴上的步进方向 和 距离
        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 1e7) if dx != 0 else 1e7
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 1e7) if dy != 0 else 1e7
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 1e7) if dz != 0 else 1e7
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        dd = np.array([[dx, dy, dz], [delta_x, delta_y, delta_z], [max_x, max_y, max_z]])

        # 循环遍历存在于射线路径上的体素，直到超出最大检测范围
        while not np.all(dd[2, :] > 1.0):
            result = self.get_voxel_id(current_voxel_pos)
            if result[0]:
                self.voxel_id, self.voxel_index, self.voxel_local_pos, self.chunk = result
                self.voxel_world_pos = current_voxel_pos

                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True
            # 根据哪个方向上距离最小，决定如何步进
            idx = np.argmin(dd[2, :])
            current_voxel_pos[idx] += dd[0, idx]
            dd[2, idx] += dd[1, idx]
            step_dir = idx
        return False

    def get_voxel_id(self, voxel_world_pos):
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE
        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
            chunk_index = cx + cz * WORLD_D + cy * WORLD_AREA
            chunk = self.chunks[chunk_index]
            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE
            voxel_index = lx + lz * CHUNK_SIZE + ly * CHUNK_AREA
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0