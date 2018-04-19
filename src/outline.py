'''
	@Description: draw Sphere
	@Author: yiyuan
	@Date: 2018-03-28
'''

import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class neuron():
    def __init__(self):
        self.width = 720
        self.height = 600
        # text = mf.Ui_MainWindow.textBrowser.getPlaceholderText()
        self.neuron = self.loaddata('../src/data/CA228.CNG.swc')

    # 加载数据
    def loaddata(self, filepath):
        f = open(filepath)
        lines = f.readlines()
        f.close()
        x = 0
        while lines[x][0] == '#' :
            x += 1
        data = lines[x].strip().split(' ')
        while data[0] == '' or lines[x][0] == '#':
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

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0.0, 1.0, 0.0)
        length=len(self.neuron)
        i = 1
        while i < length:
            if self.neuron[i][0]==1:
                glPushMatrix()
                glTranslatef(self.neuron[i][1], self.neuron[i][2], self.neuron[i][3])
                glutWireSphere(self.neuron[i][4], 100, 60)
                glPopMatrix()
            else:
                # 远端顶点
                dx = self.neuron[i][1]
                dy = self.neuron[i][2]
                dz = self.neuron[i][3]
                # 近端顶点
                sx = self.neuron[i-1][1]
                sy = self.neuron[i-1][2]
                sz = self.neuron[i-1][3]
                # 圆柱半径
                radius = self.neuron[i][4]
                # 目标圆柱中心轴向量
                bx = dx - sx
                by = dy - sy
                bz = dz - sz
                # 圆柱的高
                dis = math.sqrt(bx*bx+by*by+bz*bz)
                # 初始圆柱平移至(sx,sy,sz)后其中心轴向量(远端坐标)
                px = sx
                py = sy
                pz = sz + dis
                # 计算平移向量与目标的向量的法向量(线性代数：计算两向量的法向量)
                '''
                    0  0  dis 0  0  dis
                    bx by bz  bx by bz
                '''
                fx = -1*by*dis
                fy = dis*bx
                fz = 0
                # 计算第三条边
                ax = math.fabs(dx-px)
                ay = math.fabs(dy-py)
                az = math.fabs(dz-pz)
                lng=math.sqrt(ax*ax+ay*ay+az*az)
                # 余弦定理计算两向量间的夹角
                angle = math.acos((dis*dis*2-lng*lng)/(2*dis*dis))*180/math.pi
                # 变换矩阵栈，先进后出，先绕法向量旋转，再平移
                glPushMatrix()
                glTranslatef(sx,sy,sz)
                glRotatef(angle,fx,fy,fz)
                quadric = gluNewQuadric()
                gluCylinder(quadric,radius,radius,dis,16,12)
                glPopMatrix()
            i = i + 1

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-100, 100, -100, 100, -100, 100)
        gluLookAt(1.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glutSwapBuffers()
        glFlush()

    def cyLinder(self):
        glBegin(GL_QUAD_STRIP)
        glVertex3f(0.0,0.0,0.0)
        for i in range(390):
            p=i*math.pi/180
            glVertex3f(math.sin(p), math.cos(p), 1.0)
            glVertex3f(math.sin(p), math.cos(p), 0.0)
        glEnd()

    def Reshape(self,width,height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1000, 1000, -1000, 1000, -50, 50)
        gluLookAt(1.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0)
        # gluPerspective(45, self.width / self.height, 1.0, 100.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def coords_transfrom(self):
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        # glutInitWindowPosition(50,50)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow("neuron system")
        glClearColor(0.0, 0.0, 0.0, 1.0)
        # glRotatef(45, 0.0, 1.0, 0.0)
        glutDisplayFunc(self.draw)
        glutReshapeFunc(self.Reshape)
        glutMainLoop()


if __name__ == "__main__":
    sp = neuron()
    sp.coords_transfrom()
