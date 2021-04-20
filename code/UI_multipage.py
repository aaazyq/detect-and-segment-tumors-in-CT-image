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
import draw_tumour
import Naive3D
import SimpleITK as sitk
import os
from skimage import io,transform
import slice3d

class Example(QMainWindow):
    def __init__(self):
        super(Example,self).__init__()

        self.initUI()

    def initUI(self):

        centralWidget = QWidget(self)

        splash = QSplashScreen(QPixmap('./pic/start.png'))
        splash.show()
        #set 2-menu functions

        #file-save
        self.flag=0
        self.flag_draw=False
        self.maxclick=False
        self.tumor=False
        self.targets=0
        self.targeta= 0
        self.targetc= 0
        self.color='#ffc525'
        global color
        color=self.color

        saveAct = QAction(QIcon('./icon/save2.png'), 'save as nii', self)
        saveAct.setStatusTip('save application')
        saveAct.triggered.connect(self.saveasnii)#function save

        saveAct2 = QAction(QIcon('./icon/save2.png'), 'save as mha', self)
        saveAct2.setStatusTip('save application')
        saveAct2.triggered.connect(self.saveasmha)  # function save

        saveAct3 = QAction(QIcon('./icon/save2.png'), 'save segmentation result', self)
        saveAct3.setStatusTip('saveseg application')
        saveAct3.triggered.connect(self.saveseg)  # function save segmentation

        saveAct4 = QAction(QIcon('./icon/save2.png'), 'Save 3D result', self)
        saveAct4.setStatusTip('Save 3D application')
        saveAct4.triggered.connect(self.save3d)  # function save segmentation

        #file-open
        openAct = QAction(QIcon('./icon/open.png'), 'open', self)
        openAct.setStatusTip('open application')
        openAct.triggered.connect(self.openfiles) #function open

        displayAct = QAction(QIcon('./icon/display.jpg'), 'display', self)
        displayAct.setStatusTip('display application')
        displayAct.triggered.connect(self.display)  # function open

        #edit-contrast
        contrastAct = QAction(QIcon('./icon/edit.png'), 'Contrast', self)
        contrastAct.setStatusTip('contrast application')
        contrastAct.triggered.connect(self.contrast)  # 调节对比度功能接口

        #edit-Brightness
        BrightAct = QAction(QIcon('./icon/edit.png'), 'Brightness', self)
        BrightAct.setStatusTip('Brightness application')
        BrightAct.triggered.connect(self.brightness)# 调节亮度功能接口

        maxmizeAct = QAction(QIcon('./icon/enlarge.png'), 'maxmize', self)
        maxmizeAct.setStatusTip('maxmize application')
        maxmizeAct.triggered.connect(self.maxmize)  # 调节大小功能接口

        resetAct = QAction(QIcon('./icon/reset.png'), 'reset', self)
        resetAct.setStatusTip('reset application')
        resetAct.triggered.connect(self.reset)  # 重置功能接口

        resetsizeAct = QAction(QIcon('./icon/return.png'), 'reset', self)
        resetsizeAct.setStatusTip('reset application')
        resetsizeAct.triggered.connect(self.resetsize)  # 大小重置功能接口

        outlineAct = QAction(QIcon('./icon/outline.png'), 'outline', self)
        outlineAct.setStatusTip('outline application')
        outlineAct.triggered.connect(self.outline)  # 提取边缘功能接口

        thresholdAct = QAction(QIcon('./icon/edit.png'), 'threshold', self)
        thresholdAct.setStatusTip('threshold application')
        thresholdAct.triggered.connect(self.threshold)  # threshold分割肿瘤功能接口

        #segmentation-auto Segmentation
        autosegAct = QAction(QIcon('./icon/cut.png'), 'Auto Segmentation', self)
        autosegAct.setStatusTip('auto segmentation application')
        autosegAct.triggered.connect(self.close)  # 自动分割功能接口

        #segmentation-manual Segmentation
        manualsegAct = QAction(QIcon('./icon/cut.png'), 'Manual Segmentation', self)
        manualsegAct.setStatusTip('Manual segmentation application')
        manualsegAct.triggered.connect(self.manualseg)  # 手动分割功能接口

        segflagAct = QAction(QIcon('./icon/cut.png'), 'Segmentation flag', self)
        segflagAct.setStatusTip('Segmentation flag')
        segflagAct.triggered.connect(self.segflag)

        segcolorAct = QAction(QIcon('./icon/color.jpg'), 'Segmentation color', self)
        segcolorAct.setStatusTip('Segmentation color')
        segcolorAct.triggered.connect(self.segcolor)

        segoutlineAct = QAction(QIcon('./icon/cut.png'), 'Manual segmentation outline', self)
        segoutlineAct.setStatusTip('Manual segmentation outline')
        segoutlineAct.triggered.connect(self.outlinemanualseg)

        activemanualsegAct = QAction(QIcon('./icon/color.jpg'), 'Active Manual segmentation', self)
        activemanualsegAct.setStatusTip('Active Manual segmentation')
        activemanualsegAct .triggered.connect(self.activemanualseg)

        activemanualoutlineAct = QAction(QIcon('./icon/color.jpg'), 'Active Manual segmentation outline', self)
        activemanualoutlineAct.setStatusTip('Active Manual segmentation outline')
        activemanualoutlineAct.triggered.connect(self.activemanualoutline)

        #3D-show
        active3dAct = QAction(QIcon('./icon/3D.png'), 'Active 3D', self)
        active3dAct.setStatusTip('active 3D segmentation application')
        active3dAct.triggered.connect(self.active3d)  # 3D窗口

        Colorful3dAct=QAction(QIcon('./icon/3D.png'), 'Colorful 3D', self)
        Colorful3dAct.setStatusTip('active 3D colorful application')
        Colorful3dAct.triggered.connect(self.colorful3d)  # 3D窗口

        Slicer3dAct = QAction(QIcon('./icon/3D.png'), 'Slicer 3D', self)
        Slicer3dAct.setStatusTip('active 3D Slicer application')
        Slicer3dAct.triggered.connect(self.slicer3d)  # 3D窗口

        # set 1-menu
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        segMenu = menubar.addMenu('&Segmentation')
        active3dMenu = menubar.addMenu('&3D')

        # 2-menu & Icon
        # file
        saveMenu = fileMenu.addMenu("&Save As")
        saveMenu.addAction(saveAct)
        saveMenu.addAction(saveAct2)
        saveMenu.addAction(saveAct3)

        fileMenu.addAction(openAct)
        fileMenu.addAction(displayAct)

        #short cut
        toolbar = self.addToolBar('exit')
        toolbar.addAction(maxmizeAct)
        #toolbar.addAction(saveAct)
        toolbar.addAction(resetAct)
        toolbar.addAction(resetsizeAct)
        toolbar.addAction(segflagAct)
        toolbar.addAction(segcolorAct)

        # edit
        editMenu.addAction(contrastAct)
        editMenu.addAction(BrightAct)
        editMenu.addAction(maxmizeAct)

        # segmentation
        segMenu.addAction(outlineAct)
        segMenu.addAction(autosegAct)
        segMenu.addAction(manualsegAct)
        segMenu.addAction(activemanualsegAct)
        segMenu.addAction(thresholdAct)
        segMenu.addAction(segoutlineAct)
        segMenu.addAction(activemanualoutlineAct)

        # active 3D
        active3dMenu.addAction(active3dAct)
        active3dMenu.addAction(Colorful3dAct)
        active3dMenu.addAction(Slicer3dAct)

        centralWidget = QWidget(self)
        # set central widget layout
        labely = QLabel('y')
        labely.setPixmap(QPixmap.fromImage(QImage('./cover.jpg')))
        grid = QGridLayout()
        grid.addWidget(labely, 0, 0)
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)
        self.setGeometry(300, 100, 1200, 906)
        self.setWindowTitle('Main window')
        self.show()

    def openfiles(self):
        #set files
        self.flag=1
        self.click=0
        imgName, imgType = QFileDialog.getOpenFileName(self, "", "*.mha;;*.nii.gz;;*.nii;;All Files(*)")
        self.name = imgName.split("/")[-1]
        global path
        self.path = imgName
        path=self.path

        plt.cla()
        # 获取绘图并绘制
        self.Coords1s=26
        self.Coords1a=50
        self.Coords1c=30
        self.s=slice.return_S_array(path=imgName, S=self.Coords1s)
        self.a=slice.return_A_array(path=imgName,A=self.Coords1a)
        self.c=slice.return_C_array(path=imgName, C=self.Coords1c)

        plt.style.use('dark_background')
        self.figs, self.axs = plt.subplots()
        self.figa, self.axa = plt.subplots()
        self.figc, self.axc = plt.subplots()
        #self.gif , self.axg= plt.subplots()

        plt.set_cmap("gray")
        self.axs.imshow(Image.fromarray(self.s).convert("L"))
        self.axa.imshow(Image.fromarray(self.a).convert("L"))
        self.axc.imshow(Image.fromarray(self.c).convert("L"))

        cavans = FigureCanvas(self.figs)
        cavana = FigureCanvas(self.figa)
        cavanc = FigureCanvas(self.figc)
        #cavang = FigureCanvas(self.gif)

        self.figs.canvas.mpl_connect('button_press_event', self.OnClicks)
        self.figa.canvas.mpl_connect('button_press_event', self.OnClicka)
        self.figc.canvas.mpl_connect('button_press_event', self.OnClickc)
        #figs.canvas.mpl_connect('motion_notify_event', self.OnMouseMotion)
        self.label_mouse = QLabel(self)
        self.label_mouse.setGeometry(40, 30, 200, 100)
        self.label_mouse.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        self.label_mouse.setStyleSheet("color:#ffc525")
        self.label_mouse.setText('S:' + str(self.Coords1s)+" "+'A:' + str(self.Coords1a)+" "+'C: '+str(self.Coords1c)+" "+'Gray: ' + str(np.round(self.a[self.Coords1s][self.Coords1c],3)))

        #3D Wideget
        vtkWidget = QVTKRenderWindowInteractor()
        ren = fmd.show_3D_simpleITK(self.path)
        vtkWidget.GetRenderWindow().AddRenderer(ren)
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        self.iren.Start()

        # 将绘制好的图像设置为中心 Widget
        # # set central widge4t
        grid = QGridLayout()
        centralWidget = QWidget(self)
        grid.addWidget(self.label_mouse,0,0)
        grid.addWidget(cavans, 1, 0)
        grid.addWidget(cavana, 1, 1)
        grid.addWidget(cavanc, 2, 0)
        grid.addWidget(vtkWidget, 2, 1)
        flag_parent = 0

        self.imgs()
        # def update(i):
        #     if i<self.data.shape[0]:
        #         if i%5==0:
        #             return self.axg.imshow(self.imglist[i])
        #     else:
        #         global flag_parent
        #         flag_parent=1
        # if flag_parent:
        #     self.ani._stop()
        # else:
        #     self.ani=animation.FuncAnimation(self.gif, update,interval=5,repeat=False)

        # grid.addWidget(cavans, 1, 0)
        # self.label=QLabel('gif')
        # self.gif = QMovie('C:/Users/zhangke/Desktop/software/created_gif')
        # self.label.setMovie(self.gif)
        # grid.addWidget(self.label, 2, 1)
        # self.gif.start()
        grid.setContentsMargins(0, 0, 0, 0)
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)

    def saveasnii(self):
        # set files
        if self.flag:
            directory1 = QFileDialog.getExistingDirectory(self, "请选择文件夹", "/")

            image = sitk.ReadImage(self.path)
            name = self.path.split("/")[-1]
            name = name.split(".")[0]
            print(name)
            sitk.WriteImage(image, os.path.join(directory1, name + ".nii"))
        else:
            QMessageBox.information(self, "提示！", "请先打开文件(σﾟ∀ﾟ)σ")

    def saveasmha(self):
        if self.flag:
            # set files
            directory1 = QFileDialog.getExistingDirectory(self, "请选择文件夹", "/")
            image = sitk.ReadImage(self.path)
            name = self.path.split("/")[-1]
            name = name.split(".")[0]
            print(name)
            sitk.WriteImage(image, os.path.join(directory1, name + ".mha"))
        else:
            QMessageBox.information(self, "提示！", "请先打开文件(σﾟ∀ﾟ)σ")

    def saveseg(self):
        if self.tumor:
            directory2 = QFileDialog.getExistingDirectory(self, "请选择文件夹", "/")
            data_labeled = slice.read_img(path)
            data_labeled[data_labeled > min(tumor_range)] = 255
            img = sitk.GetImageFromArray(data_labeled)
            sitk.WriteImage(img, os.path.join(directory2, "segmentation_result" + ".mha"))
        else:
            QMessageBox.information(self, "提示！", "请先手动分割(σﾟ∀ﾟ)σ")

    def save3d(self):
        if self.tumor:
            directory2 = QFileDialog.getExistingDirectory(self, "请选择文件夹", "/")
            data_labeled = slice.read_img(path)
            data_labeled[data_labeled > min(tumor_range)] = 255
            img = sitk.GetImageFromArray(data_labeled)
            sitk.WriteImage(img, os.path.join(directory2, self.name + ".mha"))
        else:
            QMessageBox.information(self, "提示！", "请先手动分割(σﾟ∀ﾟ)σ")


    def imgs(self):
        self.data = slice.read_img(self.path)
        self.imglist = []
        for i in range(self.data.shape[0]):
            self.imglist.append(self.data[i, :, :])

    def replots(self):
        try:
            self.axs.cla()
            print("S:", self.Coords1s)
            self.s = slice.return_S_array(path=self.path, S=self.Coords1s)
            self.imgs = Image.fromarray(self.s).convert("L")
            self.axs.imshow(self.imgs)
            self.axs.figure.canvas.draw()
        except IndexError:
            pass

    def replota(self):
        try:
            self.axa.cla()
            print("A: ", self.Coords1a)
            self.a = slice.return_A_array(path=self.path, A=self.Coords1a)
            self.imga = Image.fromarray(self.a).convert("L")
            self.axa.imshow(self.imga)
            self.axa.figure.canvas.draw()
        except IndexError:
            pass

    def replotc(self):
        try:
            self.axc.cla()
            print("C:", self.Coords1c)
            self.c = slice.return_C_array(path=self.path, C=self.Coords1c)
            self.imgc = Image.fromarray(self.c).convert("L")
            self.axc.imshow(self.imgc)
            self.axc.figure.canvas.draw()
        except IndexError:
            pass


    def OnClicks(self,event):
        if self.flag_draw:
            try:
                self.paintpointa = int(event.xdata)
                self.paintpointc = int(event.ydata)
            except TypeError:
                pass
            try:
                self.targets=self.s[self.paintpointa][self.paintpointc]
            except IndexError:
                pass
            self.label_mouse.setText('S:' + str(self.Coords1s) + " " + 'A:' + str(self.paintpointa) + " " + 'C: ' + str(
                self.paintpointc) + " " + 'Gray: ' + str(round(self.targets, 5)))
            point = self.axs.scatter(self.paintpointa, self.paintpointc, c=self.color)
            self.axs.figure.canvas.draw()
            # point.set_visible(False)
        else:
            try:
                self.Coords1a = int(event.xdata)
                self.Coords1c = int(event.ydata)
                self.click = 1
            except TypeError:
                pass
            try:
                self.label_mouse.setText('S:' + str(self.Coords1s) + " " + 'A:' + str(self.Coords1a) + " " + 'C: ' + str(
                    self.Coords1c) + " " + 'Gray: ' + str(round(self.a[self.Coords1s][self.Coords1c], 5)))
            except IndexError:
                pass
            try:
                print("gray:", str(np.round(self.a[self.Coords1s][self.Coords1c], 5)))
            except IndexError:
                pass
            point = self.axs.scatter(self.Coords1a, self.Coords1c, c="#ffc525")
            vline = self.axs.vlines(self.Coords1a, 0, self.Coords1c, colors="#ffc525", linestyles="dashed")
            hline = self.axs.hlines(self.Coords1c, 0, self.Coords1a, colors="#ffc525", linestyles="dashed")
            self.axs.figure.canvas.draw()
            vline.set_visible(False)
            hline.set_visible(False)
            point.set_visible(False)
            self.replota()
            self.replotc()

    def OnClicka(self,event):
        if self.flag_draw:
            try:
                self.paintpoints = int(event.xdata)
                self.paintpointc = int(event.ydata)
            except TypeError:
                pass
            try:
                self.targeta = self.a[self.paintpoints][self.paintpointc]
            except IndexError:
                pass
            try:
                self.label_mouse.setText('S:' + str(self.paintpoints) + " " + 'A:' + str(self.Coords1a) + " " + 'C: ' + str(
                    self.paintpointc) + " " + 'Gray: ' + str(round(self.targeta, 5)))
            except IndexError:
                pass
            point = self.axa.scatter(self.paintpoints, self.paintpointc, c=self.color)
            self.axa.figure.canvas.draw()
            # point.set_visible(False)
        else:
            try:
                self.Coords1s = int(event.xdata)
                self.Coords1c = int(event.ydata)
                self.click = 1
            except TypeError:
                pass
            try:
                self.label_mouse.setText('S:' + str(self.Coords1s) + " " + 'A:' + str(self.Coords1a) + " " + 'C: ' + str(
                    self.Coords1c) + " " + 'Gray: ' + str(np.round(self.a[self.Coords1s][self.Coords1c], 5)))
            except IndexError:
                pass
            point = self.axa.scatter(self.Coords1s, self.Coords1c, c="#ffc525")
            vline = self.axa.vlines(self.Coords1s, 0, self.Coords1c, colors="#ffc525", linestyles="dashed")
            hline = self.axa.hlines(self.Coords1c, 0, self.Coords1s, colors="#ffc525", linestyles="dashed")
            self.axa.figure.canvas.draw()
            vline.set_visible(False)
            hline.set_visible(False)
            point.set_visible(False)
            self.replots()
            self.replotc()

    def OnClickc(self,event):
        if self.flag_draw:
            try:
                self.paintpoints = int(event.xdata)
                self.paintpointa = int(event.ydata)
            except TypeError:
                pass
            try:
                self.targetc = self.c[self.paintpoints][self.paintpointa]
            except IndexError:
                pass
            try:
                self.label_mouse.setText('S:' + str(self.paintpoints) + " " + 'A:' + str(self.paintpointa) + " " + 'C: ' + str(
                    self.Coords1c) + " " + 'Gray: ' + str(round(self.targetc, 5)))
            except IndexError:
                pass
            point = self.axc.scatter(self.paintpoints, self.paintpointa, c=self.color)
            self.axc.figure.canvas.draw()
            # point.set_visible(False)
        else:
            try:
                self.Coords1s = int(event.xdata)
                self.Coords1a = int(event.ydata)
                self.click = 1
                try:
                    self.label_mouse.setText(
                        'S:' + str(self.Coords1s) + " " + 'A:' + str(self.Coords1a) + " " + 'C: ' + str(
                            self.Coords1c) + " " + 'Gray: ' + str(np.round(self.a[self.Coords1s][self.Coords1c], 5)))
                except IndexError:
                    pass
                point = self.axc.scatter(self.Coords1s, self.Coords1a, c="#ffc525")
                vline = self.axc.vlines(self.Coords1s, 0, self.Coords1a, colors="#ffc525", linestyles="dashed")
                hline = self.axc.hlines(self.Coords1a, 0, self.Coords1s, colors="#ffc525", linestyles="dashed")
                self.axc.figure.canvas.draw()
                vline.set_visible(False)
                hline.set_visible(False)
                point.set_visible(False)
                self.replota()
                self.replots()
            except TypeError:
                pass

    def OnMouseMotion(self,event):
        global x1, y1
        self.Coords2x = event.xdata
        self.Coords2y = event.ydata
        if self.click==1:
            x1 = [self.Coords1x, self.Coords2x]
            y1 = [self.Coords1y, self.Coords2y]
            lines = self.axs.plot(x1, y1, picker=20)
            self.axs.figure.canvas.draw()  # 删除之前的线条，进行更新
            l = lines.pop(0)
            l.remove()
            del l

    def brightness(self):
        brightness, ok = QInputDialog().getDouble(self, "设置亮度", "输入亮度")
        if ok:
            print(brightness)
            self.a= adjust.adjust.bright(self.a, brightness)
            self.axa.cla()
            self.axa.imshow(self.a)
            self.axa.figure.canvas.draw()
            self.s = adjust.adjust.bright(self.s, brightness)
            self.axs.cla()
            self.axs.imshow(self.s)
            self.axs.figure.canvas.draw()
            self.c = adjust.adjust.bright(self.c, brightness)
            self.axc.cla()
            self.axc.imshow(self.c)
            self.axc.figure.canvas.draw()

    def contrast(self):
        contrast, ok = QInputDialog().getDouble(self, "设置对比度", "输入对比度")
        if ok:
            contrast=1/contrast
            print(contrast)
            self.a= adjust.adjust.contrast(self.a, contrast)
            self.axa.cla()
            self.axa.imshow(self.a)
            self.axa.figure.canvas.draw()
            self.s = adjust.adjust.contrast(self.s, contrast)
            self.axs.cla()
            self.axs.imshow(self.s)
            self.axs.figure.canvas.draw()
            self.c = adjust.adjust.contrast(self.c, contrast)
            self.axc.cla()
            self.axc.imshow(self.c)
            self.axc.figure.canvas.draw()

    def reset(self):
        self.gif, self.axg = plt.subplots()
        self.figs, self.axs = plt.subplots()
        self.figa, self.axa = plt.subplots()
        self.figc, self.axc = plt.subplots()
        plt.set_cmap("gray")
        self.axs.imshow(self.s)
        self.axa.imshow(self.a)
        self.axc.imshow(self.c)
        cavans = FigureCanvas(self.figs)
        cavana = FigureCanvas(self.figa)
        cavanc = FigureCanvas(self.figc)
        cavang = FigureCanvas(self.gif)
        self.figs.canvas.mpl_connect('button_press_event', self.OnClicks)
        self.figa.canvas.mpl_connect('button_press_event', self.OnClicka)
        self.figc.canvas.mpl_connect('button_press_event', self.OnClickc)
        # figs.canvas.mpl_connect('motion_notify_event', self.OnMouseMotion)
        self.label_mouse = QLabel(self)
        self.label_mouse.setGeometry(40, 30, 200, 100)
        self.label_mouse.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        self.label_mouse.setStyleSheet("color:#ffc525")
        try:
            self.label_mouse.setText('S:' + str(self.Coords1s) + " " + 'A:' + str(self.Coords1a) + " " + 'C: ' + str(
                self.Coords1c) + " " + 'Gray: ' + str(np.round(self.a[self.Coords1s][self.Coords1c], 3)))
        except IndexError:
            pass
        grid = QGridLayout()
        centralWidget = QWidget(self)
        grid.addWidget(self.label_mouse, 0, 0)
        grid.addWidget(cavans, 1, 0)
        grid.addWidget(cavana, 1, 1)
        grid.addWidget(cavanc, 2, 0)
        grid.addWidget(cavang, 2, 1)
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)
        i = [i for i in range(self.data.shape[0]) if i % 5 == 0]
        def update(i):
            return self.axg.imshow(self.imglist[i])
        self.ani = animation.FuncAnimation(self.gif, update, interval=30, repeat=True)

    def resetsize(self):
        self.replota()
        self.replotc()
        self.replots()

    def maxmize(self):
        self.s = adjust.adjust.enlarge(self.Coords1a, self.Coords1c, self.s, 1.5)
        self.a = adjust.adjust.enlarge(self.Coords1s, self.Coords1c, self.a, 1.5)
        self.c = adjust.adjust.enlarge(self.Coords1s, self.Coords1a, self.c, 1.5)
        self.axa.cla()
        self.axa.imshow(self.a)
        self.axa.figure.canvas.draw()
        self.axs.cla()
        self.axs.imshow(self.s)
        self.axs.figure.canvas.draw()
        self.axc.cla()
        self.axc.imshow(self.c)
        self.axc.figure.canvas.draw()

    def outline(self):
        self.s = threshold.outline(self.s)
        self.a = threshold.outline(self.a)
        self.c = threshold.outline(self.c)
        self.axa.cla()
        self.axa.imshow(self.a)
        self.axa.figure.canvas.draw()
        self.axs.cla()
        self.axs.imshow(self.s)
        self.axs.figure.canvas.draw()
        self.axc.cla()
        self.axc.imshow(self.c)
        self.axc.figure.canvas.draw()

    def threshold(self):
        graya=self.a[self.Coords1s][self.Coords1c]
        tmpa = threshold.threshold(self.a,graya,choice="TOZERO")
        self.axa.cla()
        self.axa.imshow(tmpa,cmap="gray")
        self.axa.figure.canvas.draw()
        tmps = threshold.threshold(self.s, graya, choice="TOZERO")
        self.axs.cla()
        self.axs.imshow(tmps, cmap="gray")
        self.axs.figure.canvas.draw()
        tmpc = threshold.threshold(self.c, graya, choice="TOZERO")
        self.axc.cla()
        self.axc.imshow(tmpc, cmap="gray")
        self.axc.figure.canvas.draw()

    def segcolor(self):
        c = QColorDialog.getColor()
        self.color = c.name()
        global color
        color = self.color
        print("color:",color)

    def manualseg(self):
        if max([self.targets, self.targeta, self.targetc])>0:
            self.flag_draw=True
            self.manualsegthresh,ok = QInputDialog().getDouble(self, "设置手动分割阈值", "输入阈值")
            if ok:
                global tumor_range
                tumor_range = [max([self.targets, self.targeta, self.targetc]) - self.manualsegthresh,
                               max([self.targets, self.targeta, self.targetc]) + self.manualsegthresh]
                self.tumor = True
                print("targets:",self.targets,"targeta:",self.targeta,"targetc:",self.targetc)
                if self.targets:
                    print(self.targets)
                    self.manualseg_scatters()
                if self.targeta:
                    print(self.targeta)
                    self.manualseg_scattera()
                if self.targetc:
                    print(self.targetc)
                    self.manualseg_scatterc()
        else:
            QMessageBox.information(self, "提示！", "请先做手动分割标注(σﾟ∀ﾟ)σ")

    def manualseg_scatters(self):
        self.replots()
        nrows = self.s.shape[0]
        ncols = self.s.shape[1]
        x_scatters = []
        y_scatters = []
        for x in range(nrows):
            for y in range(ncols):
                if abs(self.s[x][y] - max([self.targets,self.targeta,self.targetc]))<self.manualsegthresh:
                    x_scatters.append(y)
                    y_scatters.append(x)
        self.axs.scatter(x_scatters, y_scatters, c=self.color,s=1)
        self.axs.figure.canvas.draw()
        # point.set_visible(False)

    def manualseg_scattera(self):
        self.replota()
        nrowa = self.a.shape[0]
        ncola = self.a.shape[1]
        x_scattera = []
        y_scattera = []
        for x in range(nrowa):
            for y in range(ncola):
                if abs(self.a[x][y] - max([self.targets,self.targeta,self.targetc])) < self.manualsegthresh:
                    x_scattera.append(y)
                    y_scattera.append(x)
        self.axa.scatter(x_scattera, y_scattera, c=self.color,s=1)
        self.axa.figure.canvas.draw()
        # point.set_visible(False)

    def manualseg_scatterc(self):
        self.replotc()
        nrowc = self.c.shape[0]
        ncolc = self.c.shape[1]
        x_scatterc = []
        y_scatterc = []
        for x in range(nrowc):
            for y in range(ncolc):
                if abs(self.c[x][y] - max([self.targets,self.targeta,self.targetc])) <self.manualsegthresh:
                    x_scatterc.append(y)
                    y_scatterc.append(x)
        self.axc.scatter(x_scatterc, y_scatterc, c=self.color,s=1)
        self.axc.figure.canvas.draw()
        # point.set_visible(False)

    def segflag(self):
        if self.flag_draw:
            self.flag_draw=False
            QMessageBox.information(self, "提示！", "即将切换到三维视图(=￣ω￣=)")
        else:
            self.flag_draw = True
            QMessageBox.information(self, "提示！", "即将切换到手动分割标注模式(✪ω✪)")

    def activemanualseg(self):
        self.data = slice.read_img(self.path)
        self.imglist = []

        for i in range(self.data.shape[0]):
            self.imglist.append(self.data[i, :, :])

        targets=[i for i in [self.targetc,self.targeta,self.targets] if i]
        print(targets)

        if min(targets)>0:
            # global tumor_range
            # tumor_range=[max([self.targets,self.targeta,self.targetc])-self.manualsegthresh,max([self.targets,self.targeta,self.targetc])+self.manualsegthresh]
            # self.tumor=True
            # print("Tumor range:",tumor_range)
            #self.data_label()
            if self.flag:
                self.manualsegresult = Manualseg_result()
                self.manualsegresult.show()
            else:
                QMessageBox.information(self, "提示！", "先选择要打开的文件吧(〃'▽'〃)")

    def activemanualoutline(self):
        if self.flag:
            self.manualsegoutline = Manualseg_outline()
            self.manualsegoutline.show()
        else:
            QMessageBox.information(self, "提示！", "先选择要打开的文件吧(〃'▽'〃)")



    def outlinemanualseg(self):
        if self.tumor:
            print("ok")
            print(tumor_range)
            #self.data_outline = slice.read_img(path)
            # self.data_outline[self.data_outline < max(tumor_range)] = 0
            # self.data_outline[self.data_outline > max(tumor_range)] = 255
            plt.set_cmap("gray")

            self.tmps = self.s.copy()
            self.tmpa = self.a.copy()
            self.tmpc = self.c.copy()

            self.tmps[self.tmps > min(tumor_range)] = 255
            self.tmpa[self.tmpa > min(tumor_range)] = 255
            self.tmpc[self.tmpc > min(tumor_range)] = 255

            self.tmps[self.tmps < min(tumor_range)] = 0
            self.tmpa[self.tmpa < min(tumor_range)] = 0
            self.tmpc[self.tmpc < min(tumor_range)] = 0

            self.tmps = threshold.outline(self.tmps)
            self.tmpa = threshold.outline(self.tmpa)
            self.tmpc = threshold.outline(self.tmpc)

            self.outline_scatters()
            self.outline_scattera()
            self.outline_scatterc()
        else:
            QMessageBox.information(self, "提示！", "需要先做手动分割标注哦(^_−)☆")

    def outline_scatters(self):
        self.replots()
        nrows = self.tmps.shape[0]
        ncols = self.tmps.shape[1]
        x_scatters = []
        y_scatters = []
        for x in range(nrows):
            for y in range(ncols):
                if self.tmps[x][y] >120:
                    x_scatters.append(y)
                    y_scatters.append(x)
        self.axs.scatter(x_scatters, y_scatters, c=self.color,s=0.1)
        self.axs.figure.canvas.draw()
        # point.set_visible(False)

    def outline_scattera(self):
        self.replota()
        nrowa = self.tmpa.shape[0]
        ncola = self.tmpa.shape[1]
        x_scattera = []
        y_scattera = []
        for x in range(nrowa):
            for y in range(ncola):
                if self.tmpa[x][y] > 120:
                    x_scattera.append(y)
                    y_scattera.append(x)
        self.axa.scatter(x_scattera, y_scattera, c=self.color,s=0.1)
        self.axa.figure.canvas.draw()
        # point.set_visible(False)

    def outline_scatterc(self):
        self.replotc()
        nrowc = self.tmpc.shape[0]
        ncolc = self.tmpc.shape[1]
        x_scatterc = []
        y_scatterc = []
        for x in range(nrowc):
            for y in range(ncolc):
                if self.tmpc[x][y] >120:
                    x_scatterc.append(y)
                    y_scatterc.append(x)
        self.axc.scatter(x_scatterc, y_scatterc, c=self.color,s=0.1)
        self.axc.figure.canvas.draw()
        # point.set_visible(False)


    def data_label(self):
        global data_labeled
        data_labeled = slice.read_img(path)
        data_labeled[data_labeled < min(tumor_range)] = 0
        data_labeled[data_labeled > min(tumor_range)] = 255
        f=open("data_labeled.txt","a+",encoding="utf-8")
        for x in range(data_labeled.shape[0]):
            for y in range(data_labeled.shape[1]):
                for z in range(data_labeled.shape[2]):
                    f.write(str(x)+","+str(y)+","+str(z)+","+str(data_labeled[x,y,z])+"\n")


    def active3d(self):
        if self.flag:
            self.show3dcolor=Color_config()
            self.show3dcolor.show()
        else:
            print("Open file first!")

    def slicer3d(self):
        if self.flag:
            self.sliders=Slider_config()
            self.sliders.show()
        else:
            QMessageBox.information(self, "提示！", "先选择要打开的文件吧(〃'▽'〃)")

    def display(self):
        if self.flag:
            self.figuredisplay=Figure_display()
            self.figuredisplay.show()
        else:
            QMessageBox.information(self, "提示！", "先选择要打开的文件吧(〃'▽'〃)")

    def colorful3d(self):
        if self.flag:
            self.colorful=Colorful3d()
            self.colorful.show()
        else:
            QMessageBox.information(self, "提示！", "先选择要打开的文件吧(〃'▽'〃)")


