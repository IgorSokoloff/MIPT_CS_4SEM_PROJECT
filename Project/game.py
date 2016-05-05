import pygame
import math
import engine
import random as rnd


class Rect:
    def __init__(self, left, top, right, bottom):
        self.left, self.top, self.right, self.bottom =\
            left, top, right, bottom

class Frame:
    def __init__(self, pressed, dt):
        self.pressed = pressed
        self.dt = dt

"""
Derived class from Scene
It has function for rendering
"""
class GScene(engine.Scene):
    def __init__(self):
        super(GScene, self).__init__()
        self.sphere_color = {}
        self.vel_vector = {}
        print('Create')

    def handle_border(self, rect=Rect(0, 0, 800, 600)):
        for i in self.sphere:
            if self.sphere[i].pos.x - self.sphere[i].radius < rect.left:
                if self.sphere[i].vel.x < 0:
                    self.sphere[i].vel.x = -self.sphere[i].vel.x
                    self.sphere[i].pos.x = rect.left + self.sphere[i].radius

            if self.sphere[i].pos.y - self.sphere[i].radius < rect.top:
                if self.sphere[i].vel.y < 0:
                    self.sphere[i].vel.y = -self.sphere[i].vel.y
                    self.sphere[i].pos.y = rect.top + self.sphere[i].radius

            if self.sphere[i].pos.x + self.sphere[i].radius > rect.right:
                if self.sphere[i].vel.x > 0:
                    self.sphere[i].vel.x = -self.sphere[i].vel.x
                    self.sphere[i].pos.x = rect.right - self.sphere[i].radius;

            if self.sphere[i].pos.y + self.sphere[i].radius > rect.bottom:
                if self.sphere[i].vel.y > 0:
                    self.sphere[i].vel.y = -self.sphere[i].vel.y
                    self.sphere[i].pos.y = rect.bottom - self.sphere[i].radius

    """Update scene state"""
    def update_graphick_scene(self, frame):
        #f = Vec2()
        #f.x = frame.pressed[pygame.K_RIGHT] - frame.pressed[pygame.K_LEFT];
        #f.y = frame.pressed[pygame.K_DOWN] - frame.pressed[pygame.K_UP];
        #f *= self.a
        self.handle_border()
        self.update(frame.dt)
        self.collision_response_spheres(self.collision_detection_spheres(frame.dt), frame.dt)



    def render(self, canvas):
        """Draw Player on the Game window"""
        for i in self.sphere:
            canvas.circle(self.sphere_color[i],
                          self.sphere[i].pos.intpair(),
                          self.sphere[i].radius)

    def in_sphere(self, pos):
        for i in self.sphere:
            if abs(self.sphere[i].pos - engine.Vector2D(*pos)) <= self.sphere[i].radius:
                return i

        return False
    #def generate_scene_none_intersects(self):

     #   for i in range (0, self.n_spheres):



class Canvas:
    def __init__(self, screen):
        self.screen = screen

    def clear(self):
        self.screen.fill((0, 0, 0))

    def circle(self, color, pos, radius):
        pygame.draw.circle(self.screen, color, pos, radius)


class World:
    def __init__(self):
        self.units = []

    def update(self, frame):
        for u in self.units:
            u.update_graphick_scene(frame)

    def render(self, canvas):
        canvas.clear()
        for u in self.units:
            u.render(canvas)

    def addUnit(self, u):
        self.units.append(u)

