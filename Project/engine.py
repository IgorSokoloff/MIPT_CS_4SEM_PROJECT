import math
#service clas Vector2D


"""
There won't be any functions for planeStatic class in first beta version
There won't be any differences beetwen "static" and "dinamic" spheres (static a also will update)

"""


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        self.x = self.x / abs(self)
        self.y = self.y / abs(self)
    """
    It returns scalar
    @param: other - Vector2D
    """
    def сross_product (self, other):
        return (self.x * other.y - self.y * other.x )

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
        if type(other) is Vector2D:
            return self.x*other.x + self.y*other.y
        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        if type(other) is Vector2D:
            return self.x * other.x + self.y * other.y
        return Vector2D(self.x * other, self.y * other)

    def __truediv__(self, other ):
        return Vector2D(self.x / other, self.y / other)

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
        self.imass = 1/mass


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

    def __call__(self, pos, vel, acc):
        self.pos, self.vel, self.acc = pos, vel, acc

    def __iter__(self):
        pass

    def apply_impulse(self, contact, normal, impulse):
        self.vel += impulse * normal * self.imass

    def update_vel(self, dt):
        self.vel += self.acc * dt

    def update_pos (self, dt):
        self.pos += self.vel * dt

    """
    update position and velocity
    """


    def update (self, dt):
        self.update_vel(dt)
        self.update_pos(dt)


"""
This class contains containers of objects of the class. It used for set physical scene.
You have to create only one intanse of class Scene.
"""
class Scene:

    def __init__(self ):
        self.n_planes = 0
        self.n_spheres = 0
        self.sphere = {}

        self.depth = []
        # array of index
        #self.l_sphere = []

    def __str__(self):
        str_out = ''
        for i in range(0, self.n_spheres):
            str_out +=  i.__repr__() +' ' + self.sphere[i].__repr__() + '\n'
        return str_out


    def add_sphere(self, pos, vel=Vector2D(0, 0), acc=Vector2D(0, 0), mass=1, radius=10):
        self.sphere[self.n_spheres] = Sphere(pos, vel, acc, mass, radius)
        self.n_spheres += 1

        #demo
        #self.l_sphere = list(self.sphere)

    def vel_relative(self, normal, contact, i, j):
        return   (normal.x * (self.sphere[i].vel.x - self.sphere[j].vel.x) +
                  normal.y * (self.sphere[i].vel.y - self.sphere[j].vel.y))


    # TODO: добавить position_based подход
    # TODO: добавить алгоритмы генерации сцены


    #На взод принимает массив индексов сфер из дереве всех сфер
    #То есть те которые будем обрабатывать
    #На выходе список из кортежей пар индексов
    #(пока что проходит просто по дереву)

    """
    self.sphere[col_spheres[i][0]] - second sphere in colision number i
    self.sphere[col_spheres[i][0]] - first sphere in colision number i
    принимает лист из пар индексов
    """
#
    def collision_detection_spheres(self, dt):
        col_spheres = []
        for i in range(0, self.n_spheres-1 ):
            for j in range(i + 1, self.n_spheres):

                pos_ex_i, pos_ex_j = self.sphere[i].pos, self.sphere[j].pos
                vel_ex_i, vel_ex_j = self.sphere[i].vel, self.sphere[j].vel
                acc_ex_i, acc_ex_j = self.sphere[i].acc, self.sphere[j].acc
                self.sphere[i].update(dt)
                if (abs(  self.sphere[i].pos - self.sphere[j].pos  ) < (self.sphere[i].radius + self.sphere[j].radius)):
                    self.depth.append( (self.sphere[i].radius + self.sphere[j].radius) - abs(  self.sphere[i].pos - self.sphere[j].pos  ))
                    self.sphere[i](pos_ex_i, vel_ex_i, acc_ex_i)
                    self.sphere[j](pos_ex_j, vel_ex_j, acc_ex_j)
                    col_spheres.append((i, j))
                else:
                    self.sphere[i](pos_ex_i, vel_ex_i, acc_ex_i)
                    self.sphere[j](pos_ex_j, vel_ex_j, acc_ex_j)

                    #print('Crash')
        return col_spheres

    def calculate_normal (self, i, j):
        n = self.sphere[i].pos - self.sphere[j].pos
        n.norm()
        return n

    def calculate_contact(self, i, j):
        r1, r2 = self.sphere[i].radius, self.sphere[j].radius

        if (self.sphere[i].pos.x < self.sphere[j].pos.x):
            return self.sphere[i].pos + (r1 / (r1 + r2)) * (self.sphere[j].pos - self.sphere[i].pos)
        else:
            return self.sphere[j].pos + (r2 / (r1 + r2)) * (self.sphere[i].pos - self.sphere[j].pos)


    def calculate_impulse(self, normal, contact, i, j ):
        R1 = contact - self.sphere[i].pos
        R2 = contact - self.sphere[j].pos
        MIN_V = 8
        E = 1
        #Z1 = normal.сross_product(R1) * self.sphere[i].imass
        #Z2 = normal.сross_product(R2) * self.sphere[j].imass

        J = ( normal.x * (normal.x * self.sphere[i].imass + normal.x * self.sphere[j].imass)
              + normal.y * (normal.y * self.sphere[i].imass + normal.y * self.sphere[j].imass) )
        return ( MIN_V - (1 + E) * self.vel_relative(normal,contact, i, j) ) / J

    def colision_response_spheres(self, col_spheres, dt):
        for i in range(0, len(col_spheres)):
            m1 = self.sphere[col_spheres[i][0]].mass
            m2 = self.sphere[col_spheres[i][1]].mass
            #print (col_spheres[i][0], col_spheres[i][1])

            #self.sphere[col_spheres[i][0]].vel = (self.sphere[col_spheres[i][0]].vel * (m1 - m2) + (2 * m2 * self.sphere[col_spheres[i][1]].vel))/(m1 + m2)
            #self.sphere[col_spheres[i][1]].vel = -(self.sphere[col_spheres[i][1]].vel * (m2 - m1) + (2 * m1 * self.sphere[col_spheres[i][0]].vel))/(m1 + m2)

            contact = self.calculate_contact(col_spheres[i][0], col_spheres[i][1])
            normal =  self.calculate_normal(col_spheres[i][0], col_spheres[i][1])
            impulse = self.calculate_impulse(normal, contact, col_spheres[i][0], col_spheres[i][1])
            self.sphere[col_spheres[i][0]].apply_impulse(contact, normal, impulse)
            self.sphere[col_spheres[i][1]].apply_impulse(contact, normal, -impulse)
            print ("")

            #self.sphere[col_spheres[i][0]].update_pos(dt)
            #self.sphere[col_spheres[i][1]].update_pos(dt)

            while (abs(self.sphere[col_spheres[i][0]].pos - self.sphere[col_spheres[i][1]].pos) <
                       (self.sphere[col_spheres[i][0]].radius + self.sphere[col_spheres[i][1]].radius)):
                self.sphere[col_spheres[i][0]].update_pos(dt)
                self.sphere[col_spheres[i][1]].update_pos(dt)

            self.sphere[col_spheres[i][0]].update(dt)
            self.sphere[col_spheres[i][1]].update(dt)


    def update(self, dt):
        for i in range(0, self.n_spheres):
            self.sphere[i].update(dt)

            #if (self.collision_detection() != False):

    def set_plane(self):
        pass




class Cell:
    pass

