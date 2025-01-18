import pygame as pg
from camera import Camera
from settings import *

class PLayer(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        super().__init__(position, yaw, pitch)
        self.app = app
        self.mouse_control_flg = False
        self.keybord_control_flg = True

    def update(self):
        if self.mouse_control_flg:
            self.mouse_control()
        if self.keybord_control_flg:
            self.keybord_control()
        super().update()
    
    def mouse_control(self):
        """处理鼠标输入, 控制旋转角"""
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(mouse_dy * MOUSE_SENSITIVITY)
        
    def keybord_control(self):
        """处理键盘输入，控制位置移动"""
        keys = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time
        if keys[pg.K_w]:
            self.move_forward(vel)
        if keys[pg.K_s]:
            self.move_forback(vel)
        if keys[pg.K_a]:
            self.move_left(vel)
        if keys[pg.K_d]:
            self.move_right(vel)
        if keys[pg.K_q]:
            self.move_up(vel)
        if keys[pg.K_e]:
            self.move_down(vel)

    def handle_event(self, event):
        # 增加和移除体素，通过单击鼠标
        if event.type == pg.MOUSEBUTTONDOWN:
            voxelHandler = self.app.scene.world.voxelHandler
            if event.button == 1:
                voxelHandler.set_voxel()
            elif event.button == 3:
                voxelHandler.switch_mode()