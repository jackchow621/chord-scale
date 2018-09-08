# -*- coding: utf-8 -*-
from Instrument.MusicInstrument import MusicInstrument


class GuitarInstrument(MusicInstrument):
    notes = [[],[],[],[],[],[]]

    def __init__(self, fretNum):
        self.noteStyles = ("Letter", "Arabic numeral")
        self.fretNum = fretNum
        self.initString(1, 'E', 4)
        self.initString(2, 'B', 3)
        self.initString(3, 'G', 3)
        self.initString(4, 'D', 3)
        self.initString(5, 'A', 2)
        self.initString(6, 'E', 2)

    def initString(self, string, zeroNote, octave):
        index = self.notesAll.index(zeroNote)
        notePerStr = []
        for i in range(self.fretNum):
            tmp = self.notesAll[(index + i) % 12]
            notePerStr.append(tmp.split('/')[0] + '-' + str(octave))
            if tmp == 'B':
                octave = octave + 1

        self.notes[string - 1] = notePerStr

    def initFretBoard(self):
        pass
# g = Guitar(15)
# print(g.notesAll)
# print(g.notes)
