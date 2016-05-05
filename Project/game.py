import pygame
import math
import engine
import random as rnd


class Rect:
    def __init__(self, left, top, right, bottom):
        self.left, self.top, self.right, self.bottom =\
            left, top, right, bottom

        self.momentum = engine.Vector2D(0,0)

    def get_momentum(self):
        return self.momentum

class Frame:
    def __init__(self, pressed, dt):
        self.pressed = pressed
        self.dt = dt

"""pos and val - Vector2D class"""
class Arrow:
    def __init__(self, pos, val, color):
        self.pos, self.val = pos, val
        self.color = color
        self.tip = 10
        self.dir = self.val/abs(self.val)
        self.list_of_points = []
        self.list_of_points = [list(self.pos.intpair()),
                               list((self.pos + self.val / 3).intpair()),
                               list((self.pos + self.val / 3 - self.tip * self.dir + self.tip / 3 * self.dir.cross()).intpair()),
                               list((self.pos + self.val / 3 - self.tip * self.dir - self.tip / 3 * self.dir.cross()).intpair()),
                               list((self.pos + self.val / 3).intpair()),
                               ]

    def __call__(self, pos, val):
        self.pos, self.val = pos, val
        self.dir = self.val / abs(self.val)
        self.list_of_points = [list(self.pos.intpair()),
                               list((self.pos + self.val / 3).intpair()),
                               list((self.pos + self.val / 3 - self.tip * self.dir + self.tip/3 * self.dir.cross()).intpair()),
                               list((self.pos + self.val / 3 - self.tip * self.dir - self.tip/3 * self.dir.cross()).intpair()),
                               list((self.pos + self.val / 3).intpair()),
                               ]


