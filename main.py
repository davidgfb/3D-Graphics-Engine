import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer
from pygame import init, GL_CONTEXT_MAJOR_VERSION, GL_CONTEXT_MINOR_VERSION,\
     GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE, OPENGL, DOUBLEBUF, QUIT,\
     KEYDOWN, K_ESCAPE, quit
from pygame.display import gl_set_attribute, set_mode, flip
from pygame.event import set_grab, get
from pygame.mouse import set_visible
from pygame.time import Clock, get_ticks
from numpy import array

class GraphicsEngine:
    def __init__(self, win_size = (1600, 900)):
        # init pygame modules
        init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr

        (*(gl_set_attribute(a, b) for a, b in ((GL_CONTEXT_MAJOR_VERSION, 3),\
                                      (GL_CONTEXT_MINOR_VERSION, 3),\
                                      (GL_CONTEXT_PROFILE_MASK,\
                                       GL_CONTEXT_PROFILE_CORE))),)
        
        '''gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, 3)
        gl_set_attribute(GL_CONTEXT_MINOR_VERSION, 3)
        gl_set_attribute(GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE)'''
        # create opengl context
        set_mode(self.WIN_SIZE, flags = OPENGL | DOUBLEBUF)
        # mouse settings
        set_grab(True)
        set_visible(False)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw'
        self.ctx.enable(flags = mgl.DEPTH_TEST | mgl.CULL_FACE)
        # create an object to help track time
        self.clock = Clock()
        self.time = 0
        self.delta_time = 0
        # light
        self.light = Light()
        # camera
        self.camera = Camera(self)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)
        # renderer
        self.scene_renderer = SceneRenderer(self)

    def check_events(self):
        for event in get():
            if event.type == QUIT or event.type == KEYDOWN and\
                                      event.key == K_ESCAPE:
                self.mesh.destroy()
                self.scene_renderer.destroy()
                quit()
                sys.exit()

    def render(self):
        # clear framebuffer
        self.ctx.clear(color = array((4, 8, 9)) / 50)
        # render scene
        self.scene_renderer.render()
        # swap buffers
        flip()

    def get_time(self):
        self.time = get_ticks() / 1000

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()






