class Manualseg_result(QMainWindow):
    def __init__(self):
        super(Manualseg_result, self).__init__()
        self.init_ui()

    def init_ui(self):
        plt.style.use('dark_background')
        self.gif_original, self.axg_original = plt.subplots()
        self.gif_seg, self.axg_seg = plt.subplots()
        #plt.set_cmap("gray")
        print(path)
        self.data = slice.read_img(path)

        self.imglist = []
        for i in range(self.data.shape[2]):
            self.imglist.append(self.data[:, :, i])

        self.axg_original.imshow(self.imglist[100])
        # self.axg_seg.imshow(self.imglist[100])

        cavang_original = FigureCanvas(self.gif_original)
        cavang_seg = FigureCanvas(self.gif_seg)

        # 将绘制好的图像设置为中心 Widget
        grid = QGridLayout()
        centralWidget = QWidget(self)
        grid.addWidget(cavang_original, 0, 0)
        grid.addWidget(cavang_seg, 0, 1)
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)
        self.setGeometry(300, 100, 1200, 906)
        self.setWindowTitle('Manual segmentation result')
        self.show()

        i = [i for i in range(self.data.shape[2]) if i % 10 == 0]

        # def update_original(i):
        #     return self.axg_original.imshow(self.imglist[i])
        #self.ani = animation.FuncAnimation(self.gif_original, update_original, interval=30, repeat=True)
        self.tumor_range = tumor_range
        print(self.tumor_range)
        global data_labeled
        data_labeled = slice.read_img(path)
        data_labeled[data_labeled<min(tumor_range)]=0
        data_labeled[data_labeled > min(tumor_range)]=255
        print(data_labeled.shape)

        flag=0

        def update_seg(i):
            if i<self.data.shape[2]:
                self.axg_seg.cla()
                self.axg_seg.imshow(Image.fromarray(self.imglist[i]).convert("L"))
                nrow = self.imglist[i].shape[0]
                ncol = self.imglist[i].shape[1]
                x_scatter = []
                y_scatter = []
                for x in range(nrow):
                    for y in range(ncol):
                        if self.imglist[i][x][y] < max(self.tumor_range):
                            if self.imglist[i][x][y] > min(self.tumor_range):
                                x_scatter.append(y)
                                y_scatter.append(x)
                self.axg_seg.scatter(x_scatter, y_scatter, c=color, s=1)
            else:
                global flag
                flag=1
        if flag:
            self.ani_seg._stop()
        else:
            self.ani_seg=animation.FuncAnimation(self.gif_seg, update_seg, interval=30, repeat=True)
            #self.ani_seg.save("seg_fill.gif")


