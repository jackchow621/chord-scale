from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton


class PianoKey(QPushButton):
    currentKey = pyqtSignal(str)

    def __init__(self, text, type, keyWidth, x):
        super().__init__()
        self.highLightColor = ''
        self.type = type
        self.x = x
        self.keyWidth = keyWidth
        self.keyHeight = self.keyWidth * 7 if (self.type == 0) else (self.keyWidth * 5)
        self.setFixedWidth(self.keyWidth)
        self.setFixedHeight(self.keyHeight)
        self.initUI()

    def initUI(self):
        if self.type == 0:
            self.fontColor = 'black'
            self.backgroudColor = 'rgb(255,255,255)'  # default black key
            self.highLightColor = ''
        else:
            self.fontColor = 'white'
            self.backgroudColor = 'rgb(0, 0, 0)'  # default white key

    def paintEvent(self, QPaintEvent):
        self.setStyleSheet(
            "QPushButton {background-color:" + self.backgroudColor + ";}QPushButton {color: " + self.fontColor + "}")
        self.move(self.x, 0)
        return super().paintEvent(QPaintEvent)

    def enterEvent(self, *args, **kwargs):
        self.backgroudColor = 'rgb(200,200,50)'  # selected
        self.repaint()

    def leaveEvent(self, *args, **kwargs):
        # While leave the keynote,if the the key has a highlight color which mean it is a note in the specific scale/chord,
        # then set the background color to tht HIGHLIGHTCOLOR. Or otherwise set it to the default key style(white or black int [initUI] function)
        if self.highLightColor != '':
            self.backgroudColor = self.highLightColor
        else:
            self.initUI()
        self.repaint()

    def mousePressEvent(self, *args, **kwargs):
        try:
            self.currentKey.emit(self.text().replace('\r\n', ''))
        except Exception as ex:
            print(ex)

    def highlight(self, bool):
        if bool:
            self.highLightColor = 'rgb(100,180,250)'  # HIGHLIGHTCOLOR
            self.backgroudColor = self.highLightColor
        else:
            self.initUI()
        self.repaint()
