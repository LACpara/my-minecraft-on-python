from settings import *
from meshes.guad_mesh import QuadMesh
from world_objection.chunk import Chunk
from world_objection.voxel_marker import VoxelMarker
from world import World

class Scene():
    def __init__(self, app):
        self.app = app
        self.world = World(app)
        self.voxelMarker = VoxelMarker(self.world.voxelHandler)
    
    def update(self):
        self.world.update()
        self.voxelMarker.update()

    def render(self):
        self.world.render()
        self.voxelMarker.render()