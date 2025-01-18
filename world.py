from settings import *
from world_objection.chunk import Chunk
from voxel_handler import VoxelHandler
from dinary import log_write

class World():
    def __init__(self, app):
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype=np.uint8)
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxelHandler = VoxelHandler(self)

    @log_write("world.build_chunks")
    def build_chunks(self):
        "world gnerate"
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, (x, y, z))
                    chunk_index = x + z * WORLD_W + y * WORLD_AREA
                    self.chunks[chunk_index] = chunk
                    self.voxels[chunk_index] = chunk.buid_voxels()
                    chunk.voxels = self.voxels[chunk_index]

    @log_write("world.build_chunk_mesh")
    def build_chunk_mesh(self):
        print(WORLD_VOL)
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        self.voxelHandler.update()

    def render(self):
        for chunk in self.chunks:
            chunk.render()