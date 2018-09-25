# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from Instrument.GuitarInstrument import *
from Panel.InstrumentPanel import InstrumentPanel
from Panel.widgets.GuitarBoard import GuitarBoard


class GuitarPanel(InstrumentPanel):
    def __init__(self):
        super().__init__(GuitarInstrument())
        self.name = 'Guitar'
        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()
        # 往上对齐
        self.vbox.setAlignment(Qt.AlignTop)
        self.fb = GuitarBoard(self.instrument, 21)
        self.fb.displayNote(None)

        self.fl = QVBoxLayout()
        self.fl.addWidget(self.fb)

        # 垂直布局
        self.vbox.addLayout(self.fl)
        self.vbox.addWidget(self.detail)
        self.setLayout(self.vbox)

    def initPanel(self, num, notes=None):
        self.fl.removeWidget(self.fb)
        self.fb.deleteLater()
        self.currentNum = num
        self.fb = GuitarBoard(self.instrument, self.currentNum)
        self.fb.displayNote(notes)
        self.fl.addWidget(self.fb)
