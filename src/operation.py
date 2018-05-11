import sys
from neuronsystem import neurons
from OpenGL.GLU import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QSlider, QWidget, QFileDialog, QGridLayout, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt, QEvent

def split(filepath):
    if filepath is None:
        return None
    else:
        ind = filepath.index('src')
        path = '../' + filepath[ind:]
        return path

class Ui_MainWindow(QWidget):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setMinimumSize(700,600)
        self.x_last_time_move = 0
        self.y_last_time_move = 0
        layout = QGridLayout()
        self.textBrowser = QtWidgets.QTextBrowser()
        self.glWidget = neurons(self)
        self.glWidgetArea = QScrollArea()
        self.xSlider = self.createSlider(self.glWidget.xRotationChanged, self.glWidget.setXRotation)
        self.ySlider = self.createSlider(self.glWidget.yRotationChanged, self.glWidget.setYRotation)
        self.zSlider = self.createSlider(self.glWidget.zRotationChanged, self.glWidget.setZRotation)
        self.xTrans = self.createTrans(self.glWidget.xTranslationChanged, self.glWidget.setXtranslation)
        self.yTrans = self.createTrans(self.glWidget.yTranslationChanged, self.glWidget.setYtranslation)
        self.zTrans = self.createTrans(self.glWidget.zTranslationChanged, self.glWidget.setZtranslation)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.Point = QtWidgets.QPushButton(self)
        self.Line = QtWidgets.QPushButton(self)
        self.Surface = QtWidgets.QPushButton(self)
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setObjectName("textBrowser")
        self.glWidget.setObjectName("openGLWidget")
        self.glWidgetArea.setWidget(self.glWidget)
        self.glWidgetArea.setWidgetResizable(True)
        self.glWidgetArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.glWidgetArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.glWidgetArea.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)

        self.vertical_bar = self.glWidgetArea.verticalScrollBar()
        self.horizontal_bar = self.glWidgetArea.horizontalScrollBar()
        # self.translate = QtWidgets.QLabel()
        # self.translate.setObjectName("label1")
        # self.rotate = QtWidgets.QLabel()
        # self.rotate.setObjectName("label2")
        # self.rotate.setWordWrap(True)
        # self.rotate.setAlignment(Qt.AlignTop)

        self.glWidgetArea.setMinimumSize(50, 50)
        self.glWidgetArea.installEventFilter(self)

        self.xSlider.setValue(15 * 16)
        self.ySlider.setValue(0 * 16)
        self.zSlider.setValue(0 * 16)

        self.xTrans.setValue(0 * 16)
        self.yTrans.setValue(0 * 16)
        self.zTrans.setValue(0 * 16)

        self.pushButton.clicked.connect(self.button_click)
        self.Point.clicked.connect(self.point_click)
        self.Line.clicked.connect(self.line_click)
        self.Surface.clicked.connect(self.surface_click)

        layout.addWidget(self.textBrowser, 2, 2, 3, 49)
        layout.addWidget(self.pushButton, 2, 52, 3, 8)
        layout.addWidget(self.glWidgetArea, 6, 2, 45, 58)
        layout.addWidget(self.xSlider, 52, 2, 3, 58)
        layout.addWidget(self.ySlider, 55, 2, 3, 58)
        layout.addWidget(self.zSlider, 58, 2, 3, 58)
        layout.addWidget(self.xTrans, 6, 62, 45, 2)
        layout.addWidget(self.yTrans, 6, 64, 45, 2)
        layout.addWidget(self.zTrans, 6, 66, 45, 2)
        layout.addWidget(self.Point, 52, 63, 3, 4)
        layout.addWidget(self.Line, 55, 63, 3, 4)
        layout.addWidget(self.Surface, 58, 63, 3, 4)
        # layout.addWidget(self.translate,2, 64, 3, 2)
        # layout.addWidget(self.rotate,52, 62, 6, 1)

        self.setLayout(layout)

        self.retranslateUi()
        self.setWindowTitle("neuron system")

    def createSlider(self, changedSignal, setterSlot):
        slider = QSlider(Qt.Horizontal,self)
        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QSlider.TicksBelow)

        slider.valueChanged.connect(setterSlot)
        changedSignal.connect(slider.setValue)

        return slider

    def createTrans(self, changedSignal, setterSlot):
        slider = QSlider(Qt.Vertical, self)
        slider.setRange(-1000*16, 1000 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(50 * 16)
        slider.setTickInterval(50 * 16)
        slider.setTickPosition(QSlider.TicksRight)

        slider.valueChanged.connect(setterSlot)
        changedSignal.connect(slider.setValue)

        return slider

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("Form", "Browse"))
        self.Point.setText(_translate("Form", "Point"))
        self.Line.setText(_translate("Form", "Line"))
        self.Surface.setText(_translate("Form", "Surface"))
        # self.translate.setText(_translate("Form", "平移"))
        # self.rotate.setText(_translate("Form", "旋转"))

    def button_click(self):
        dir,type = QFileDialog.getOpenFileName(self,"Browser",'./','All Files (*);;Text Files (*.swc)')
        self.textBrowser.setText(dir)
        dir = split(dir)
        self.glWidget.clear()
        self.glWidget.setpath(dir)
        self.glWidget.initializeGL()

    def point_click(self):
        self.glWidget.setmode(GLU_POINT)
        self.glWidget.initializeGL()

    def line_click(self):
        self.glWidget.setmode(GLU_LINE)
        self.glWidget.initializeGL()

    def surface_click(self):
        self.glWidget.setmode(GLU_FILL)
        self.glWidget.initializeGL()

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            print(event.pos().y())

            if self.y_last_time_move == 0:
                self.last_time_move = event.pos().y()

            distance = self.x_last_time_move - event.pos().y()
            self.vertical_bar.setValue(self.vertical_bar.value() + distance)
            self.y_last_time_move = event.pos().y()

        elif event.type() == QEvent.MouseButtonRelease:
            self.y_last_time_move = 0

        if event.type() == QEvent.MouseMove:
            print(event.pos().x())

            if self.x_last_time_move == 0:
                self.last_time_move = event.pos().x()

            distance = self.x_last_time_move - event.pos().x()
            self.horizontal_bar.setValue(self.horizontal_bar.value() + distance)
            self.x_last_time_move = event.pos().x()

        elif event.type() == QEvent.MouseButtonRelease:
            self.x_last_time_move = 0

        return QWidget.eventFilter(self, source, event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sp = Ui_MainWindow()
    sp.show()
    sys.exit(app.exec_())
    