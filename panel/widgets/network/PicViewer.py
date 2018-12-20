# -*- coding: utf-8 -*-
import shutil
from PyQt5.QtWidgets import QWidget, QLabel, QMenu, QAction, QFileDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage, QCursor


class PicViewer(QLabel, QWidget):
    images = []
    currentImg = QImage()
    index = 0
    ctrlPressed = False

    def __init__(self):
        super(QWidget, self).__init__()

    def view(self, images):
        self.scale = 0
        if len(images) == 0:
            self.setPixmap(QPixmap(r'images/nonetab.bmp'))
        else:
            try:
                self.images = images
                self.index = 0
                self.currentImg = QPixmap(self.images[self.index])
                self.setPixmap(self.currentImg)
            except Exception as ex:
                print(ex)

    def nextImg(self):
        self.scale = 0
        if len(self.images) == 0:
            return
        self.index = (self.index + 1) % len(self.images)
        self.currentImg = QPixmap(self.images[self.index])
        self.setPixmap(self.currentImg)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.nextImg()

    def contextMenuEvent(self, QContextMenuEvent):
        menu = QMenu()
        action = QAction('save this pic', self)
        action.triggered.connect(self.save)
        menu.addAction(action)
        menu.exec_(QCursor.pos())

    def zoomPic(self, zoomIn):
        if zoomIn:
            width = self.currentImg.width() * 1.2
            if (self.scale > 4):
                return
            height = self.currentImg.height() * 1.2
            self.scale = self.scale + 1
        else:
            width = self.currentImg.width() / 1.2
            if (self.scale < -4):
                return
            height = self.currentImg.height() / 1.2
            self.scale = self.scale - 1
        try:
            self.currentImg = QImage(self.images[self.index])
            self.currentImg = self.currentImg.scaled(QSize(width, height), Qt.IgnoreAspectRatio)
            self.resize(width, height)
            self.setPixmap(QPixmap.fromImage(self.currentImg))
        except Exception as ex:
            print(ex)

    def save(self):
        try:
            name, type = QFileDialog().getSaveFileName(self, 'save pic', '',
                                                       'img files(*.jpg *.gif *.jpeg *.png *.bmp);;all files(*.*)')
            # 100:The quality factor
            self.currentImg.save(str(name), 'jpg', 100)
        except Exception as ex:
            print(ex)
