#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import os
from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice, QMimeData, QPoint, Qt, QRect)
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp, QWidget, QFrame,QGroupBox, QDesktopWidget, QApplication ,
            QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QMenu, QTextEdit, QColorDialog, QScrollArea, QInputDialog, QGridLayout, QMessageBox, QPushButton, QLCDNumber, QSlider, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap, QImage,QColor, QImageWriter, qRgb, QPainter, QPen, QDrag, QPainter, QPixmap, QScreen
import image_adjustments as ia
import cv2
import numpy as np
import test


class KaryogramUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Karyogram'
        self.initUI()

    def initUI(self):


        self.setMenuBar()

        self.resize(1200, 800)
        self.setWindowTitle(self.title)
        # logo
        self.setWindowIcon(QIcon('icons/logo.png'))
        self.form_widget = None
        self.show()

    def setMenuBar(self):
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

    def setImageLayout(self, folderPath):
        self.form_widget = FormWidget(self, folderPath)

        # paint window


        # add all main to the main vLayout
        # self.scribbleArea.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.form_widget, 0, 0)

        # central widget
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)
        # self.setCentralWidget(self.form_widget)
        self.show()

    def file_open(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder:', '.', QFileDialog.ShowDirsOnly)
        # print(dir_)
        self.setImageLayout(dir_)
        # pixmap = QPixmap(name)
        # self.display_image(pixmap)


    def file_save(self):
        if self.form_widget is not None:
            p = self.form_widget.scroll.widget().grab()
            filename = QFileDialog.getSaveFileName(self, 'Save File', '.',"Image files (*.jpg *.jpeg *.png)")[0]
            if filename :
                if not p.save(filename):
                    QMessageBox.warning(self, self.tr("Save Image"),
                        self.tr("Failed to save file at the specified location."))
        # self.setImageLayout(dir_)


class FormWidget(QWidget):

    def __init__(self, parent, folderPath):
        super(FormWidget, self).__init__(parent)
        self.setGeometry(300, 300, 1200, 300);


        self.imageList = self.getImageList(folderPath)
        self.ScribbleWindow = test.ScribbleWindow()
        self.scroll = QScrollArea()
        self.layout = QGridLayout()
        self.layout1 = QGridLayout()
        self.layout2 = QGridLayout()

        self.createGridLayout()


        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        # self.setLayout(self.layout)
    def getImageList(self,folderPath):
        folderPath = folderPath+"/"
        pathList = os.listdir(folderPath)
        imageList = list()
        for i in range(len(pathList)):
            path = folderPath + pathList[i]
            pixmap = QPixmap(path)
            imageList.insert(len(imageList), pixmap)
        return imageList;

    def createGridLayout(self):
        # folderPath = "/home/vinod/workspace/python-GUI/process/"

        self.horizontalGroupBox = QGroupBox()
        # scroll
        # layout.setContentsMargins(5, 5,5,5)
        n = 0
        ID = 0

        self.layout1.addWidget(self.ScribbleWindow, 0, 0);

        # layout.setColumnStretch(0, 3);
        for row in range(5):
            for col in range(10):
                if (n<len(self.imageList)):
                    pixmap = self.imageList[n]
                    # pixmap2 = QPixmap(path2)
                    dragWidget = DragWidget(pixmap, str(n+1))
                    self.layout2.addWidget(dragWidget, row, col)
                    n = n + 1


        self.layout.addLayout(self.layout1, 0, 0)
        self.layout.addLayout(self.layout2, 1, 0)
        self.horizontalGroupBox.setLayout(self.layout)
        self.scroll.setWidget(self.horizontalGroupBox)
        self.scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(400)
        self.v_layout = QVBoxLayout(self)
        self.v_layout.addWidget(self.scroll)

# dragWidget contains 2 images which can be dragged and dropped to any other widget
class DragWidget(QFrame):
    def __init__(self, pixmap1, idx, parent=None):
        super(DragWidget, self).__init__(parent)

        self.setMinimumSize(180, 180)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)

        image1 = QLabel(self)
        image1.setPixmap(pixmap1)
        image1.move(20, 20)
        image1.show()
        image1.setAttribute(Qt.WA_DeleteOnClose)


        # image2 = QLabel(self)
        # image2.setPixmap(pixmap2)
        # image2.move(100, 20)
        # image2.show()
        # image2.setAttribute(Qt.WA_DeleteOnClose)

        index = QLabel('', self)
        index.move(10, 160)
        index.setStyleSheet('color: red')
        index.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            itemData = event.mimeData().data('application/x-dnditemdata')
            dataStream = QDataStream(itemData, QIODevice.ReadOnly)

            pixmap = QPixmap()
            offset = QPoint()
            dataStream >> pixmap >> offset


            newIcon = QLabel(self)
            newIcon.setPixmap(pixmap)
            newIcon.move(event.pos() - offset)
            newIcon.show()
            newIcon.setAttribute(Qt.WA_DeleteOnClose)

            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.setDropAction(Qt.MoveAction)
                event.accept()

                # event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        child = self.childAt(event.pos())
        if not child:
            return

        pixmap = QPixmap(child.pixmap())

        # convert qpixmap to qimage and set image in scribblearea
        img = pixmap.toImage()
        self.parent().parent().parent().parent().ScribbleWindow.scribbleArea.setImage(img, True)

        itemData = QByteArray()
        dataStream = QDataStream(itemData, QIODevice.WriteOnly)
        dataStream << pixmap << QPoint(event.pos() - child.pos())

        mimeData = QMimeData()
        mimeData.setData('application/x-dnditemdata', itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos() - child.pos())

        tempPixmap = QPixmap(pixmap)
        painter = QPainter()
        painter.begin(tempPixmap)
        painter.fillRect(pixmap.rect(), QColor(127, 127, 127, 127))
        painter.end()

        child.setPixmap(tempPixmap)

        if drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
            child.close()
        else:
            child.show()
            child.setPixmap(pixmap)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = KaryogramUI()
    sys.exit(app.exec_())