class Manualseg_outline(QMainWindow):
    def __init__(self):
        super(Manualseg_outline, self).__init__()
        self.init_ui()

    def init_ui(self):
        plt.style.use('dark_background')
        self.gif_original, self.axg_original = plt.subplots()
        self.gif_seg, self.axg_seg = plt.subplots()
        #plt.set_cmap("gray")
        print(path)
        self.data = slice.read_img(path)

        self.imglist = []
        for i in range(self.data.shape[2]):
            self.imglist.append(self.data[:, :, i])

        self.axg_original.imshow(self.imglist[100])
        # self.axg_seg.imshow(self.imglist[100])

        cavang_original = FigureCanvas(self.gif_original)
        cavang_seg = FigureCanvas(self.gif_seg)

        # 将绘制好的图像设置为中心 Widget
        grid = QGridLayout()
        centralWidget = QWidget(self)
        grid.addWidget(cavang_original, 0, 0)
        grid.addWidget(cavang_seg, 0, 1)
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)
        self.setGeometry(300, 100, 1200, 906)
        self.setWindowTitle('Manual segmentation outline result')
        self.show()

        i = [i for i in range(self.data.shape[2]) if i % 10 == 0]

        # def update_original(i):
        #     return self.axg_original.imshow(self.imglist[i])
        #self.ani = animation.FuncAnimation(self.gif_original, update_original, interval=30, repeat=True)

        self.tumor_range = tumor_range
        print(self.tumor_range)
        global data_labeled
        data_labeled = slice.read_img(path)
        data_labeled[data_labeled<min(tumor_range)]=0
        data_labeled[data_labeled > min(tumor_range)]=255
        print(data_labeled.shape)

        flag=0

        def update_seg(i):
            if i<self.data.shape[2]:
                self.axg_seg.cla()
                self.axg_seg.imshow(Image.fromarray(self.imglist[i]).convert("L"))
                nrow = self.imglist[i].shape[0]
                ncol = self.imglist[i].shape[1]
                x_scatter = []
                y_scatter = []
                self.tmp = self.imglist[i].copy()
                self.tmp[self.tmp > min(tumor_range)] = 255
                self.tmp[self.tmp < min(tumor_range)] = 0
                self.tmp = threshold.outline(self.tmp)
                for x in range(nrow):
                    for y in range(ncol):
                        if self.tmp[x][y] >120:
                                x_scatter.append(y)
                                y_scatter.append(x)
                self.axg_seg.scatter(x_scatter, y_scatter, c=color,s=0.1)
            else:
                global flag
                flag=1
        if flag:
            self.ani_seg._stop()
        else:
            self.ani_seg=animation.FuncAnimation(self.gif_seg, update_seg, interval=30, repeat=True)
            #self.ani_seg.save("seg_outline.gif")

