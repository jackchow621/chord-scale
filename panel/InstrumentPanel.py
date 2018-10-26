# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel


class InstrumentPanel(QWidget):

    def __init__(self, instrument):
        super().__init__()
        self.panels = []
        self.instrument = instrument
        self.name = 'instrument'
        self.detail = QLabel('')

    def createInstrumentPanel(self, instrs):
        for ins in instrs:
            if ins == 'Guitar':
                from panel.GuitarPanel import GuitarPanel
                instrument = GuitarPanel()
            elif ins == 'Piano':
                from panel.PianoPanel import PianoPanel
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

    def playNote(self, note, sec):
        self.instrument.playNote(note, sec)

    def playScale(self, scale, sec):
        for note in scale:
            self.instrument.playNote(note, sec)

    def playChord(self, chord, sec):
        self.instrument.playChord(chord, sec)

    def playArpeggio(self, notes, sec):
        self.instrument.playArpeggio(notes, sec)
