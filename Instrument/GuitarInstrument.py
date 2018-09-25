# -*- coding: utf-8 -*-
from Instrument.MusicalInstrument import MusicalInstrument


class GuitarInstrument(MusicalInstrument):
    notes = [[], [], [], [], [], []]

    def __init__(self):
        super().__init__()
        self.sd.setInstrument(0, 24, 0)  # Nylon Guitar
        self.noteStyles = ("Letter", "Arabic numeral")

    # generate notes on the both six string by the given fret number
    def initFretBoard(self, fretNum):
        self.notes = [[], [], [], [], [], []]
        self.fretNum = fretNum
        self.initString(1, 'E', 4)
        self.initString(2, 'B', 3)
        self.initString(3, 'G', 3)
        self.initString(4, 'D', 3)
        self.initString(5, 'A', 2)
        self.initString(6, 'E', 2)

    # generate notes on the specific string
    def initString(self, stringIndex, zeroNote, octave):
        index = self.notesAll.index(zeroNote)
        notePerStr = []
        for i in range(self.fretNum):
            tmp = self.notesAll[(index + i) % 12]
            notePerStr.append(tmp.split('/')[0] + '-' + str(octave))
            if tmp == 'B':
                octave = octave + 1

        self.notes[stringIndex - 1] = notePerStr