class Show3d(QMainWindow):
    def __init__(self):
        super(Show3d, self).__init__()
        self.init_ui()

    def init_ui(self):
        #input
        brain_path=path
        tumour_points=[]
        data_labeled = slice.read_img(path)
        data_labeled[data_labeled < min(tumor_range)] = 0
        data_labeled[data_labeled > min(tumor_range)] = 255
        for x in range(data_labeled.shape[0]):
            for y in range(data_labeled.shape[1]):
                for z in range(data_labeled.shape[2]):
                    if data_labeled[x,y,z]==255:
                        tumour_points.append([x,y,z])
        choice, ok = QInputDialog().getText(self, "保存选项", "是否保存分割结果(yes/no)？")
        if choice=="yes":
            directory = QFileDialog.getExistingDirectory(self, "请选择文件夹", "/")
        else:
            directory=None

        brain_coulor = self.get_color_list(global_color, global_alpha)
        tumour_colour = self.get_color_list(tumor_color, tumor_alpha)

        vtkWidget = QVTKRenderWindowInteractor()
        ren = draw_tumour.draw_tumour(brain_path, tumour_points, brain_coulor, tumour_colour,directory)
        vtkWidget.GetRenderWindow().AddRenderer(ren)

        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        self.iren.Start()
        self.setCentralWidget(vtkWidget)

        self.setGeometry(300, 100, 1200, 906)
        self.setWindowTitle('3D window')
        self.show()

    def get_color_list(self, hexcolor, alpha):
        hexcolor = hexcolor.strip('#')
        num_16 = int(hexcolor, 16)
        alpha = float(alpha)
        color_list = [round(((num_16 >> 16) & 0xff) / 255, 3),
                      round(((num_16 >> 8) & 0xff) / 255, 3),
                      round((num_16 & 0xff) / 255, 3), alpha]
        print("color_list:",color_list)
        return color_list

