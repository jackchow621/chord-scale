# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget,QLabel


class InstrumentPanel(QWidget):

    def __init__(self, instrument):
        super().__init__()
        self.panels = []
        self.instrument = instrument
        self.name = 'Instrument'
        self.detail = QLabel('')

    def createInstrumentPanel(self, instrs):
        for ins in instrs:
            if ins == 'Guitar':
                from Panel.GuitarPanel import GuitarPanel
                instrument = GuitarPanel()
            elif ins == 'Piano':
                from Panel.PianoPanel import PianoPanel
                instrument = PianoPanel()
            else:
                instrument = None
            self.panels.append(instrument)
        return self.panels

    def initUI(self):
        pass

    def initPanel(self):
        pass

    # change instrument's program
    def changeProgram(self, value):
        self.instrument.changeProgram(self.instrument.programs.index(value))

    # play a note
    def play(self, notes):
        self.instrument.playNote(notes)
