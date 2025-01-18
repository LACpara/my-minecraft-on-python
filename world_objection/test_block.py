from settings import *
from meshes.cube_mesh import CubeMesh
import glm

class TestBlock():
    def __init__(self, app, pos):
        self.app = app
        self.position = pos
        self.m_model = self.get_model_matrix()
        self.mesh = CubeMesh(self.app)

        self.mesh.program['m_model'].write(glm.translate(glm.mat4(), self.position))
        self.mesh.program['mode_id'] = 1

    def update(self):
        pass

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position))
        return m_model
    
    def render(self):
        self.mesh.render()