class Colorful3d(QMainWindow):
    def __init__(self):
        super(Colorful3d, self).__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()

        vtkWidget_tough= QVTKRenderWindowInteractor()
        ren_tough = Naive3D.show_brain_tumour_rough(path)
        vtkWidget_tough.GetRenderWindow().AddRenderer(ren_tough)

        self.iren_tough = vtkWidget_tough.GetRenderWindow().GetInteractor()
        self.iren_tough.Initialize()
        self.iren_tough.Start()

        vtkWidget_brain = QVTKRenderWindowInteractor()
        ren_brain = Naive3D.show_3D_brain(path)
        vtkWidget_brain.GetRenderWindow().AddRenderer(ren_brain)

        self.iren_brain = vtkWidget_brain.GetRenderWindow().GetInteractor()
        self.iren_brain.Initialize()
        self.iren_brain.Start()

        grid.addWidget(vtkWidget_tough,0,0)
        grid.addWidget(vtkWidget_brain,0,1)

        centralWidget = QWidget(self)
        centralWidget.setLayout(grid)

        self.setCentralWidget(centralWidget)

        self.setGeometry(300, 100, 1200, 906)
        self.setWindowTitle('Colorful 3D window')
        self.show()

class Figure_display(QMainWindow):

    def __init__(self):
        super(Figure_display, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.fig0,self.ax0=plt.subplots()
        self.fig1, self.ax1 = plt.subplots()
        self.fig2, self.ax2 = plt.subplots()
        self.fig3, self.ax3 = plt.subplots()
        self.fig4, self.ax4 = plt.subplots()
        self.fig5, self.ax5 = plt.subplots()
        self.fig6, self.ax6 = plt.subplots()
        self.fig7, self.ax7 = plt.subplots()
        self.fig8, self.ax8 = plt.subplots()
        self.fig9, self.ax9 = plt.subplots()
        self.fig10, self.ax10 = plt.subplots()
        self.fig11, self.ax11 = plt.subplots()

        plt.set_cmap("gray")
        self.data = slice.read_img(path)
        imgs=[]
        d, ok = QInputDialog().getDouble(self, "设置维度(0,1,2)", "输入维度")
        d=int(d)
        if ok:
            if d<3:
                if d == 0:
                    for i in range(self.data.shape[d]):
                        if i % 10 == 0:
                            if i > 30:
                                if len(imgs) < 13:
                                    imgs.append(self.data[i, :, :])
                if d == 1:
                    for i in range(self.data.shape[d]):
                        if i % 10 == 0:
                            if i>30:
                                if len(imgs) < 13:
                                    imgs.append(self.data[:, i, :])
                if d == 2:
                    for i in range(self.data.shape[d]):
                        if i % 10 == 0:
                            if i>30:
                                if len(imgs) < 13:
                                    imgs.append(self.data[:, :, i])
                print(len(imgs))
                self.ax0.imshow(imgs[0])
                self.ax1.imshow(imgs[1])
                self.ax2.imshow(imgs[2])
                self.ax3.imshow(imgs[3])
                self.ax4.imshow(imgs[4])
                self.ax5.imshow(imgs[5])
                self.ax6.imshow(imgs[6])
                self.ax7.imshow(imgs[7])
                self.ax8.imshow(imgs[8])
                self.ax9.imshow(imgs[9])
                self.ax10.imshow(imgs[10])
                self.ax11.imshow(imgs[11])

                cavan0 = FigureCanvas(self.fig0)
                cavan1 = FigureCanvas(self.fig1)
                cavan2 = FigureCanvas(self.fig2)
                cavan3 = FigureCanvas(self.fig3)
                cavan4 = FigureCanvas(self.fig4)
                cavan5 = FigureCanvas(self.fig5)
                cavan6 = FigureCanvas(self.fig6)
                cavan7 = FigureCanvas(self.fig7)
                cavan8 = FigureCanvas(self.fig8)
                cavan9 = FigureCanvas(self.fig9)
                cavan10 = FigureCanvas(self.fig10)
                cavan11 = FigureCanvas(self.fig11)

                grid = QGridLayout()
                centralWidget = QWidget(self)
                grid.addWidget(cavan0, 0, 0)
                grid.addWidget(cavan1, 0, 1)
                grid.addWidget(cavan2, 0, 2)
                grid.addWidget(cavan3, 0, 3)
                grid.addWidget(cavan4, 1, 0)
                grid.addWidget(cavan5, 1, 1)
                grid.addWidget(cavan6, 1, 2)
                grid.addWidget(cavan7, 1, 3)
                grid.addWidget(cavan8, 2, 0)
                grid.addWidget(cavan9, 2, 1)
                grid.addWidget(cavan10, 2, 2)
                grid.addWidget(cavan11, 2, 3)
                centralWidget.setLayout(grid)
                self.setCentralWidget(centralWidget)
                self.setGeometry(300, 100, 1200, 906)
                self.setWindowTitle('Section display window')
                self.show()
            else:
                QMessageBox.information(self,"提示！","请输入0,1,2中的一个哦(*^▽^*)")

class Slider_config(QMainWindow):

    def __init__(self,parent=None):

        super(QMainWindow, self).__init__(parent)

        centralWidget = QWidget(self)
        grid = QGridLayout()

        self.label_smin= QLabel()
        self.label_smin.setText("S面最小值：")
        self.label_smin.setFont(QFont("Microsoft YaHei"))
        self.label_smax = QLabel()
        self.label_smax.setText("S面最大值：")
        self.label_smax.setFont(QFont("Microsoft YaHei"))

        self.label_amin = QLabel()
        self.label_amin.setText("A面最小值：")
        self.label_amin.setFont(QFont("Microsoft YaHei"))
        self.label_amax = QLabel()
        self.label_amax.setText("A面最大值：")
        self.label_amax.setFont(QFont("Microsoft YaHei"))

        self.label_cmin = QLabel()
        self.label_cmin.setText("C面最小值：")
        self.label_cmin.setFont(QFont("Microsoft YaHei"))
        self.label_cmax = QLabel()
        self.label_cmax.setText("C面最大值：")
        self.label_cmax.setFont(QFont("Microsoft YaHei"))

        # self.label=QLabel()
        # self.label.setFont(QFont(None,20))

        self.splider_smin=QSlider(Qt.Horizontal)
        self.splider_smin.setMinimum(0)#最小值
        self.splider_smin.setMaximum(160)#最大值
        self.splider_smin.setSingleStep(10)#步长
        self.splider_smin.setTickPosition(QSlider.TicksBelow)#设置刻度位置，在下方
        self.splider_smin.setTickInterval(5)#设置刻度间隔

        self.splider_smax = QSlider(Qt.Horizontal)
        self.splider_smax.setMinimum(0)  # 最小值
        self.splider_smax.setMaximum(160)  # 最大值
        self.splider_smax.setSingleStep(10)  # 步长
        self.splider_smax.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.splider_smax.setTickInterval(5)  # 设置刻度间隔

        self.splider_amin = QSlider(Qt.Horizontal)
        self.splider_amin.setMinimum(0)  # 最小值
        self.splider_amin.setMaximum(216)  # 最大值
        self.splider_amin.setSingleStep(10)  # 步长
        self.splider_amin.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.splider_amin.setTickInterval(5)  # 设置刻度间隔

        self.splider_amax = QSlider(Qt.Horizontal)
        self.splider_amax.setMinimum(0)  # 最小值
        self.splider_amax.setMaximum(216)  # 最大值
        self.splider_amax.setSingleStep(10)  # 步长
        self.splider_amax.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.splider_amax.setTickInterval(5)  # 设置刻度间隔

        self.splider_cmin = QSlider(Qt.Horizontal)
        self.splider_cmin.setMinimum(0)  # 最小值
        self.splider_cmin.setMaximum(216)  # 最大值
        self.splider_cmin.setSingleStep(10)  # 步长
        self.splider_cmin.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.splider_cmin.setTickInterval(5)  # 设置刻度间隔

        self.splider_cmax = QSlider(Qt.Horizontal)
        self.splider_cmax.setMinimum(0)  # 最小值
        self.splider_cmax.setMaximum(176)  # 最大值
        self.splider_cmax.setSingleStep(10)  # 步长
        self.splider_cmax.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.splider_cmax.setTickInterval(5)  # 设置刻度间隔

        grid.addWidget(self.label_smin, 0, 0)
        grid.addWidget(self.label_smax, 0, 1)

        grid.addWidget(self.splider_smin, 1, 0)
        grid.addWidget(self.splider_smax, 1, 1)

        grid.addWidget(self.label_amin, 2, 0)
        grid.addWidget(self.label_amax, 2, 1)

        grid.addWidget(self.splider_amin, 3, 0)
        grid.addWidget(self.splider_amax, 3, 1)

        grid.addWidget(self.label_cmin, 4, 0)
        grid.addWidget(self.label_cmax, 4, 1)

        grid.addWidget(self.splider_cmin, 5, 0)
        grid.addWidget(self.splider_cmax, 5, 1)

        self.btn_3d = QPushButton("Start slice 3d")
        self.btn_3d.setFont(QFont("Microsoft YaHei"))
        self.btn_3d .clicked.connect(lambda: self.slice_window())

        grid.addWidget(self.btn_3d, 6, 0)

        #self.slice_window()
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)

        self.setGeometry(300, 100, 500, 500)
        self.setWindowTitle('Slicer 3D window')
        self.show()

    def slice_window(self):
        global S_low
        global S_up
        global A_low
        global A_up
        global C_low
        global C_up

        S_low = self.splider_smin.value()
        S_up = self.splider_smax.value()
        A_low = self.splider_amin.value()
        A_up = self.splider_amax.value()
        C_low = self.splider_cmin.value()
        C_up = self.splider_cmax.value()
        self.slice3d=Slice_3d_window()
        self.slice3d.show()

