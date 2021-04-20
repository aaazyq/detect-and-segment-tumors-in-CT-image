from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication,QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
from PyQt5.QtGui import QIcon,QPixmap,QMovie
import adjust
import fmd
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
matplotlib.use('TkAgg')
from matplotlib import pylab as plt
import threshold
from PIL import Image
from slice import slice
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
class Show3d(QMainWindow):
    def __init__(self):
        super(Show3d, self).__init__()
        self.init_ui()

    def init_ui(self):
        exit3dAct = QAction(QIcon('exit24.png'), 'exit3d act', self)
        exit3dAct.setStatusTip('exit 3d act application')
        exit3dAct.triggered.connect(self.exit3d)  # 3D窗口
        # set 1-menu
        self.statusBar()
        menubar = self.menuBar()

        #self.parent = example()

        # short cut
        toolbar = self.addToolBar('3d')
        toolbar.addAction(exit3dAct)
        centralWidget = QWidget(self)
        # set central widget layout

        vtkWidget = QVTKRenderWindowInteractor()
        ren = fmd.show_3D_simpleITK('C:/Users/zhangke/Desktop/software/mprage_3T_bet_dr.nii')
        vtkWidget.GetRenderWindow().AddRenderer(ren)
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        self.iren.Start()
        self.setCentralWidget(vtkWidget)

        self.setGeometry(300, 100, 1200, 906)
        self.setWindowTitle('Main window')
        self.show()

    def exit3d(self):
        self.hide()
        self.parent.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Show3d()
    ex.show()
    sys.exit(app.exec_())