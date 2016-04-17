import math
import random as rnd
#service clas Vector2D


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector2D({}, {})'.format(self.x, self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        return other - self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __mul__(self, other):
        return self.x*other.x + self.y*other.y

    def __call__(self, x, y):
        self.x, self.y = x, y

    #@property
    def len(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def intpair(self):
        return (int(self.x), int(self.y))
    """
    def __setattr__(self, key, value):
        #print(key, value)
        object.__setattr__(self, key, value)
    """

class PlaneStatic2D:
    """
    point1 and point2 have to be an instance of Vector2D
    """
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.direction_vector = self.point1 - self.point2
        self.normal = Vector2D(self.direction_vector.y, -self.direction_vector.x)

    def __repr__(self):
        return 'PlaneStatic2D({}, {}, {})'.format(self.point1, self.point2, self.normal)

    def __str__(self):
        return '({}, {}, {})'.format(self.point1, self.point2, self.normal)

    """
    def __setattr__(self, key, value):
        print(key, value)
        if not key in self.__dict__:
            object.__setattr__(self, key, value)
        elif key == "point1" or "point2":
            object.__setattr__(self, key, value)
            self.direction_vector = self.point1 - self.point2
            self.normal = Vector2D(self.direction_vector.y, -self.direction_vector.x)
    """


"""
    Base class. Argument pos [position] have to be setted
    pos, vel, acc have to be a specimen of Vector2D class
    pos - position
    vel - velocity
    acc - acceleration
"""
class RigidBody:
    def __init__(self, pos, vel=Vector2D(0, 0), acc=Vector2D(0, 0), mass=1):
        self.pos, self.vel, self.acc = pos, vel, acc
        self.mass = mass

class Sphere(RigidBody):
    def __init__(self,  pos, vel=Vector2D(0, 0), acc=Vector2D(0, 0), mass=1, radius=10):
        super(Sphere, self).__init__(pos, vel, acc, mass)
        self.radius = radius

    #self < other
    def __lt__(self, other):
        return self.radius < other.radius

    # self <= other
    def __le__(self, other):
        return self.radius <= other.radius

    # self == other
    def __eq__(self, other):
        return self.radius == other.radius

    # self != other
    def __ne__(self, other):
        return self.radius != other.radius

    # self > other
    def __gt__(self, other):
        return self.radius > other.radius

    # self != other
    def __ge__(self, other):
        return self.radius >= other.radius

    def __repr__(self):
        return 'Shere2D({}, {}, {}, {}, {} )'.format(self.pos, self.vel, self.acc, self.mass, self.radius)

    def __str__(self):
        return '({}, {}, {}, {}, {})'.format(self.pos, self.vel, self.acc, self.mass, self.radius)

    def __iter__(self):
        pass
"""
This class contains containers of objects of the class. It used for set physical scene.
You have to create only one intanse of class Scene.
"""
class Scene:

    def __init__(self, width=800, height=600, n_spheres=0, n_planes=0):
        self.size = self.width, self.height = width, height
        self.n_spheres, self.n_planes = n_spheres, n_planes

        rnd.seed()

        #list of all spheres
        self.list_of_spheres = []

        for i in range(0, self.n_spheres):
            self.set_sphere(Vector2D(rnd.randint(10, self.width - 10), rnd.randint(10, self.height - 10)))

        self.list_of_spheres.sort(reverse=True)

    def __str__(self):
        str_out = ''
        for i in range(0, self.n_spheres):
            str_out +=  i.__repr__() +' ' + self.list_of_spheres[i].__repr__() + '\n'
        return str_out



    """
    Add sphere to list of spheres
    """
    def set_sphere(self, pos, vel=Vector2D(0, 0), acc=Vector2D(0, 0), mass=1, radius=10):
        self.list_of_spheres.append(Sphere(pos, vel, acc, mass, rnd.randint(1, 10)))

    def set_plane(self):
        pass

    def update(self):
        pass



class Cell:
    pass

sc = Scene(800, 600, 10)

print(sc)



