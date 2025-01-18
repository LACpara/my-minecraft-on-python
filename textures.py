import pygame as pg
import moderngl as mgl
from settings import *
import os

class Textures():
    def __init__(self, app):
        self.app = app
        self.ctx = self.app.ctx
        # 加载纹理
        self.texture_0 = self.load("frame")
        self.texture_0.use(location=0) # 设置纹理位置

        self.texture_array_0 = self.load("texSets01_3", is_tex_array=True)
        self.texture_array_0.use(location=0)

    def load(self, fileName, is_tex_array=False):
        texture = pg.image.load(os.path.join(ASSETS_DIR_PATH, f"textures\\{fileName}.png"))

        texture = pg.transform.flip(texture, flip_x=True, flip_y=False) # 翻转纹理
        
        if is_tex_array:
            nums_pr_layer = int(fileName.split('_')[-1])
            num_layers = nums_pr_layer * texture.get_height() // texture.get_width() # 计算纹理层数
            texture = self.app.ctx.texture_array(
                size = (texture.get_width(), texture.get_height() // num_layers, num_layers),
                components = 4,
                data = pg.image.tostring(texture, 'RGBA')
            )
        else:
            texture = self.ctx.texture(
                size = texture.get_size(),  # 纹理大小
                components = 4,             # 颜色通道数
                data = pg.image.tostring(texture, "RGBA", False) # 纹理数据
            )

        texture.anisolatropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture
