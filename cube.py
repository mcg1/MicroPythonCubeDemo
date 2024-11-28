from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN
import time
#from dataclasses import dataclass
import math

graphics = PicoGraphics(display=DISPLAY_COSMIC_UNICORN)

cu = CosmicUnicorn()

class Point3d:
    def __init__(self,x,y,z) -> None:
        self.x = x
        self.y=y
        self.z=z        
    x: float
    y: float
    z: float

    def Normalised(self):
        l = self.x * self.x + self.y * self.y + self.z*self.z
        l = math.sqrt(l)
        return Point3d(self.x/l, self.y/l, self.z / l)

class Point2d:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y=y
    x: int
    y: int

vertex_list = (
    Point3d(-1,-1,-1),
    Point3d(-1,1,-1),
    Point3d(1,1,-1),
    Point3d(1,-1,-1),
    Point3d(-1,-1,1),
    Point3d(-1,1,1),
    Point3d(1,1,1),
    Point3d(1,-1,1),
)

pen_red = (255,0,0)
pen_green = (0,255,0)
pen_cyan = (0,255,255)
pen_yellow = (255,255,0)
pen_black = graphics.create_pen(0,0,0)

tri_list = (
    (0,1,2, pen_green),
    (0,2,3, pen_green),

    (4,7,6, pen_cyan),
    (4,6,5, pen_cyan),

    (1,5,6, pen_red),
    (1,6,2, pen_red),

    (2,6,3, pen_red),
    (3,6,7, pen_red),

    (1,4,5, pen_yellow),
    (0,4,1, pen_yellow),

    (0,7,4, pen_yellow),
    (0,3,7, pen_yellow)
)



def RotatePoint(point:Point3d, rotatedPoint:Point3d, x_angle:float, y_angle:float, z_angle:float):
    #x
    y = point.y*math.sin(x_angle) + point.z * math.cos(x_angle)
    z = point.y*math.cos(x_angle) - point.z * math.sin(x_angle)
    x = point.x

    #y
    x1 = x*math.sin(y_angle) + z * math.cos(y_angle)
    z1 = x*math.cos(y_angle) - z * math.sin(y_angle)
    
    #z
    x = x1*math.sin(z_angle) + y * math.cos(z_angle)
    y1 = x1*math.cos(z_angle) - y * math.sin(z_angle)

    rotatedPoint.x = x
    rotatedPoint.y = y1
    rotatedPoint.z = z1

def TransformTo2D(point:Point3d, point2d: Point2d):
    x = point.x
    y = point.y
    z = point.z
    z += 5
    x = 38 * x / z
    y = 38 * y / z
    x += 16
    y += 16    
    point2d.x = int(x+0.5)
    point2d.y = int(y+0.5)

transformedPoints2d = []
transformedPoints3d = []
act_pen = graphics.create_pen(0,0,0)

def Draw():
    draw_pixel = graphics.pixel
    set_pen = graphics.set_pen
    points_list3d = transformedPoints3d
    points_list2d = transformedPoints2d
    set_pen(pen_black)
    graphics.clear()    

    lx = -0.3
    ly = 0.3
    lz = 0.3

    for (p1,p2,p3,pen) in tri_list:
        v1 = points_list3d[p1]
        v2 = points_list3d[p2]
        v3 = points_list3d[p3]
        a = Point3d(v2.x-v1.x, v2.y-v1.y, v2.z-v1.z).Normalised()
        b = Point3d(v3.x-v1.x, v3.y-v1.y, v3.z-v1.z).Normalised()
        nx = a.y * b.z - a.z * b.y
        ny = a.z * b.x - a.x * b.z
        nz = a.x * b.y - a.y * b.x
        
        if nz<0.1:
            continue

        #set_pen(pen)
        v2d1 = points_list2d[p1]
        v2d2 = points_list2d[p2]
        v2d3 = points_list2d[p3]
        #l = nx*nx + ny*ny + nz*nz
        #l = math.sqrt(l)
        #nz = nz/l
        #ny = ny/l
        #nx = nx/l

        dot = nx * lx + ny * ly + nz * lz
        if dot < 0: dot = 0
        if dot > 1: dot = 1
        dot = 0.2 + dot*0.8
        #dot = 1
        vr = int(pen[0] * dot)
        vg = int(pen[1] * dot)
        vb = int(pen[2] * dot)
        set_pen(graphics.create_pen(vr,vg,vb))
        graphics.triangle(v2d1.x, v2d1.y, v2d2.x, v2d2.y, v2d3.x, v2d3.y)
        graphics.line(v2d1.x, v2d1.y, v2d2.x, v2d2.y)                        
        graphics.line(v2d2.x, v2d2.y, v2d3.x, v2d3.y)
        graphics.line(v2d1.x, v2d1.y, v2d3.x, v2d3.y)

    cu.update(graphics)


cu.set_brightness(0.99)

x_angle = float(0)
y_angle = float(0)
z_angle = float(0)

#pre-populate the array
for point in vertex_list:
    transformedPoints2d.append(Point2d(0,0))
    transformedPoints3d.append(Point3d(0,0,0))

while True:
    x_angle += 0.04
    y_angle += 0.043
    z_angle += 0.008

    for i,point in enumerate(vertex_list):
        RotatePoint(point, transformedPoints3d[i], x_angle,y_angle,z_angle)
        TransformTo2D(transformedPoints3d[i], transformedPoints2d[i])

    Draw()
    if x_angle > math.pi:
        x_angle-= math.pi *2
    if y_angle > math.pi:
        y_angle-= math.pi *2
    if z_angle > math.pi:
        z_angle-= math.pi *2
    time.sleep(0.01)


