import pyglet
from pyglet.gl import *
import numpy as np

class Quad():
    def __init__(self, width, height, xpos, ypos, R, G, B):
        self.width = width
        self.height = height
        self.xpos = xpos
        self.ypos = ypos
        self.R = R
        self.G = G
        self.B = B
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.xpos, self.ypos, 0)
        glColor3f(self.R, self.G, self.B)
        x = self.width / 2
        y = self.height / 2
        vlist = pyglet.graphics.vertex_list(4,
                          ('v2f',[-x, y,
                                  -x, -y,
                                  x, -y,
                                  x, y]))
        vlist.draw(GL_QUADS)
        glPopMatrix()


class Line():
    def __init__(self, xpos, ypos, length, width, quantity, interval, rotation):
        self.xpos = xpos
        self.ypos = ypos
        self.length = length
        self.width = width
        self.quantity = quantity
        self.interval = interval
        self.rotation = rotation
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.xpos, self.ypos, 0)
        glColor3f(0.0, 0.0, 0.0)
        glRotatef(self.rotation, 0, 0, 1)
        glLineWidth(self.width)
        for i in range(self.quantity):
            vlist = pyglet.graphics.vertex_list(2,
                                                ("v2f", [0, 0 + i*self.interval, self.length, 0 + i*self.interval]))
            
            vlist.draw(GL_LINES)
        glPopMatrix()

class cLine():
    def __init__(self, xpos, ypos, length, width, quantity, interval, radius, rotation):
        self.xpos = xpos
        self.ypos = ypos
        self.length = length
        self.width = width
        self.quantity = quantity
        self.interval = interval
        self.radius = float(radius)
        self.rotation = rotation
        self.vertices = 240
    
    def draw(self):
        glPushMatrix()
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable (GL_BLEND)
        glEnable (GL_LINE_SMOOTH)
        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glTranslatef(self.xpos, self.ypos, 0)
        glRotatef(self.rotation, 0, 0, 1)
        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(self.width)
        verts = []
        a = lambda y : np.sqrt(self.radius**2 - y**2)
        for i in range(int(-self.radius*2), int(self.radius*2), self.width):
            x = a(i)
#            verts += [x, float(i), x + self.length, float(i)]
#            vert = [x, float(i), x + self.length, float(i)]
            vlist = pyglet.graphics.vertex_list(2, ("v2f",[x, float(i), x + self.length, float(i)]))
            vlist.draw(GL_LINES)
        glPopMatrix()

class Circle():
    def __init__(self, xpos, ypos, width, radius, vertices):
        self.xpos = round(xpos)
        self.ypos = round(ypos)
        self.width = width
        self.radius = radius
        self.vertices = vertices
    
    def draw(self):
        glPushMatrix()
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable (GL_BLEND) 
        glEnable (GL_LINE_SMOOTH)
        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glLineWidth(self.width)
        glTranslatef(self.xpos, self.ypos, 0)
        glColor3f(1.0, 0.0, 0.0)
        verts = []
        for i in range(self.vertices):
            x = self.radius*np.cos(2*np.pi*float(i)/float(self.vertices))
            y = self.radius*np.sin(2*np.pi*float(i)/float(self.vertices))
            verts += [x, y]
        vlist = pyglet.graphics.vertex_list(self.vertices, ("v2f", verts))
        vlist.draw(GL_LINE_LOOP)
        glPopMatrix()

    def half_circle(self):
        glPushMatrix()
        glClear(GL_COLOR_BUFFER_BIT)
        glLineWidth(self.width)
        glTranslatef(self.xpos, self.ypos, 0)
        glColor3f(0.0, 0.0, 0.0)
        verts = []
        for i in range(self.vertices):
            x = self.radius*np.cos(np.pi*float(i)/float(self.vertices))
            y = self.radius*np.sin(np.pi*float(i)/float(self.vertices))
            verts += [x, y]
        vlist = pyglet.graphics.vertex_list(self.vertices, ("v2f", verts))
        vlist.draw(GL_LINE_LOOP)
        glPopMatrix()
