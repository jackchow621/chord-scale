from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton


class GuitarFret(QPushButton):
    currentKey = pyqtSignal(str)

    def __init__(self, width, height):
        super().__init__()
        self.img = 'images/line.png'
        self.fontColor = 'black'
        self.fretWidth = width
        self.fretHeight = height
        self.setFixedWidth(self.fretWidth)
        self.setFixedHeight(self.fretHeight)
        self.fretType = 0

    def paintEvent(self, QPaintEvent):
        self.setStyleSheet("QPushButton {color: " + self.fontColor + ";border-image:url(" + self.img + ");}")
        return super().paintEvent(QPaintEvent)

    def enterEvent(self, *args, **kwargs):
        self.img = 'images/line-selected.png'
        self.repaint()

    def leaveEvent(self, *args, **kwargs):
        self.setImage(self.fretType)
        self.repaint()

    def mousePressEvent(self, *args, **kwargs):
        try:
            self.currentKey.emit(self.toolTip())
        except Exception as ex:
            print(ex)

    def setImage(self, fretType):
        self.fretType = fretType
        if fretType == 0:
            self.img = 'images/line.png'
            self.fontColor = 'grey'
        elif fretType == 1:
            self.img = 'images/line-dot.png'
            self.fontColor = 'black'
        else:
            self.img = 'images/line-root.png'
            self.fontColor = 'white'
        self.repaint()
