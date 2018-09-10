# -*- coding: utf-8 -*-
from Instrument.MusicInstrument import MusicInstrument
from sound import *


class PianoInstrument(MusicInstrument):
    notes = []

    def __init__(self, oct):
        self.noteStyles = ("Letter", "Arabic numeral")
        self.sd = sound('PIANO')
        self.initNote(oct)

    def initNote(self, oct):
        self.notes = []
        self.oct = oct
        self.minOct = 4
        if not self.oct in range(1, 8):
            sys.exit(1)

        if self.oct % 2 != 0:
            self.minOct = 4 - int(oct / 2)
        elif self.oct == 2:
            self.minOct = 4
        elif self.oct == 4:
            self.minOct = 3
        elif self.oct == 6:
            self.minOct = 2
        # print('lowest c is:c-' + str(self.minOct) + ',and octave num is:' + str(self.oct))

        for i in range(self.oct):
            for j in range(12):
                self.notes.append(self.notesAll[j].split('/')[0] + '-' + str(self.minOct))
            self.minOct = self.minOct + 1

        #print(self.notes)


'''for c in range(1, 8):
    p = PianoInstrument(c)'''
