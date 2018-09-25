# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from Instrument.PianoInstrument import *
from Panel.InstrumentPanel import InstrumentPanel
from Panel.widgets.PianoBoard import PianoBoard


class PianoPanel(InstrumentPanel):
    def __init__(self):
        super().__init__(PianoInstrument())
        self.name = 'Piano'
        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()
        # 往上对齐
        self.vbox.setAlignment(Qt.AlignTop)
        self.fl = QHBoxLayout()
        self.fl.setAlignment(Qt.AlignTop)
        self.board = PianoBoard(self.instrument, 4)
        self.fl.addWidget(self.board)

        # 垂直布局
        # self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.fl)
        self.vbox.addWidget(self.detail)
        self.setLayout(self.vbox)

    def initPanel(self, num, notes=None):
        self.fl.removeWidget(self.board)
        self.board.deleteLater()
        self.currentNum = num
        self.board = PianoBoard(self.instrument, self.currentNum)
        self.board.highlightNotes(notes)
        self.fl.addWidget(self.board)