"""
Derived class from Scene
It has function for rendering
"""
class GScene(engine.Scene):
    def __init__(self, width, height):
        super(GScene, self).__init__()
        self.sphere_color = {}
        #self.vel_vector = {}
        self.number_arrow = 0
        self.border_active = True
        self.arrow_enable  = False
        self.vel_arrow = {}
        self.rect = Rect(0, 0, width, height)
        print('Create')

    def delete_arrow(self, i):
        self.vel_arrow.pop(i)
        self.number_arrow -= 1


    def handle_border(self):
        self.rect.momentum = engine.Vector2D(0, 0)
        for i in self.sphere:
            if self.sphere[i].pos.x - self.sphere[i].radius < self.rect.left:
                if self.sphere[i].vel.x < 0:
                    p_prev = self.sphere[i].get_momentum()
                    self.sphere[i].vel.x = -self.sphere[i].vel.x
                    self.rect.momentum += ( p_prev-self.sphere[i].get_momentum())
                    self.sphere[i].pos.x = self.rect.left + self.sphere[i].radius

            if self.sphere[i].pos.y - self.sphere[i].radius < self.rect.top:
                if self.sphere[i].vel.y < 0:
                    p_prev = self.sphere[i].get_momentum()
                    self.sphere[i].vel.y = -self.sphere[i].vel.y
                    self.rect.momentum += ( p_prev - self.sphere[i].get_momentum())
                    self.sphere[i].pos.y = self.rect.top + self.sphere[i].radius

            if self.sphere[i].pos.x + self.sphere[i].radius > self.rect.right:
                if self.sphere[i].vel.x > 0:
                    p_prev = self.sphere[i].get_momentum()
                    self.sphere[i].vel.x = -self.sphere[i].vel.x
                    self.rect.momentum += ( p_prev - self.sphere[i].get_momentum())
                    self.sphere[i].pos.x = self.rect.right - self.sphere[i].radius;

            if self.sphere[i].pos.y + self.sphere[i].radius > self.rect.bottom:
                if self.sphere[i].vel.y > 0:
                    p_prev = self.sphere[i].get_momentum()
                    self.sphere[i].vel.y = -self.sphere[i].vel.y
                    self.rect.momentum += ( p_prev - self.sphere[i].get_momentum())
                    self.sphere[i].pos.y = self.rect.bottom - self.sphere[i].radius

    """Update scene state"""
    def update_graphick_scene(self, frame):
        #f = Vec2()
        #f.x = frame.pressed[pygame.K_RIGHT] - frame.pressed[pygame.K_LEFT];
        #f.y = frame.pressed[pygame.K_DOWN] - frame.pressed[pygame.K_UP];
        #f *= self.a
        if self.border_active is True:
            self.handle_border()

        self.update(frame.dt)

        if self.arrow_enable is True:
            for i in self.sphere:
                self.vel_arrow[i](self.sphere[i].pos, self.sphere[i].vel)


        self.collision_response_spheres(self.collision_detection_spheres(frame.dt), frame.dt)



    def render(self, canvas):
        """Draw Player on the Game window"""
        for i in self.sphere:
            canvas.circle(self.sphere_color[i],
                          self.sphere[i].pos.intpair(),
                          self.sphere[i].radius)
        if self.arrow_enable is True:
            for i in self.vel_arrow:
                canvas.arrow(self.vel_arrow[i].color,
                             self.vel_arrow[i].list_of_points
                         )

    def add_arrow(self, pos, vel, color):
        self.vel_arrow[self.number_arrow] = Arrow(pos, vel, color)
        self.number_arrow += 1

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

    def arrow (self, color, list_of_points):
        pygame.draw.lines(self.screen, color, False, list_of_points)


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

        #self.show_vel_vector = False
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
        self.number_speres = 5 #default

        self.scene = GScene(self.width, self.height)

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

        for i in range (0, self.number_speres):
            self.scene.add_arrow(self.scene.sphere[i].pos,
                                 self.scene.sphere[i].vel,
                                 (255 - self.scene.sphere_color[i][0],
                                  255 - self.scene.sphere_color[i][1],
                                  255 - self.scene.sphere_color[i][2])
                                 )


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
                pass#self.show_vel_vector = True

            if event.key == pygame.K_DELETE:
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)
                if i is not False:
                    self.scene.delete_sphere(i)
                    self.scene.delete_arrow(i)
                    i = False

            """Border"""
            if event.key == pygame.K_b:
                if self.scene.border_active is True:
                    self.scene.border_active = False
                else:
                    self.scene.border_active = True

            if event.key == pygame.K_a:
                for i in self.scene.sphere:
                    self.scene.vel_arrow[i](self.scene.sphere[i].pos, self.scene.sphere[i].vel)
                if self.scene.arrow_enable is True:
                    self.scene.arrow_enable = False
                else:
                    self.scene.arrow_enable = True


        if event.type == pygame.MOUSEMOTION:
            """Left mouse button down + motion"""
            #print (pygame.mouse.get_pressed())
            if (pygame.mouse.get_pressed() == (1,0,0)):
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)
                #if i is False:

                if i is not False:
                    self.scene.sphere[i].set_pos(self.pos)
                    self.scene.vel_arrow[i](self.scene.sphere[i].pos,
                                            self.scene.sphere[i].vel)
                    i = False




        if event.type == pygame.MOUSEBUTTONDOWN:
            """Right mouse button down - create new sphere"""

            if (pygame.mouse.get_pressed() == (1, 0, 0)):
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)
                print(self.scene.sphere[i])
            if (pygame.mouse.get_pressed() == (0, 0, 1)):
                self.pos = pygame.mouse.get_pos()
                self.scene.add_sphere(engine.Vector2D(*self.pos),
                                          engine.Vector2D(rnd.randint(100, 500),
                                                          rnd.randint(100, 500)),
                                          engine.Vector2D(0, 0), 1, 50)
                self.scene.sphere_color[self.scene.n_spheres-1] = (rnd.randint(0, 255),
                                              rnd.randint(0, 255),
                                              rnd.randint(0, 255))

                self.scene.add_arrow(self.scene.sphere[self.scene.n_spheres-1].pos,
                                     self.scene.sphere[self.scene.n_spheres-1].vel,
                                     (255 - self.scene.sphere_color[self.scene.n_spheres-1][0],
                                      255 - self.scene.sphere_color[self.scene.n_spheres-1][1],
                                      255 - self.scene.sphere_color[self.scene.n_spheres-1][2])
                                     )
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

            self.scene.calculate_momentum()
            self.scene.calculate_energy()
            self.draw_text("FPS: %6.3f  PLAYTIME: %6.3f SECONDS" %(self.clock.get_fps(), self.playtime),
                           (self.font.get_linesize(), self.height - self.font.get_linesize()*3))
            self.draw_text("MOMENTUM: %6.3f  ENERGY: %6.3f " %(abs(self.scene.calculate_momentum()), self.scene.energy),
                           (self.font.get_linesize(), self.height - self.font.get_linesize() *2))
            self.draw_text("NUMBER OF SPHERES: %6d " % (self.scene.n_spheres),
                           (self.font.get_linesize(), self.height - self.font.get_linesize() * 1))
            self.scene.momentum = engine.Vector2D(0, 0)
            self.scene.energy = 0
            self.flip()

        self.cleanup()

if __name__ == "__main__":
    game = Game()
    game.execute()
