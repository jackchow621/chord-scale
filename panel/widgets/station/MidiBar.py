# -*- coding: utf-8 -*-
from PyQt5.Qt import *
from panel.widgets.station.BarSelector import BarSelector


class MidiBar(QPushButton):
    barDeleteSignal = pyqtSignal(object)
    barChangeSignal = pyqtSignal(object)
    barPlaySignal = pyqtSignal(object)

    def __init__(self, dict):
        super().__init__()
        self.dict = dict
        self.bar = None
        self.initUI()
        self.setBar()

    def initUI(self):
        self.setStyleSheet("QPushButton{border-image:url(images/bar.png);}")
        # icon = QPixmap(r'images/bar.png')
        # icon.scaled(QSize(100, 100), Qt.IgnoreAspectRatio)
        # self.setIcon(icon)
        self.setFixedWidth(100)
        self.setFixedHeight(100)

    def contextMenuEvent(self, QContextMenuEvent):
        menu = QMenu()
        playAction = QAction('play')
        menu.addAction(playAction)
        playAction.triggered.connect(self.play)
        delAction = QAction('delete')
        menu.addAction(delAction)
        delAction.triggered.connect(self.delete)
        menu.exec_(QCursor.pos())

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            bs = BarSelector(self.dict)
            bs.testPlaySignal.connect(self.testPlay)
            if bs.exec_():
                self.dict = bs.getResult()
                self.setBar()

    def setBar(self):
        if len(self.dict) == 3:
            labels = self.dict.get('label')
            if len(labels) == 6:
                self.setText(labels[0] + labels[2] + labels[3] + '\r\n' + labels[5])
                self.bar = self.dict.get('bar')
                self.barChangeSignal.emit(self)

    def delete(self):
        self.barDeleteSignal.emit(self)

    def play(self):
        if self.bar:
            self.barPlaySignal.emit(self.bar)
        else:
            QMessageBox().information(self, '错误', '小节为空')

    def testPlay(self, bar):
        self.barPlaySignal.emit(bar)
