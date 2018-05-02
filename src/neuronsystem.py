# -*- coding: utf-8 -*-

import math

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize, QTimer

class neurons(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)
    def __init__(self, parent = None):
        super(neurons, self).__init__(parent)
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.lastPos = QPoint()
        self.color = [(1.0,0.0,0.0),(0.0,1.0,0.0),(0.8,0.6,0.0)]
        self.coords = 0
        self.gRot = 0
        self.filepath = None
        self.scale = 1
        self.flag = False
        self.width = 450
        self.height = 580
        # timer = QTimer(self)
        # timer.timeout.connect(self.advance)
        # timer.start(50)

    def setpath(self,dir):
        self.filepath = dir

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(450, 580)

    def resize(self):
        return QSize(450*self.scale,580*self.scale)

    def initializeGL(self):
        # 数据中有两个根房室如何解决？？？
        self.coords = 0
        if self.filepath is not None:
            self.neuron,self.coords = self.loaddata(self.filepath)
            self.object = self.makeObject()
        else:
            self.object=None
        lightPos = (5.0, 5.0, 10.0, 1.0)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glColor3f(1.0, 0.0, 0.0)
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        glScale(self.scale, self.scale, self.scale)
        self.drawNeurons(0.0, 0.0, 0.0, self.gRot / 16.0)
        glRotated(+90.0, 1.0, 0.0, 0.0)
        glPopMatrix()
        glFlush()
        self.update()

    def advance(self):
        self.gRot += 2 * 16
        self.update()

    def drawNeurons(self, dx, dy, dz, angle):
        glPushMatrix()
        glTranslated(dx, dy, dz)
        glRotated(angle, 0.0, 0.0, 1.0)
        if self.object is not None:
            glCallList(self.object)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-1 * self.coords*self.scale, self.coords*self.scale, -1 * self.coords*self.scale,
                    self.coords*self.scale, -1 * self.coords*self.scale, self.coords*self.scale)
            glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def resizeGL(self, width, height):
        glViewport(0,0,width,height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 0.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.coords!=0:
            glOrtho(-1*self.coords*self.scale, self.coords*self.scale, -1*self.coords*self.scale,
                    self.coords*self.scale, -1*self.coords*self.scale, self.coords*self.scale)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    # 加载数据
    def loaddata(self, filepath):
        coords = 0
        if filepath is None:
            return None,0
        f = open(filepath)
        lines = f.readlines()
        f.close()
        x = 0
        while lines[x][0] == '#':
            x += 1
        data = lines[x].strip().split(' ')
        while data[0] == '' or lines[x][0] == '#':
            x += 1
            data = lines[x].strip().split(' ')

        neuron = {
            int(data[0]): [int(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]),
                           int(data[6])]}
        coords = max(coords, neuron[1][1])
        coords = max(coords, neuron[1][2])
        coords = max(coords, neuron[1][3])
        x += 1
        cnt = 2
        lines = lines[x:]
        for line in lines:
            data = line.strip().split(' ')
            neuron.setdefault(int(data[0]), []).extend(
                [int(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]), int(data[6])])
            coords = max(coords, neuron[cnt][1])
            coords = max(coords, neuron[cnt][2])
            coords = max(coords, neuron[cnt][3])
            cnt += 1
            # print(neuron[float(data[0])])
        return neuron,coords

    def makeObject(self):
        genList = glGenLists(1)
        glNewList(genList, GL_COMPILE)
        length = len(self.neuron)
        k = 0
        glColor3f(1.0, 0.0, 0.0)
        self.coords = self.coords + 100
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1 * self.coords*self.scale, self.coords*self.scale, -1 * self.coords*self.scale,
                self.coords*self.scale, -1 * self.coords*self.scale, self.coords*self.scale)
        glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()
        i = 1
        while i < length:
            if self.neuron[i][0] == 1:
                glPushMatrix()
                glTranslatef(self.neuron[i][1], self.neuron[i][2], self.neuron[i][3])
                my_quad = gluNewQuadric()
                gluSphere(my_quad,self.neuron[i][4], 32, 16)
                glPopMatrix()
            else:
                # 远端顶点
                dx = self.neuron[i][1]
                dy = self.neuron[i][2]
                dz = self.neuron[i][3]
                # 近端顶点
                if self.neuron[i][5] == -1:
                    self.neuron[i][5] = 1
                sx = self.neuron[self.neuron[i][5]][1]
                sy = self.neuron[self.neuron[i][5]][2]
                sz = self.neuron[self.neuron[i][5]][3]
                # 圆柱半径
                radius = self.neuron[i][4]
                # 目标圆柱中心轴向量
                bx = dx - sx
                by = dy - sy
                bz = dz - sz
                # 圆柱的高
                dis = math.sqrt(bx * bx + by * by + bz * bz)
                # 初始圆柱平移至(sx,sy,sz)后其中心轴向量(远端坐标)
                px = sx
                py = sy
                pz = sz + dis
                # 计算平移向量与目标的向量的法向量(线性代数：计算两向量的法向量)
                '''
                    0  0  dis 0  0  dis
                    bx by bz  bx by bz
                '''
                fx = -1 * by * dis
                fy = dis * bx
                fz = 0
                # 计算第三条边
                ax = math.fabs(dx - px)
                ay = math.fabs(dy - py)
                az = math.fabs(dz - pz)
                lng = math.sqrt(ax * ax + ay * ay + az * az)
                # 余弦定理计算两向量间的夹角
                angle = math.acos((dis * dis * 2 - lng * lng) / (2 * dis * dis)) * 180 / math.pi
                # 变换矩阵栈，先进后出，先绕法向量旋转，再平移
                glPushMatrix()
                glTranslatef(sx, sy, sz)
                glRotatef(angle, fx, fy, fz)
                quadric = gluNewQuadric()
                gluCylinder(quadric, radius, radius, dis, 16, 12)
                glPopMatrix()
            i = i + 1
            if self.neuron[i][5] != i-1:
                glColor3f(self.color[k%3][0], self.color[k%3][1], self.color[k%3][2])
                k = k + 1
        # self.coords = self.coords + 100
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1 * self.coords * self.scale, self.coords * self.scale, -1 * self.coords * self.scale,
                self.coords * self.scale, -1 * self.coords * self.scale, self.coords * self.scale)
        gluLookAt(1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # glutSwapBuffers()
        glFlush()
        glEndList()
        return genList

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()
    # 点击--旋转
    def mousePressEvent(self, event):
        self.lastPos = event.localPos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons():
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.localPos()

    # 放大--缩小
    def mouseDoubleClickEvent(self, QMouseEvent):
        if self.filepath is not None and QMouseEvent.buttons():
            if self.scale >= 16:
                self.flag = True
            elif self.scale <= 1:
                self.flag = False
            if self.flag:
                self.scale = self.scale / 2
            else:
                self.scale = self.scale * 2
            self.coords = self.coords * self.scale
            self.resize()

    def translation(self):
        pass

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

