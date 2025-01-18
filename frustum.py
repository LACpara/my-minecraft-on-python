from settings import *

# 截断头的锥体
class Frustum():
    def __init__(self, camera):
        self.cam = camera
        self.factory_y = 1.0 / math.cos(half_fov := V_FOV / 2)
        self.tan_y = math.tan(half_fov)

        self.factory_x = 1.0 / math.cos(half_x := H_FOV / 2)
        self.tan_x = math.tan(half_x)
    
    def is_on_frustum(self, chunk):
        sphere_vec = chunk.center - self.cam.position
        sz = glm.dot(sphere_vec, self.cam.FORWARD)
        if not (NEAR - CHUNK_SPASE_RADIUS <= sz <= FAR + CHUNK_SPASE_RADIUS):
            return False
        
        sy = glm.dot(sphere_vec, self.cam.UP)
        dist = self.factory_y * CHUNK_SPASE_RADIUS + sz * self.tan_y
        if not (-dist <= sy <= dist):
            return False

        sx = glm.dot(sphere_vec, self.cam.RIGHT)
        dist = self.factory_x * CHUNK_SPASE_RADIUS + sz * self.tan_x
        if not (-dist <= sx <= dist):
            return False

        # dist = glm.abs(glm.distance(chunk.center, self.cam.position))
        # if dist > 3 * CHUNK_SPASE_RADIUS:
        #     return False
        
        return True