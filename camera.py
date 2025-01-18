import glm
from settings import *
from frustum import Frustum

class Camera():
    def __init__(self, position, yaw, pitch):
        self.position = glm.vec3(position) # 相机位置
        self.yaw = glm.radians(yaw) # 相机偏航角，转换为弧度制
        self.pitch = glm.radians(pitch) # 相机俯仰角, 同上

        self.UP = glm.vec3(0, 1, 0) # 相机的 UP 向量
        self.RIGHT = glm.vec3(1, 0, 0) # 相机的 RIGHT 向量
        self.FORWARD = glm.vec3(0, 0, -1) # 相机的 FORWARD 向量

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR) # 生成透视投影矩阵
        self.m_view = glm.mat4()
        self.frustum = Frustum(self)

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.FORWARD, self.UP)

    # 相机方向向量的计算
    def update_vectors(self):
        self.FORWARD.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.FORWARD.y = glm.sin(self.pitch)
        self.FORWARD.z = glm.sin(self.yaw) * glm.cos(self.pitch)
        self.FORWARD = glm.normalize(self.FORWARD)

        self.RIGHT = glm.normalize(glm.cross(self.FORWARD, glm.vec3(0, 1, 0)))
        self.UP = glm.normalize(glm.cross(self.RIGHT, self.FORWARD))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def move_left(self, velocity):
        self.position -= self.RIGHT * velocity

    def move_right(self, velocity):
        self.position += self.RIGHT * velocity
        
    def move_up(self, velocity):
        self.position += self.UP * velocity

    def move_down(self, velocity):
        self.position -= self.UP * velocity

    def move_forward(self, velocity):
        self.position += self.FORWARD * velocity

    def move_forback(self, velocity):
        self.position -= self.FORWARD * velocity
