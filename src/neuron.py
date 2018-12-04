'''
	@Description: draw Sphere
	@Author: yiyuan
	@Date: 2018-03-28
'''

import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


class neuron():
    def __init__(self):
        self.vertical_slice=50
        self.horizontal_slice=50
        self.width=720
        self.height=600
        self.vertices=[]
        self.indices=[]
        self.cellposition=[(0.2,0.1,0.2,0.1),(-0.4,-0.5,0.2,0.2)]

    # 加载数据
    def loaddata(self, filepath):
        f = open(filepath)
        lines = f.readlines()
        f.close()
        x = 0
        while lines[x][0] == '#':
            x += 1
        data = lines[x].strip().split(' ')
        neuron = {
            int(data[0]): [int(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]),
                           int(data[6])]}
        x += 1
        lines = lines[x:]
        for line in lines:
            data = line.strip().split(' ')
            neuron.setdefault(int(data[0]), []).extend(
                [int(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]), int(data[6])])
            # print(neuron[float(data[0])])
        return neuron

    def getcoords(self):
        neuron=self.loaddata('../src/data/recon.swc')
        for item in neuron.keys():
            data=neuron[item]
            self.cellposition.append((data[1],data[2],data[3],data[4]))

    def window_resize(window, width, height):
        glViewport(0, 0, width, height)

    def drawshadow(self,radius):
        self.vertices=[]
        self.indices=[]
        # 经度
        vstep = 2 * math.pi / self.vertical_slice
        # 纬度
        hstep = math.pi / self.horizontal_slice
        start_index=0
        current_index=0
        # 绘制上端三角形
        for i in range(self.horizontal_slice+1):
            start_index=current_index
            vertical_angle = hstep * i
            z_coord = radius * math.cos(vertical_angle)
            sub_radius = radius * math.sin(vertical_angle)
            for j in range(self.vertical_slice+1):
                horizontal_angle = vstep * j
                x_coord = sub_radius * math.cos(horizontal_angle)
                y_coord = sub_radius * math.sin(horizontal_angle)
                if j==self.vertical_slice:
                    self.vertices.append((self.vertices[start_index][0],
                                          self.vertices[start_index][1],
                                          self.vertices[start_index][2]))
                else:
                    self.vertices.append((x_coord,z_coord,y_coord))
                current_index=current_index+1
                if i>0 and j>0:
                    bottom_ring_a = (self.vertical_slice + 1) * i + j
                    bottom_ring_b = (self.vertical_slice + 1) * i + j - 1
                    top_ring_a = (self.vertical_slice + 1) * (i - 1) + j
                    top_ring_b = (self.vertical_slice + 1) * (i - 1) + j - 1
                    if j==1:
                        self.indices.append(bottom_ring_a)
                        self.indices.append(top_ring_a)
                        self.indices.append(top_ring_b)
                    elif j==self.horizontal_slice:
                        self.indices.append(bottom_ring_a)
                        self.indices.append(top_ring_b)
                        self.indices.append(bottom_ring_b)
                    else:
                        self.indices.append(bottom_ring_a)
                        self.indices.append(top_ring_a)
                        self.indices.append(top_ring_b)
                        self.indices.append(bottom_ring_a)
                        self.indices.append(top_ring_b)
                        self.indices.append(bottom_ring_b)

    def showSphere(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        gluPerspective(45.0, (display[0] / display[1]), 0.1, 100.0)

        glTranslatef(0.0, 0.0, -3.0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            glRotatef(1, 1, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            for i in range(len(self.cellposition)):
                self.drawshadow(self.cellposition[i][3])
                # self.cellposition[i][0], self.cellposition[i][1], self.cellposition[i][2],

                glBegin(GL_LINE_LOOP)
                for item in self.vertices:
                    glVertex3fv(item)
                glEnd()

            pygame.display.flip()
            pygame.time.wait(5)
if __name__ == "__main__":
    sp=neuron()
    # sp.getcoords()
    sp.showSphere()
