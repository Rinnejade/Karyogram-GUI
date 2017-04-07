#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp, QWidget, QDesktopWidget, QApplication ,
            QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QGridLayout, QMessageBox, QPushButton, QLCDNumber, QSlider, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap, QImage
import image_adjustments as ia
import cv2
import numpy as np


class KaryogramUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Karyogram'
        self.initUI()

    def initUI(self):

        self.pic = QLabel("",self)
        # exit Window
        exitAction = QAction(QIcon('icons/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        # open File
        openFile = QAction(QIcon('icons/open.png'), '&Open', self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
        self.statusBar()

        saveFile = QAction(QIcon('icons/save.png'), '&Save', self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)

        # menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        # imageMenu = menubar.addMenu('&Image')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(exitAction)

        # toolbar = self.addToolBar('open')
        # toolbar.addAction(openFile)

        self.createLayout()
        # size and position
        self.resize(1000, 800)
        self.center()
        self.setWindowTitle(self.title)
        # logo
        self.setWindowIcon(QIcon('icons/logo.png'))
        self.show()

    # centering the window
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createLayout(self):
        self.l1 = QLabel("Brightness", self)
        self.l2 = QLabel("Contrast", self)
        self.l3 = QLabel("Alpha Value", self)
        self.lcd1 = QLCDNumber(self)
        self.sld1 = QSlider(Qt.Horizontal, self)
        self.sld1.setMaximum(200)
        self.lcd2 = QLCDNumber(self)
        self.sld2 = QSlider(Qt.Horizontal, self)
        self.sld2.setValue(1)
        self.sld2.setMinimum(1)
        self.sld2.setRange(1, 10)
        self.lcd3 = QLCDNumber(self)
        self.sld3 = QSlider(Qt.Horizontal, self)

        self.histogram_checkBox = QCheckBox("Histogram", self)
        self.histogram_checkBox.toggle()
        # self.noise_checkBox = QCheckBox("Noise Remove", self)

        self.nextButton = QPushButton("Next", self)
        # cancelButton = QPushButton("Cancel")

        base = 50
        self.l1.move(1200, base)
        self.lcd1.move(1200, base+30)
        self.sld1.move(1200, base+60)
        base+= 120
        self.l2.move(1200, base)
        self.lcd2.move(1200, base+30)
        self.sld2.move(1200, base+60)

        base+= 120
        self.l3.move(1200, base)
        self.lcd3.move(1200, base+30)
        self.sld3.move(1200, base+60)

        self.sld1.valueChanged.connect(self.adjust_image)
        self.sld2.valueChanged.connect(self.adjust_image)
        self.sld3.valueChanged.connect(self.adjust_image)
        self.histogram_checkBox.stateChanged.connect(self.adjust_image)
        # self.noise_checkBox.stateChanged.connect(self.noise_check)


        base+= 120
        self.histogram_checkBox.move(1200, base+30)
        # self.noise_checkBox.move(1200, base+60)
        self.nextButton.move(1200, base+200)


    def file_open(self):
        name = QFileDialog.getOpenFileName(self,'Open file',
         '.',"Image files (*.jpg *.jpeg *.png)")[0]
        self.imageName = name
        print(name)
        pixmap = QPixmap(name)
        self.display_image(pixmap)


    def file_save(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', '.',"Image files (*.jpg *.jpeg *.png)")[0]
        print(path)
        if path:
            if not self.pic.pixmap().save(path):
                QMessageBox.warning(self, self.tr("Save Image"),
                     self.tr("Failed to save file at the specified location."))

    def display_image(self, pixmap):

        # pixmap_resized = pixmap.scaled(900, 600, QtCore.Qt.KeepAspectRatio)
        self.pic.setScaledContents(True);
        self.pic.move(100,100)
        self.pic.resize(900,550)
        self.pic.setPixmap(pixmap)

        self.pic.show() # You were missing this.
        # pixmap = ""

    # def noise_check(self, state):
    #     QpixmapImg = self.getImage()
    #     cv2Img = self.convertQpixmapToMat(QpixmapImg)
    #     if state == Qt.Checked:
    #         cv2Img = ia.hist_eqn(cv2Img)
    #     updated_Qpixmap = QPixmap("Out.jpg")
    #     self.display_image(updated_Qpixmap)

    def adjust_image(self, state):
        self.sld1.valueChanged.connect(self.lcd1.display)
        self.sld2.valueChanged.connect(self.lcd2.display)
        self.sld3.valueChanged.connect(self.lcd3.display)
        QpixmapImg = self.getImage()
        cv2Img = self.convertQpixmapToMat(QpixmapImg)
        # adjust brightness
        brightness_value = self.sld1.value()
        cv2Img = ia.control_brightness(cv2Img, brightness_value)
        # adjust contrast
        contrast_value = self.sld2.value()
        cv2Img = ia.control_contrast(cv2Img, contrast_value)
        # histogram_equalisation
        if state == Qt.Checked:
            cv2Img = ia.hist_eqn(cv2Img)
        updated_Qpixmap = QPixmap("Out.jpg")
        self.display_image(updated_Qpixmap)

    def getImage(self):
        img = QPixmap(self.imageName)
        return img

    def convertQpixmapToMat(self, incomingImage):
        incomingImage = incomingImage.toImage()
        incomingImage = incomingImage.convertToFormat(4)

        width = incomingImage.width()
        height = incomingImage.height()
        ptr = incomingImage.constBits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
        return arr

    # def convertMatToQpixmap(self, cv_img):
    #
    #     # Notice the dimensions.
    #     height, width, bytesPerComponent = cv_img.shape
    #     bytesPerLine = width * 3;
    #     # Convert to RGB for QImage.
    #     cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB, cv_img)
    #     qImg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    #     pix = QPixmap.fromImage(qImg)
    #     return pix

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = KaryogramUI()
    sys.exit(app.exec_())
