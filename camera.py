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
        teclas = {keys[K_w] : self.forward, keys[K_d] : self.right,\
                  keys[K_q] : self.up, keys[K_s] : -self.forward,\
                  keys[K_a] : -self.right, keys[K_e] : -self.up}

        '''teclas = {1 : (keys[K_w], keys[K_d], keys[K_q]),\
                  -1 : (keys[K_s], keys[K_a], keys[K_e])}'''

        '''teclas = {keys[K_w] or keys[K_s] : self.forward,\
                  keys[K_d] or keys[K_a] : self.right,\
                  keys[K_q] or keys[K_e] : self.up}'''

        for tecla_Pos in teclas:
            if tecla_Pos:
                if keys[K_w] and keys[K_d]:
                    velocity *= self.forward + self.right

                elif keys[K_w] and keys[K_a]:
                    velocity *= self.forward - self.right

                elif keys[K_a] and keys[K_s]:
                    velocity *= -self.forward - self.right

                elif keys[K_s] and keys[K_d]:
                    velocity *= self.right - self.forward

                else:
                    velocity *= teclas[tecla_Pos]

                self.position += velocity

    def get_view_matrix(self):
        return lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return perspective(radians(FOV), self.aspect_ratio, NEAR, FAR)




















