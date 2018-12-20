# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import pyqtSignal, Qt


class PicScrool(QScrollArea):
    ctrlPressed = False
    zoomSignal = pyqtSignal(int)

    def __init__(self):
        super(QScrollArea, self).__init__()
        self.setMouseTracking(True)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Control:
            self.ctrlPressed = True
        return super().keyReleaseEvent(QKeyEvent)

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Control:
            self.ctrlPressed = False
        return super().keyReleaseEvent(QKeyEvent)

    def wheelEvent(self, QWheelEvent):
        if self.ctrlPressed:
            delta = QWheelEvent.angleDelta()
            oriention = delta.y() / 8
            if oriention > 0:
                self.zoomSignal.emit(True)
            else:
                self.zoomSignal.emit(False)
        else:
            return super().wheelEvent(QWheelEvent)