class Slice_3d_window(QMainWindow):
    def __init__(self):
        super(Slice_3d_window, self).__init__()
        self.init_ui()

    def init_ui(self):

        vtkWidget = QVTKRenderWindowInteractor()
        ren = slice3d.slice_3d(path, S_low, S_up,A_low, A_up,C_low,C_up)
        vtkWidget.GetRenderWindow().AddRenderer(ren)

        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        self.iren.Start()

        self.setCentralWidget(vtkWidget)

        self.setGeometry(300, 100, 1200, 906)
        self.setWindowTitle('Colorful 3D window')
        self.show()

class Color_config(QMainWindow):

    def __init__(self,parent=None):

        super(QMainWindow, self).__init__(parent)

        centralWidget = QWidget(self)
        grid = QGridLayout()

        self.label_alpha_all= QLabel()
        self.label_alpha_all.setText("设置全局透明度：")
        self.label_alpha_all.setFont(QFont("Microsoft YaHei"))

        self.btn_color_all= QPushButton("设置全局颜色")
        self.btn_color_all.setFont(QFont("Microsoft YaHei"))
        self.btn_color_all.clicked.connect(lambda: self.global_color())

        self.label_alpha_tumor = QLabel()
        self.label_alpha_tumor.setText("设置肿瘤透明度：")
        self.label_alpha_tumor.setFont(QFont("Microsoft YaHei"))

        self.btn_color_tumor = QPushButton("设置肿瘤颜色")
        self.btn_color_tumor.setFont(QFont("Microsoft YaHei"))
        self.btn_color_tumor.clicked.connect(lambda: self.tumor_color())

        self.splider_alpha_all=QSlider(Qt.Horizontal)
        self.splider_alpha_all.setMinimum(0)#最小值
        self.splider_alpha_all.setMaximum(10)#最大值
        self.splider_alpha_all.setSingleStep(1)#步长
        self.splider_alpha_all.setTickPosition(QSlider.TicksBelow)#设置刻度位置，在下方
        self.splider_alpha_all.setTickInterval(1)#设置刻度间隔

        self.splider_alpha_tumor = QSlider(Qt.Horizontal)
        self.splider_alpha_tumor.setMinimum(0)  # 最小值
        self.splider_alpha_tumor.setMaximum(10)  # 最大值
        self.splider_alpha_tumor.setSingleStep(1)  # 步长
        self.splider_alpha_tumor.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.splider_alpha_tumor.setTickInterval(1)  # 设置刻度间隔

        grid.addWidget(self.label_alpha_all, 0, 0)
        grid.addWidget(self.btn_color_all, 0, 1)

        grid.addWidget(self.splider_alpha_all, 1, 0)

        grid.addWidget(self.label_alpha_tumor, 2, 0)
        grid.addWidget(self.btn_color_tumor, 2, 1)

        grid.addWidget(self.splider_alpha_tumor, 3, 0)

        self.btn_3d = QPushButton("开始3D分割")
        self.btn_3d.setFont(QFont("Microsoft YaHei"))
        self.btn_3d .clicked.connect(lambda: self.seg_window())

        grid.addWidget(self.btn_3d, 4, 0)

        #self.slice_window()
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)

        self.setGeometry(300, 100, 500, 500)
        self.setWindowTitle('Segmentation 3D window')
        self.show()

    def tumor_color(self):
        self.tumorcolor = QColorDialog.getColor().name()

    def global_color(self):
        self.globalcolor = QColorDialog.getColor().name()


    def seg_window(self):
        global tumor_color
        global global_color
        global tumor_alpha
        global global_alpha

        tumor_color=self.tumorcolor
        global_color=self.globalcolor
        tumor_alpha=self.splider_alpha_tumor.value()/10
        global_alpha=self.splider_alpha_all.value()/10
        self.show3d=Show3d()
        self.show3d.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())