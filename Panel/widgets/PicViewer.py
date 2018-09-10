# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget,  QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage

class PicViewer(QLabel, QWidget):
    images = []
    currentImg = QImage()
    index = 0
    ctrlPressed = False

    def __init__(self):
        super(QWidget, self).__init__()

    def view(self, images):
        if len(images) == 0:
            self.setPixmap(QPixmap(r'../resources/image/nonetab.bmp'))
        else:
            self.images = images
            self.index = 0
            self.currentImg = QPixmap(self.images[self.index])
            self.setPixmap(self.currentImg)

    def nextImg(self):
        if len(self.images) == 0:
            return
        self.index = (self.index + 1) % len(self.images)
        self.currentImg = QPixmap(self.images[self.index])
        self.setPixmap(self.currentImg)

    def mousePressEvent(self, event):
        # self.currentImg.emit('hello')
        print("点击：")
        self.nextImg()

    def zoomPic(self, zoomIn):
        if zoomIn:
            width = self.currentImg.width() * 1.2
            height = self.currentImg.height() * 1.2
        else:
            width = self.currentImg.width() / 1.2
            height = self.currentImg.height() / 1.2
            print('zoom out')
        try:
            self.currentImg = QImage(self.images[self.index])
            self.currentImg = self.currentImg.scaled(QSize(width, height), Qt.IgnoreAspectRatio)
            self.resize(width, height)
            self.setPixmap(QPixmap.fromImage(self.currentImg))
        except Exception as ex:
            print(ex)