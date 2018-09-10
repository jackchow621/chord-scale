# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QComboBox, \
    QVBoxLayout, QLineEdit, QStyleOptionButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPaintEvent
from PyQt5.QtCore import QSize, Qt, QRect
from Instrument.GuitarInstrument import *
from sound import *
import sys

screenWidth = 1920


# 吉他指板 用于展示和弦、音阶
class GuitarPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # self.show()

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
        self.numText = QLineEdit('21')
        test2 = QPushButton('音阶2')
        test2.clicked.connect(self.reDraw)

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
        self.hbox.addWidget(self.numText)
        self.hbox.addWidget(test2)

        self.fb = FretBoard(21)
        fl = QVBoxLayout()
        fl.addWidget(self.fb)

        # 垂直布局
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(fl)
        self.setLayout(self.vbox)

    def reDraw(self):
        self.fb.generateNote(int(self.numText.text()))
        self.fb.displayNote(False, ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        # self.fb.displayNote(True)


class FretBoard(QWidget):
    frets = []

    def __init__(self, fretboardNum):
        super().__init__()
        self.sd = sound('GUITAR')
        self.fretboardNum = fretboardNum
        self.initUI()

    def initUI(self):
        self.fretBoardLayout = QGridLayout()
        self.fretBoardLayout.setSpacing(0)
        self.generateNote(self.fretboardNum)

    # 初始化每一品的音名
    def generateNote(self, num):
        if num in list(range(12, 25)):
            self.fretboardNum = num
            self.guitar = GuitarInstrument(self.fretboardNum)
            self.__clearNote()
            for i in range(6):
                ftmp = []
                for j in range(self.fretboardNum):
                    fret = Fret()
                    fret.setToolTip(self.guitar.notes[i][j])
                    fret.drawFret(self)
                    self.fretBoardLayout.addWidget(fret, i, j)
                    ftmp.append(fret)
                self.frets.append(ftmp)
            try:
                self.setLayout(self.fretBoardLayout)
            except Exception as ex:
                print(ex)

    def __clearNote(self):
        if len(self.frets) > 0:
            for fret in self.frets:
                for f in fret:
                    self.fretBoardLayout.removeWidget(f)
                    f.deleteLater()
        self.frets = []

    # 显示音的名，可显示全部，也可显示执行的音阶。当传入音阶时，默认将第一个音当做根音
    def displayNote(self, isAll, notes=None):
        if isAll == True:
            for i in range(6):
                for j in range(self.fretboardNum):
                    self.frets[i][j].setText(self.guitar.notes[i][j])
                    self.frets[i][j].setImage('images/line-dot.bmp')
        else:
            root = notes[0]
            for i in range(6):
                for j in range(self.fretboardNum):
                    for n in notes:
                        if n == self.guitar.notes[i][j].split('-')[0]:  # 和弦内或音阶内的音
                            self.frets[i][j].setText(self.guitar.notes[i][j])
                            if root == self.guitar.notes[i][j].split('-')[0]:  # 根音
                                self.frets[i][j].setImage(2)
                                break
                            else:  # 普通音
                                self.frets[i][j].setImage(1)
                                break
                        else:  # 非和弦内或音阶内的音
                            self.frets[i][j].setText('')
                            self.frets[i][j].setImage(0)

    def playScale(self, scale):
        self.sd.playNotes(scale)

    def playChord(self, chord):
        self.sd.playChord(chord)


class Fret(QPushButton):
    def __init__(self):
        super().__init__()
        self.img = 'images/line.bmp'
        self.fontColor = 'black'

    def drawFret(self, parent):
        self.parent = parent
        self.fretWidth = int(screenWidth / self.parent.fretboardNum)
        self.fretHeight = int(self.fretWidth / 2)
        self.setFixedWidth(self.fretWidth)
        self.setFixedHeight(self.fretHeight)
        parent.setFixedHeight(self.fretHeight * 6)

        self.setStyleSheet("QPushButton {color: " + self.fontColor + "}")

        '''self.setStyleSheet("QPushButton { \n"
                           "background-color: white; \n"
                           "border-width: 1px; \n"
                           "border-color: golden; \n"
                           "border-style: solid; \n"
                           # "border-radius: 1; \n"
                           "}")'''

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        QPaintEvent.rect()
        painter.drawPixmap(0, 0, self.width(), self.height(), QPixmap(self.img))
        painter.drawText(QPaintEvent.rect(), Qt.AlignCenter, self.text())

    def enterEvent(self, *args, **kwargs):
        pass

    def leaveEvent(self, *args, **kwargs):
        pass

    def mousePressEvent(self, *args, **kwargs):
        self.parent.sd.playNote(self.toolTip())

    def setImage(self, fretType):
        if fretType == 0:
            self.img = 'images/line.bmp'
            self.fontColor = 'grey'
        elif fretType == 1:
            self.img = 'images/line-dot.bmp'
            self.fontColor = 'black'
        else:
            self.img = 'images/line-root.bmp'
            self.fontColor = 'white'
        self.setStyleSheet("QPushButton {color: " + self.fontColor + "}")
