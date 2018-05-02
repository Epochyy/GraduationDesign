from neuronsystem import neurons
from OpenGL.GLUT import *
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
        self.setMinimumSize(600,600)
        self.x_last_time_move = 0
        self.y_last_time_move = 0
        layout = QGridLayout()
        self.textBrowser = QtWidgets.QTextBrowser()
        self.glWidget = neurons(self)
        self.glWidgetArea = QScrollArea()
        self.xSlider = self.createSlider(self.glWidget.xRotationChanged, self.glWidget.setXRotation)
        self.ySlider = self.createSlider(self.glWidget.yRotationChanged, self.glWidget.setYRotation)
        self.zSlider = self.createSlider(self.glWidget.zRotationChanged, self.glWidget.setZRotation)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
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

        self.glWidgetArea.setMinimumSize(50, 50)
        self.glWidgetArea.installEventFilter(self)

        self.xSlider.setValue(15 * 16)
        self.ySlider.setValue(0 * 16)
        self.zSlider.setValue(0 * 16)

        self.pushButton.clicked.connect(self.button_click)

        layout.addWidget(self.textBrowser, 2, 2, 3, 49)
        layout.addWidget(self.pushButton, 2, 52, 3, 8)
        layout.addWidget(self.glWidgetArea, 6, 2, 45, 58)
        layout.addWidget(self.xSlider, 52, 2, 3, 58)
        layout.addWidget(self.ySlider, 55, 2, 3, 58)
        layout.addWidget(self.zSlider, 58, 2, 3, 58)
        self.setLayout(layout)

        self.retranslateUi()
        self.setWindowTitle("neuron system")

    def createSlider(self, changedSignal, setterSlot):
        slider = QSlider(Qt.Horizontal,self)
        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QSlider.TicksRight)

        slider.valueChanged.connect(setterSlot)
        changedSignal.connect(slider.setValue)

        return slider

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("Form", "Browse"))

    def button_click(self):
        dir,type = QFileDialog.getOpenFileName(self,"Browser",'./','All Files (*);;Text Files (*.swc)')
        self.textBrowser.setText(dir)
        dir = split(dir)
        self.glWidget.setpath(dir)
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