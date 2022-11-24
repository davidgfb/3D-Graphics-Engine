from glm import vec3, lookAt, perspective, radians, cos, sin, cross, normalize
from pygame import K_w, K_s, K_a, K_d, K_q, K_e
from pygame.key import get_pressed
from pygame.mouse import get_rel
from numpy import array

FOV, NEAR, FAR, SPEED, SENSITIVITY = array((1e4, 20, 2e4, 1, 8)) / 200 #50, 1 / 10, 100, 1 / 200, 1 / 25  # deg

class Camera:
    def __init__(self, app, position = 4 * array((0, 0, 1)), yaw = -90, pitch = 0):
        self.app, (ancho, alto) = app, app.WIN_SIZE
        self.aspect_ratio, self.position, self.up, self.right, self.forward,\
                           self.yaw, self.pitch = ancho / alto, vec3(position),\
                           vec3(0, 1, 0), vec3(1, 0, 0), vec3(0, 0, -1), yaw, pitch
        # view matrix
        self.m_view, self.m_proj = self.get_view_matrix(),\
                                   self.get_projection_matrix() # projection matrix
         
    def rotate(self):
        rel_x, rel_y = get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = radians(self.yaw), radians(self.pitch)
        self.forward.x, self.forward.y, self.forward.z = cos(yaw) * cos(pitch),\
                                                         sin(pitch),\
                                                         sin(yaw) * cos(pitch)
        self.forward, self.right, self.up = normalize(self.forward),\
                                    normalize(cross(self.forward, vec3(0, 1, 0))),\
                                    normalize(cross(self.right, self.forward))

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = get_pressed()

        if keys[K_w]:
            self.position += self.forward * velocity

        if keys[K_d]:
            self.position += self.right * velocity
            
        if keys[K_q]:
            self.position += self.up * velocity
            
        if keys[K_s]:
            self.position -= self.forward * velocity
            
        if keys[K_a]:
            self.position -= self.right * velocity
                     
        if keys[K_e]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        return lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return perspective(radians(FOV), self.aspect_ratio, NEAR, FAR)




















