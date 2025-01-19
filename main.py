from settings import *
import moderngl as mgl
import pygame as pg
import sys
from shader_program import ShaderProgram
from scene import Scene
from player import PLayer
from textures import Textures
from dinary import log_init, log_write

class VoxelEngine():
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3) # 设置 Opengl 主要版本
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3) # 设置 Opengl 次要版本
        # 设置 Opengl 上下文及核心配置
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # 设置深度缓冲区大小
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        # 创建一个 Opengl 双缓冲区，尺寸位置为窗口的尺寸
        self.screen = pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)

        # 创建一个 Moderngl 上下文， 用于进行 Opengl 的渲染操作
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = "auto"
        
        self.clock = pg.time.Clock()
        self.delta_time = 0 # 记录帧间时间
        self.time = 0 # 记录游戏时间

        self.isrunning = True
        self.is_focus = False
        self.on_init()

    def on_init(self):
        # 创建实例
        log_init()

        self.textures = Textures(self)
        self.player = PLayer(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)

    def update(self):
        self.player.update()
        self.shader_program.update()
        self.scene.update()
        
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 1e-3
        pg.display.set_caption(f'当前帧率 : {self.clock.get_fps(): .0f} | '
        #    f'选中块 : {self.scene.world.voxelHandler.voxel_local_pos} | '
        #    f'{self.scene.world.voxelHandler.voxel_world_pos} | '
        #    f'id : {self.scene.world.voxelHandler.voxel_id} | '
            f'chunk : {id(self.scene.world.voxelHandler.chunk)}| '
            f'面朝方向 : {self.player.FORWARD}'
        )

        # self.test.update()

    def render(self):
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.isrunning = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.mouse.set_visible(self.is_focus)
                    self.is_focus = not self.is_focus
                    self.player.mouse_control_flg = self.is_focus
                    pg.event.set_grab(self.is_focus)
            self.player.handle_event(event)
    
    def run(self):
        while self.isrunning:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    app = VoxelEngine()
    app.run()
    # \\ \\ \\