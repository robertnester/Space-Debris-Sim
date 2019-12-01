from pyorbital.orbital import Orbital
from datetime import datetime
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import FPSM

from objloader import *

import random

##tle = tlefile.read('COSMOS 2251', 'cosmos-2251-debris.txt')

orbMat = [[0 for x in range(3)] for y in range(100)]
vertMat = [[0 for x in range(8)] for y in range(100)]

now = datetime.utcnow()

i = 0

##file = open("data_points.txt","w")

for x in range(0,100):
    if x == 0:
        string = 'COSMOS 2251'
    if x >= 1:
        string = 'COSMOS 2251 DEB' + str(x)
    orbX = Orbital(string, 'cosmos-2251-debris.txt')
    orbY = Orbital(string, 'cosmos-2251-debris.txt')
    orbZ = Orbital(string, 'cosmos-2251-debris.txt')

    orbMat[i][0] = 0.49 * orbX.get_position(now)[0][0]
    orbMat[i][1] = 0.49 * orbY.get_position(now)[0][1]
    orbMat[i][2] = 0.49 * orbZ.get_position(now)[0][2]

##    file.write(str(orbMat[i][0]))
##    file.write(", ")
##    file.write(str(orbMat[i][1]))
##    file.write(", ")
##    file.write(str(orbMat[i][2]))
##    file.write("\n")

    i += 1

##file.close()

i = 0
    
for eachOrb in orbMat:
    vertMat[i][0] = [orbMat[i][0], orbMat[i][1], orbMat[i][2]]
    vertMat[i][1] = [orbMat[i][0] + 0.01, orbMat[i][1], orbMat[i][2]]
    vertMat[i][2] = [orbMat[i][0] + 0.01, orbMat[i][1] - 0.01, orbMat[i][2]]
    vertMat[i][3] = [orbMat[i][0], orbMat[i][1] - 0.01, orbMat[i][2]]
    vertMat[i][4] = [orbMat[i][0], orbMat[i][1], orbMat[i][2] + 0.01]
    vertMat[i][5] = [orbMat[i][0] + 0.01, orbMat[i][1], orbMat[i][2] + 0.01]
    vertMat[i][6] = [orbMat[i][0] + 0.01, orbMat[i][1] - 0.01, orbMat[i][2] + 0.01]
    vertMat[i][7] = [orbMat[i][0], orbMat[i][1] - 0.01, orbMat[i][2] + 0.01]
    i += 1

surfaces = [
    [0,1,2,3],
    [6,5,1,2],
    [4,5,1,0],
    [7,4,0,3],
    [7,6,2,3],
    [4,5,7,6]
    ]

def draw(r, g, b):
        
    glBegin(GL_QUADS)
    

    i = 0

    for x in range(0,100):
        glColor3fv((r, g, b))
        for surface in surfaces:
            for vertex in surface:
                glVertex3fv(vertMat[i][vertex])
        i += 1
    
    glEnd()

def main():
    pygame.init()

    wWidth = 1200
    wHeight = 800

    clock = pygame.time.Clock()

    window = pygame.display.set_mode((wWidth, wHeight), DOUBLEBUF|OPENGL)
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(90, wWidth/wHeight, 0.001, 100000.0)
    glMatrixMode(GL_MODELVIEW)

    glTranslate(2,0,0)

    r = 1.0
    g = 0.8
    b = 0.9

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_1]:
            r += 0.01
        if keys[pygame.K_2]:
            r -= 0.01
        if keys[pygame.K_3]:
            g += 0.01
        if keys[pygame.K_4]:
            g -= 0.01
        if keys[pygame.K_5]:
            b += 0.01
        if keys[pygame.K_6]:
            b -= 0.01

        obj = OBJ("earth.obj", swapyz=False)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        draw(r, g, b)

        glCallList(obj.gl_list)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.8, 0.8, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (0.9, 0.8, 0.8, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.15, 0, 0, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION, (50.0, 30.0, 200.0, 8.0))
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        
        mov = FPSM.Spectator()
        mov.get_keys()
        mov.controls_3d(0,'w','s','a','d')
        matrix = mov.controls_3d(.05)

        pygame.display.flip()
        clock.tick(60)

main()
