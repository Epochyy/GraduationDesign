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
    xTranslationChanged = pyqtSignal(int)
    yTranslationChanged = pyqtSignal(int)
    zTranslationChanged = pyqtSignal(int)
    def __init__(self, parent = None):
        super(neurons, self).__init__(parent)
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTran = 0
        self.yTran = 0
        self.zTran = 0
        self.lastPos = QPoint()
        self.color = [(1.0,0.0,0.0),(0.0,1.0,0.0),(0.8,0.6,0.0)]
        self.coords = 0
        self.gRot = 0
        self.filepath = None
        self.width = 2000
        self.height = 2000
        self.scale = 1
        self.flag = False
        self.style = 0
        self.mode = GLU_FILL
        # timer = QTimer(self)
        # timer.timeout.connect(self.advance)
        # timer.start(50)
    def clear(self):
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.xTran = 0
        self.yTran = 0
        self.zTran = 0
        self.lastPos = QPoint()
        self.color = [(1.0,0.0,0.0),(0.0,1.0,0.0),(0.8,0.6,0.0)]
        self.coords = 0
        self.gRot = 0
        self.filepath = None
        self.scale = 1
        self.width = 1000
        self.height = 1000
        self.flag = False
        self.style = 1
        self.mode = GLU_FILL

    def setmode(self, mode):
        self.mode = mode

    def changestyle(self,style):
        self.style = style

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
            if self.style == 0:
                self.object = self.makeObject(self.mode)
            else:
                self.object = self.skeleton()
        else:
            self.object=None
        lightPos = (0.5, 0.5, 0.5, 1.0)
        light_ambient = (0.0, 0.0, 0.0, 1.0)
        light_diffuse = (1.0, 1.0, 1.0, 1.0)
        light_specular = (1.0, 1.0, 1.0, 1.0)
        glLightfv(GL_LIGHT1, GL_SPOT_CUTOFF, 45)
        # glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
        # glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
        # glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHTING)
        # 开启深度测试
        glEnable(GL_DEPTH_TEST)
        # 开始颜色追踪
        glEnable(GL_COLOR_MATERIAL)
        # 设置颜色追踪的材料属性
        # glColorMaterial(GL_FRONT, GL_POSITION)
        # glColorMaterial(GL_FRONT, GL_AMBIENT)
        glColorMaterial(GL_FRONT, GL_DIFFUSE)
        # glColorMaterial(GL_FRONT, GL_SPECULAR)
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
        # glTranslate()
        glScale(self.scale, self.scale, self.scale)
        self.drawNeurons(self.xTran / 16.0, self.yTran / 16.0, self.zTran / 16.0, self.gRot / 16.0)
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
            glOrtho(-1 * self.coords, self.coords, -1 * self.coords, self.coords, -1 * self.coords, self.coords)
            glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def resizeGL(self, width, height):
        glViewport(0,0,width,height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 0.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.coords!=0:
            glOrtho(-1 * self.coords, self.coords, -1 * self.coords, self.coords, -1 * self.coords, self.coords)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    # 加载数据
    def loaddata(self, filepath):
        coords = 0
        if filepath is None or filepath == '':
            return None,0
        with open(filepath) as f:
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
            coords = max(coords, math.fabs(neuron[1][1]))
            coords = max(coords, math.fabs(neuron[1][2]))
            coords = max(coords, math.fabs(neuron[1][3]))
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

    def makeObject(self,mode=GLU_FILL):
        if self.neuron is not None:
            genList = glGenLists(1)
            glNewList(genList, GL_COMPILE)
            length = len(self.neuron)
            k = 0
            glColor3f(1.0, 0.0, 0.0)
            self.coords = self.coords + 100
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-1 * self.coords, self.coords, -1 * self.coords, self.coords, -1 * self.coords, self.coords)
            glMatrixMode(GL_MODELVIEW)
            # glLoadIdentity()
            i = 1
            while i < length:
                if self.neuron[i][0] == 1:
                    glPushMatrix()
                    glTranslatef(self.neuron[i][1], self.neuron[i][2], self.neuron[i][3])
                    my_quad = gluNewQuadric()
                    gluQuadricDrawStyle(my_quad, mode)
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
                    # 圆台底半径
                    dradius = self.neuron[i-1][4]
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
                    gluQuadricDrawStyle(quadric, mode)
                    gluCylinder(quadric, radius, radius, dis, 16, 12)
                    glPopMatrix()
                i = i + 1
                if self.neuron[i][5] != i-1:
                    glColor3f(self.color[k%3][0], self.color[k%3][1], self.color[k%3][2])
                    k = k + 1
            # self.coords = self.coords + 100
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-1 * self.coords, self.coords, -1 * self.coords,self.coords, -1 * self.coords, self.coords)
            gluLookAt(1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            # glutSwapBuffers()
            glFlush()
            glEndList()
            return genList

    # 神经元骨架结构
    def skeleton(self):
        if self.neuron is not None:
            genList = glGenLists(1)
            glNewList(genList, GL_COMPILE)
            length = len(self.neuron)
            k = 0
            glColor3f(1.0, 0.0, 0.0)
            self.coords = self.coords + 100
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-1 * self.coords, self.coords, -1 * self.coords, self.coords, -1 * self.coords, self.coords)
            glMatrixMode(GL_MODELVIEW)
            # glLoadIdentity()
            dx = self.neuron[1][1]
            dy = self.neuron[1][2]
            dz = self.neuron[1][3]
            i = 2
            while i < length:
                # 近端顶点
                if self.neuron[i][5] == -1:
                    self.neuron[i][5] = 1
                sx = self.neuron[self.neuron[i][5]][1]
                sy = self.neuron[self.neuron[i][5]][2]
                sz = self.neuron[self.neuron[i][5]][3]
                glPushMatrix()
                glBegin(GL_LINE)
                glVertex3f(dx,dy,dz)
                glVertex3f(sx,sy,sz)
                glEnd()
                glPopMatrix()
                i = i + 1
                # 远端顶点
                dx = self.neuron[i][1]
                dy = self.neuron[i][2]
                dz = self.neuron[i][3]
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-1 * self.coords, self.coords, -1 * self.coords, self.coords, -1 * self.coords, self.coords)
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
            if self.scale >= 32:
                self.flag = True
            elif self.scale <= 1:
                self.flag = False
            if self.flag:
                self.scale = self.scale / 2
            else:
                self.scale = self.scale * 2
            self.coords = self.coords * self.scale

    def setXtranslation(self,value):
        value = self.normalizeValue(value)
        if value != self.xTran:
            self.xTran = value
            self.xTranslationChanged.emit(value)
            self.update()

    def setYtranslation(self,value):
        value = self.normalizeValue(value)
        if value != self.yTran:
            self.yTran = value
            self.yTranslationChanged.emit(value)
            self.update()

    def setZtranslation(self,value):
        value = self.normalizeValue(value)
        if value != self.zTran:
            self.zTran = value
            self.zTranslationChanged.emit(value)
            self.update()

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def normalizeValue(self, value):
        while value < -1000*16:
            value += 2000*6
        while value > 1000*16:
            value -= 2000*16
        return value

