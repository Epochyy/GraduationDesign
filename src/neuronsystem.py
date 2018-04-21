# -*- coding: utf-8 -*-

import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QSlider, QWidget, QFileDialog, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize
from PyQt5.QtGui import QColor

class neurons(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)
    def __init__(self,parent = None):
        super(neurons, self).__init__(parent)
        self.width = 720
        self.height = 600
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.lastPos = QPoint()
        self.color=[(1.0,0.0,0.0),(0.0,1.0,0.0),(0.8,0.6,0.0)]
        self.coords=0

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(400, 400)

    def initializeGL(self):
        # 数据中有两个根房室如何解决？？？
        self.neuron = self.loaddata('../src/data/Series003_cmle.CNG.swc')
        lightPos = (5.0, 5.0, 10.0, 1.0)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_FLAT)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.object = self.makeObject()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glColor3f(1.0, 0.0, 0.0)
        glCallList(self.object)
        glFlush()

    def resizeGL(self, width, height):
        glViewport(0,0,width,height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 0.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1*self.coords, self.coords, -1*self.coords, self.coords, -1*self.coords, self.coords)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    # 加载数据
    def loaddata(self, filepath):
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
        x += 1
        lines = lines[x:]
        for line in lines:
            data = line.strip().split(' ')
            neuron.setdefault(int(data[0]), []).extend(
                [int(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]), int(data[6])])
            # print(neuron[float(data[0])])
        return neuron

    def makeObject(self):
        genList = glGenLists(1)
        glNewList(genList, GL_COMPILE)
        length = len(self.neuron)
        k = 0
        glColor3f(1.0, 0.0, 0.0)
        i = 1
        while i < length:
            self.coords = max(self.coords,self.neuron[i][1])
            self.coords = max(self.coords,self.neuron[i][2])
            self.coords = max(self.coords,self.neuron[i][3])
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
        self.coords = self.coords + 100
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1*self.coords, self.coords, -1*self.coords, self.coords, -1*self.coords, self.coords)
        gluLookAt(1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # glutSwapBuffers()
        glFlush()
        glEndList()
        return genList

    def scale(self,fs):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0,0.0,0.0,1.0)
        glScale(fs,fs,fs)


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

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle


class Ui_MainWindow(QWidget):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        # layout = QGridLayout()
        self.textBrowser = QtWidgets.QTextBrowser()
        self.xSlider = self.createSlider()
        self.ySlider = self.createSlider()
        self.zSlider = self.createSlider()
        self.glWidget = neurons(self)
        self.xSlider.valueChanged.connect(self.glWidget.setXRotation)
        self.glWidget.xRotationChanged.connect(self.xSlider.setValue)
        self.ySlider.valueChanged.connect(self.glWidget.setYRotation)
        self.glWidget.yRotationChanged.connect(self.ySlider.setValue)
        self.zSlider.valueChanged.connect(self.glWidget.setZRotation)
        self.glWidget.zRotationChanged.connect(self.zSlider.setValue)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(380, 10, 81, 32))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 341, 31))
        self.textBrowser.setObjectName("textBrowser")
        self.glWidget.setGeometry(QtCore.QRect(19, 59, 441, 391))
        self.glWidget.setObjectName("openGLWidget")
        self.xSlider.setGeometry(QtCore.QRect(480, 70, 22, 371))
        self.ySlider.setGeometry(QtCore.QRect(530, 70, 22, 371))
        self.zSlider.setGeometry(QtCore.QRect(580, 70, 22, 371))
        self.xSlider.setValue(15 * 16)
        self.ySlider.setValue(345 * 16)
        self.zSlider.setValue(0 * 16)

        self.pushButton.clicked.connect(self.button_click)
        # hlayout = QHBoxLayout()
        # vlayout = QVBoxLayout()
        # vlayout.addWidget(self.textBrowser)
        # vlayout.addWidget(self.pushButton)
        # vlayout.addWidget(self.glWidget)
        # hlayout.addWidget(self.xSlider)
        # hlayout.addWidget(self.ySlider)
        # hlayout.addWidget(self.zSlider)
        # hlayout.setGeometry(QtCore.QRect(450,60,30,380))
        # vlayout.setGeometry(QtCore.QRect(10,10,420,480))
        # layout.addChildLayout(vlayout)
        # layout.addChildLayout(hlayout)
        # self.setLayout(layout)
        self.retranslateUi()
        self.setWindowTitle("neuron system")

    def createSlider(self):
        slider = QSlider(Qt.Vertical,self)
        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QSlider.TicksRight)

        return slider

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        # Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Browse"))

    def button_click(self):
        dir,type = QFileDialog.getOpenFileName(self,"Browser",'../src/','All Files (*);;Text Files (*.swc)')
        self.textBrowser.setText(dir)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sp = Ui_MainWindow()
    sp.show()
    sys.exit(app.exec_())