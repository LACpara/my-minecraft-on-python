import numpy as np
from dinary import log_write

# 基本网格类
class BaseMesh():
    def __init__(self):
        # 定义 Opengl 上下文
        self.ctx = None
        # 定义着色器程序
        self.program = None
        # 顶点缓存数据类型格式、例如 "3f 3f ", 表示两个三个的浮点数据
        self.vbo_format = None
        self.attrs: tuple[str, ...] = None
        # 顶点数组对象
        self.vao = None

    def get_vertex_data(self) -> np.ndarray: ...

    @log_write("mesh.get_vao")
    def get_vao(self):
        vertex_data = self.get_vertex_data()
        if vertex_data.size == 0:
            return None
        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors = True
        )
        return vao
    
    def render(self):
        if self.vao is not None:
            # if self.__class__.__name__ == "CubeMesh":
            #     print("1")
            self.vao.render()