class Game:
    #self.world.addUnit(Player(pos=(50, 50), rect=Rect(0, 0, self.width, self.height)))
    def __init__(self):
        self._running = True
        self._pause = False
        self.show_vel_vector = False
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.font = pygame.font.init()
        self.font = pygame.font.SysFont('mono', self.height//30, bold=True)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.fps = 50
        self.playtime = 0.0
        pygame.display.set_caption('Game')

        self.clock = pygame.time.Clock()

        self.canvas = Canvas(self.screen)

        self.world = World()

        rnd.seed()
        self.number_speres = 10 #default

        self.scene = GScene()

        #TODO: перегрузить вызов Scene

        for i in range(0, self.number_speres):
            self.scene.add_sphere(engine.Vector2D(rnd.randint(10, self.width - 10),
                                                  rnd.randint(10, self.height - 10)),
                                  engine.Vector2D(rnd.randint(100, 500),
                                                  rnd.randint(100, 500)),
                                  engine.Vector2D(0, 0), 1, 50)
            self.scene.sphere_color[i] = (rnd.randint(0, 255),
                                          rnd.randint(0, 255),
                                          rnd.randint(0, 255))

        """self.scene.add_sphere(engine.Vector2D(100, 200),
                              engine.Vector2D(400, 0),
                              engine.Vector2D(0, 0), 1, 50)

        self.scene.add_sphere(engine.Vector2D(700, 220),
                              engine.Vector2D(-50, 0),
                              engine.Vector2D(0, 0), 1, 50)

        self.scene.sphere_color[0] = (rnd.randint(0, 255),
                                          rnd.randint(0, 255),
                                          rnd.randint(0, 255))

        self.scene.sphere_color[1] = (rnd.randint(0, 255),
                                    rnd.randint(0, 255),
                                    rnd.randint(0, 255))"""

        self.world.addUnit(self.scene)



    def exit(self):
        """Exit the game"""
        self._running = False

    def handle_event(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            # close window event
            self.exit()
        if event.type == pygame.KEYDOWN:
            # keyboard event on press ESC
            if event.key == pygame.K_ESCAPE:
                self.exit()

            if event.key == pygame.K_SPACE:
                if self._pause is True:
                    self._pause = False
                else:
                    self._pause = True

            if event.key == pygame.K_LCTRL:
                self.show_vel_vector = True

            if event.key == pygame.K_DELETE:
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)
                if i is not False:
                    self.scene.delete_sphere(i)
                    i = False

        if event.type == pygame.MOUSEMOTION:
            """Left mouse button down + motion"""
            #print (pygame.mouse.get_pressed())
            if (pygame.mouse.get_pressed() == (1,0,0)):
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)
                if i is not False:
                    self.scene.sphere[i].set_pos(self.pos)
                    i = False



        if event.type == pygame.MOUSEBUTTONDOWN:
            """Right mouse button down - create new sphere"""

            if (pygame.mouse.get_pressed() == (1, 0, 0)):
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)
                print(i)
            if (pygame.mouse.get_pressed() == (0, 0, 1)):
                self.pos = pygame.mouse.get_pos()
                self.scene.add_sphere(engine.Vector2D(*self.pos),
                                          engine.Vector2D(rnd.randint(100, 500),
                                                          rnd.randint(100, 500)),
                                          engine.Vector2D(0, 0), 1, 50)
                self.scene.sphere_color[self.scene.n_spheres-1] = (rnd.randint(0, 255),
                                              rnd.randint(0, 255),
                                              rnd.randint(0, 255))
            """wheel mouse"""
            if (pygame.mouse.get_pressed() == (0, 0, 0)):
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)
                if i is not False:
                    if (event.button == 4):
                        self.scene.sphere[i].radius += 2
                    if (event.button == 5):
                        self.scene.sphere[i].radius -= 2
                    i = False

    def cleanup(self):
        """Cleanup the Game"""
        pygame.quit()

    def flip(self):

        pygame.display.flip()
        #self.clock.tick(self.fps)
        self.screen.blit(self.background, (0, 0))

    def draw_text(self, text, coord):
        """Center text in window.
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 255, 0))
        #self.screen.blit(surface, ((self.width - fw) // 2, (self.height - fh) // 2))

        self.screen.blit(surface, coord)

    def execute(self):
        """Execution loop of the game"""
        while self._running:
            # get all pygame events from queue
            for event in pygame.event.get():
                self.handle_event(event)

            dt = self.clock.tick(self.fps) / 1000.0
            if self._pause is False:
                self.world.update(Frame(pygame.key.get_pressed(), dt))
                self.playtime += dt
            self.world.render(self.canvas)
            #print( self.clock.get_fps() )

            self.draw_text("FPS: %6.3f  PLAYTIME: %6.3f SECONDS" %(self.clock.get_fps(), self.playtime),
                           (self.font.get_linesize(), self.height - self.font.get_linesize()*2))
            self.draw_text("IMPULSE: %6.3f  ENERGY: %6.3f " %(self.scene.impulse(), self.scene.energy()),
                           (self.font.get_linesize(), self.height - self.font.get_linesize() *1))

            self.flip()

        self.cleanup()

if __name__ == "__main__":
    game = Game()
    game.execute()
