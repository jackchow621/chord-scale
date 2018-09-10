# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QComboBox, \
    QVBoxLayout, QLineEdit, QStyleOptionButton, QSlider
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPaintEvent
from PyQt5.QtCore import QSize, Qt, QRect, pyqtSignal
from Instrument.PianoInstrument import *
from sound import *
import sys


# 吉他指板 用于展示和弦、音阶
class PianoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.vbox = QVBoxLayout()
        # 往上对齐
        self.vbox.setAlignment(Qt.AlignTop)

        # 查询条件
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(21)
        root = QLabel('根音')
        rootCombo = QComboBox()
        pro = QLabel('三音')
        proCombo = QComboBox()
        invervel = QLabel('五音')
        invervelCombo = QComboBox()
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setFixedWidth(300)
        self.slider.setMinimum(3)
        self.slider.setMaximum(7)
        self.slider.setValue(4)
        self.slider.valueChanged[int].connect(self.initPiano)
        test2 = QPushButton('生成')
        # test2.clicked.connect(self.reDraw)

        test2.setStyleSheet("QPushButton { \n"
                            "background-color: white; \n"
                            "border-width: 1px; \n"
                            "border-color: golden; \n"
                            "border-style: solid; \n"
                            "border-radius: 1; \n"
                            # "border-image:url(images/line.png); \n"
                            "}")

        self.hbox.addWidget(root)
        self.hbox.addWidget(rootCombo)
        self.hbox.addWidget(pro)
        self.hbox.addWidget(proCombo)
        self.hbox.addWidget(invervel)
        self.hbox.addWidget(invervelCombo)
        self.hbox.addWidget(self.slider)
        self.hbox.addWidget(test2)

        self.fl = QHBoxLayout()
        self.fl.setAlignment(Qt.AlignTop)
        self.board = PianoBoard(4)
        self.fl.addWidget(self.board)

        # 垂直布局
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.fl)
        self.setLayout(self.vbox)

    def initPiano(self, value):
        self.fl.removeWidget(self.board)
        self.board.deleteLater()
        self.board = PianoBoard(value)
        self.fl.addWidget(self.board)


class PianoBoard(QWidget):
    screenWidth = 1366

    def __init__(self, oct):
        super().__init__()
        self.setFixedWidth(self.screenWidth)
        self.oct = oct
        self.notes = PianoInstrument(self.oct).notes
        if not self.oct in range(1, 8):
            return
        self.sd = sound('PIANO')
        self.layout = QHBoxLayout()
        self.drawBoard()

    def drawBoard(self):
        self.whiteKeyWidth = int(self.screenWidth / self.oct / 7)
        self.blackKeyWidth = int(self.whiteKeyWidth / 1.3)
        self.currentX = 0
        for i in range(self.oct):
            for j in range(7):  # white note
                pk = PianoKey('', 0, self.whiteKeyWidth, self.currentX)
                if j in (0, 1, 2):  # (0, 1, 2)--> (0 2 4)
                    pk.setText('\r\n\r\n\r\n\r\n\r\n\r\n\r\n' + self.notes[i * 12 + j * 2])
                else:  # (3,4,5,6)--> (5 7 9 11)
                    pk.setText('\r\n\r\n\r\n\r\n\r\n\r\n\r\n' + self.notes[i * 12 + j * 2 - 1])
                pk.currentKey.connect(self.playNote)
                self.currentX = self.currentX + self.whiteKeyWidth
                self.layout.addWidget(pk)

            for j in range(5):  # black note
                self.tmp = 0
                if j > 1:  # (2,3,4)-->>(6,8,10)
                    self.tmp = self.whiteKeyWidth * 7 * i + (self.whiteKeyWidth * (j + 2) - self.blackKeyWidth / 2)
                    pk = PianoKey('', 1, self.blackKeyWidth, self.tmp)
                    pk.setText(self.notes[i * 12 + j * 2 + 2])
                else:  # (0,1)-->(1,3)
                    self.tmp = self.whiteKeyWidth * 7 * i + (self.whiteKeyWidth * (j + 1) - self.blackKeyWidth / 2)
                    pk = PianoKey('', 1, self.blackKeyWidth, self.tmp)
                    pk.setText(self.notes[i * 12 + j * 2 + 1])
                pk.currentKey.connect(self.playNote)
                self.layout.addWidget(pk)

        self.setLayout(self.layout)

    def playNote(self, str):
        self.sd.playNote(str)


class PianoKey(QPushButton):
    currentKey = pyqtSignal(str)

    def __init__(self, text, type, keyWidth, x):
        super().__init__()
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
            self.backgroudColor = 'rgb(255,255,255)'
        else:
            self.fontColor = 'white'
            self.backgroudColor = 'rgb(0, 0, 0)'

    def paintEvent(self, QPaintEvent):
        self.setStyleSheet(
            "QPushButton {background-color:" + self.backgroudColor + ";}QPushButton {color: " + self.fontColor + "}")
        self.move(self.x, 0)
        return super().paintEvent(QPaintEvent)

    def enterEvent(self, *args, **kwargs):
        self.backgroudColor = 'rgb(200,200,50)'
        self.repaint()

    def leaveEvent(self, *args, **kwargs):
        self.initUI()
        self.repaint()

    def mousePressEvent(self, *args, **kwargs):
        try:
            self.currentKey.emit(self.text())
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = PianoPanel()
    sys.exit(app.exec_())
