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

    def handle_border(self, rect=Rect(0, 0, 800, 600)):
        for i in range(0, self.n_spheres):
            if self.sphere[i].pos.x - self.sphere[i].radius < rect.left:
                if self.sphere.vel.x < 0:
                    self.sphere.vel.x = -self.sphere[i].vel.x
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



    def render(self, canvas):
        """Draw Player on the Game window"""
        for i in range(0, self.n_spheres):
            canvas.circle(self.sphere_color[i],
                          self.sphere[i].pos.intpair(),
                          self.sphere[i].radius)


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
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)

        self.fps = 50

        pygame.display.set_caption('Game')

        self.clock = pygame.time.Clock()

        self.canvas = Canvas(self.screen)

        self.world = World()

        rnd.seed()
        self.number_speres = 2 #default

        self.scene = GScene()


        #TODO: перегрузить вызов Scene

        for i in range(0, self.number_speres):
            self.scene.add_sphere(engine.Vector2D(rnd.randint(10, self.width - 10),
                                                  rnd.randint(10, self.height - 10)),
                                  engine.Vector2D(0, 0),
                                  engine.Vector2D(0, 100))
            self.scene.sphere_color[i] = (rnd.randint(0, 255),
                                          rnd.randint(0, 255),
                                          rnd.randint(0, 255))

        self.world.addUnit(self.scene)



    def exit(self):
        """Exit the game"""
        self._running = False

    def handle_event(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            # close window event
            self.exit()
        elif event.type == pygame.KEYDOWN:
            # keyboard event on press ESC
            if event.key == pygame.K_ESCAPE:
                self.exit()

    def cleanup(self):
        """Cleanup the Game"""
        pygame.quit()

    def flip(self):

        pygame.display.flip()
        self.clock.tick(self.fps)

    def execute(self):
        """Execution loop of the game"""
        while self._running:
            # get all pygame events from queue
            for event in pygame.event.get():
                self.handle_event(event)

            dt = self.clock.tick(self.fps) / 1000.0
            self.world.update(Frame(pygame.key.get_pressed(), dt))
            self.world.render(self.canvas)

            #print( self.clock.get_fps() )

            self.flip()

        self.cleanup()

if __name__ == "__main__":
    game = Game()
    game.execute()
