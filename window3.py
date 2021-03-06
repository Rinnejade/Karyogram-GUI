#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice, QMimeData, QPoint, Qt)
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp, QWidget, QDesktopWidget, QScrollArea, QApplication ,  QDialog, QGroupBox, QSizePolicy,
            QLabel, QFrame, QFileDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QGridLayout, QMessageBox, QPushButton, QLCDNumber, QSlider, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QColor, QDrag, QPainter, QPixmap, QScreen
import image_adjustments as ia
import cv2
import numpy as np


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
        self.setCentralWidget(self.form_widget)
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
        self.createGridLayout(folderPath)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        # self.setLayout(self.layout)

    def createGridLayout(self, folderPath):
        # folderPath = "/home/vinod/workspace/python-GUI/process/"
        folderPath = folderPath+"/"
        imageList = os.listdir(folderPath)
        self.horizontalGroupBox = QGroupBox()
        # scroll
        self.scroll = QScrollArea()
        layout = QGridLayout()

        # layout.setContentsMargins(5, 5,5,5)
        n = 0
        ID = 0

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        # # layout.setColumnStretch(0, 3);
        # for col in range(5):
        #     # print(column)
        #     layout.setColumnStretch(col, 10)
        for column in range(5):
            if n<len(imageList):
                path1 = folderPath + imageList[n]
                pixmap1 = QPixmap(path1)
                # pixmap2 = QPixmap(path2)
                dragWidget = DragWidget(pixmap1, str(n+1))
                # layout.addWidget(dragWidget, 0, column)
                layout1.addWidget(dragWidget)
            n = n+1
        for column in range(7):
            if n<len(imageList):
                path1 = folderPath + imageList[n]
                pixmap1 = QPixmap(path1)
                # pixmap2 = QPixmap(path2)
                dragWidget = DragWidget(pixmap1, str(n+1))
                layout2.addWidget(dragWidget)
                # layout.addWidget(dragWidget, 1, column)
            n = n+1
        for column in range(6):
            if n<len(imageList):
                path1 = folderPath + imageList[n]
                pixmap1 = QPixmap(path1)
                # pixmap2 = QPixmap(path2)
                dragWidget = DragWidget(pixmap1, str(n+1))
                layout3.addWidget(dragWidget)
                # layout.addWidget(dragWidget, 3, column)
            n = n+1
        for column in range(6):

            if n<len(imageList):
                print(column)
                path1 = folderPath + imageList[n]
                pixmap1 = QPixmap(path1)
                # pixmap2 = QPixmap(path2)
                if(column==4):
                    # print("Asda")
                    dragWidget = DragWidget(pixmap1, 'X')
                elif(column==5):
                    # print(column)
                    # print("asdafafs")
                    dragWidget = DragWidget(pixmap1, 'Y')
                else:
                    dragWidget = DragWidget(pixmap1, str(n+1))
                layout4.addWidget(dragWidget)
                # layout.addWidget(dragWidget, 4, column)
            n = n+1


        layout.addLayout(layout1, 0, 0)
        layout.addLayout(layout2, 1, 0)
        layout.addLayout(layout3, 2, 0)
        layout.addLayout(layout4, 3, 0)
        self.horizontalGroupBox.setLayout(layout)
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

        index = QLabel(idx, self)
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
