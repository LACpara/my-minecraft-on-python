from settings import *
import os

class ShaderProgram():
    def __init__(self, app):
        self.app = app
        self.ctx = self.app.ctx
        self.player = self.app.player
        self.chunk = self.get_program(shader_name="chunk")
        self.voxel_marker = self.get_program(shader_name="voxel_marker")
        
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        """设置顶点着色器的 uniform 变量"""
        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['m_view'].write(self.player.m_view)
        self.chunk['m_model'].write(glm.mat4())
        self.chunk['u_texture_array_0'] = 0

        self.voxel_marker['m_proj'].write(self.player.m_proj)
        self.voxel_marker['m_view'].write(self.player.m_view)
        self.voxel_marker['m_model'].write(glm.mat4())
        self.voxel_marker['u_texture_0'] = 0

    def update(self):
        """更新视图矩阵, 将 player 试图矩阵写入到着色器程序的 m_view"""
        self.chunk['m_view'].write(self.player.m_view)
        self.voxel_marker['m_view'].write(self.player.m_view)

    def get_program(self, shader_name):
        dir_path = "F:\\the_save_place\\vsPython3_11\\MyMc\\shaders"
        with open(os.path.join(dir_path, f"{shader_name}.vert")) as file:
            vertex_shader = file.read()
        
        with open(os.path.join(dir_path, f"{shader_name}.frag")) as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader = vertex_shader,
            fragment_shader = fragment_shader
        )

        return program