# -*- coding: utf-8 -*-
import sys

from instrument.MusicalInstrument import MusicalInstrument
from sounds.sound import *


class PianoInstrument(MusicalInstrument):
    notes = []

    def __init__(self):
        super().__init__('ARACHNO')
        self.sd.setInstrument(0, 0, 0)  # Grand Piano
        self.noteStyles = ("Letter", "Arabic numeral")

    # generate notes off each octave
    def initFretBoard(self, oct):
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
