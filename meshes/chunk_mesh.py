from meshes.base_mesh import BaseMesh
from meshes.chunk_mesh_builder import build_chunk_mesh
from dinary import log_write

class Chunk_mesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()
        self.chunk = chunk
        self.app = chunk.app
        self.ctx = self.app.ctx

        # 获取着色器程序对象
        self.program = self.app.shader_program.chunk
        
        # 顶点数据格式
        # self.vbo_format = "3u1 1u1 1u1 1u1 1u1"
        self.vbo_format = "1u4" # 打包后数据
        
        # 顶点数据格式大小，当前版本采用单位为 np.uint8
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())

        # 顶点属性名称
        # self.attrs = ('in_position', 'voxel_id', 'face_id', 'ao_id', 'flip_id')
        self.attrs = ('packed_data',) # 打包后数据
        self.vao = self.get_vao()

    def rebuild(self):
        self.vao= self.get_vao()

    # @log_write("mesh.get_vertex_data")
    def get_vertex_data(self):
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_pos=self.chunk.position,
            word_voxels=self.chunk.world.voxels
        )
        # print(mesh)
        return mesh