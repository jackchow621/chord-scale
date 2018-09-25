import unittest
import time
from mingus.containers import *

from sounds.sound import sound


class test_sound(unittest.TestCase):

    def setUp(self):
        self.sd = sound('ARACHNO')
        self.sd.setInstrument(0, 12, 0)
        self.sd.setInstrument(1, 40, 0)
        self.n = Note("C-6", 0)

    '''def test_playNote(self):
        n = Note("C-6",0)
        self.sd.playNote(n)
        time.sleep(1)

    def test_playNoteContainer(self):
        nc = NoteContainer(['C','E','G'])
        self.sd.playNoteContainer(nc)
        time.sleep(1)

    def test_playBar(self):
        lowBar1 = Bar()
        print(lowBar1.place_notes(['C-3'], 4))
        print(lowBar1.place_notes(['G-3'], 4))
        print(lowBar1.place_notes(['C-4'], 4))
        print(lowBar1.place_notes(['E-4'], 4))
        self.sd.playBar(lowBar1)

    def test_playBars(self):
        lowBar1 = Bar()
        print(lowBar1.place_notes(['C-3'], 4))
        print(lowBar1.place_notes(['G-3'], 4))
        print(lowBar1.place_notes(['C-4'], 4))
        print(lowBar1.place_notes(['E-4'], 4))
        lowBar2 = Bar()
        print(lowBar2.place_notes(['C-4'], 4))
        print(lowBar2.place_notes(['G-4'], 4))
        print(lowBar2.place_notes(['C-5'], 4))
        print(lowBar2.place_notes(['E-5'], 4))

        self.sd.playBars([lowBar1,lowBar2],[0,1])

    def test_playTrack(self):
        b1 = Bar()
        print(b1.place_notes(['G-5', ], 4))
        print(b1.place_notes(['E-5', ], 8))
        print(b1.place_notes(['F-5', ], 8))
        print(b1.place_notes(['G-5', ], 4))
        print(b1.place_notes(['E-5', ], 8))
        print(b1.place_notes(['F-5', ], 8))

        b2 = Bar()

        print(b2.place_notes(['G-5', ], 8))
        print(b2.place_notes(['G-4', ], 8))
        print(b2.place_notes(['A-4', ], 8))
        print(b2.place_notes(['B-4', ], 8))
        print(b2.place_notes(['C-5', ], 8))
        print(b2.place_notes(['D-5', ], 8))
        print(b2.place_notes(['E-5', ], 8))
        print(b2.place_notes(['F-5', ], 8))

        b3 = Bar()
        print(b3.place_notes(['E-5', ], 4))
        print(b3.place_notes(['C-5', ], 8))
        print(b3.place_notes(['D-5', ], 8))
        print(b3.place_notes(['E-5', ], 4))
        print(b3.place_notes(['E-4', ], 8))
        print(b3.place_notes(['F-4', ], 8))

        b4 = Bar()
        print(b4.place_notes(['G-4', ], 8))
        print(b4.place_notes(['A-4', ], 8))
        print(b4.place_notes(['G-4', ], 8))
        print(b4.place_notes(['F-4', ], 8))
        print(b4.place_notes(['G-4', ], 8))
        print(b4.place_notes(['C-5', ], 8))
        print(b4.place_notes(['B-4', ], 8))
        print(b4.place_notes(['C-5', ], 8))

        # m1 = self.synthInstrument('Celesta')
        # m1.names.append('Celesta')
        highTrack = Track()
        highTrack.add_bar(b1)
        highTrack.add_bar(b2)
        highTrack.add_bar(b3)
        highTrack.add_bar(b4)

        self.sd.playTrack(highTrack)

        def test_playTracks(self):
        lowBar1 = Bar()
        print(lowBar1.place_notes(['C-3'], 4))
        print(lowBar1.place_notes(['G-3'], 4))
        print(lowBar1.place_notes(['C-4'], 4))
        print(lowBar1.place_notes(['E-4'], 4))

        lowBar2 = Bar()
        print(lowBar2.place_notes(['G-2'], 4))
        print(lowBar2.place_notes(['D-3'], 4))
        print(lowBar2.place_notes(['G-3'], 4))
        print(lowBar2.place_notes(['B-3'], 4))

        lowBar3 = Bar()
        print(lowBar3.place_notes(['A-2'], 4))
        print(lowBar3.place_notes(['E-3'], 4))
        print(lowBar3.place_notes(['A-3'], 4))
        print(lowBar3.place_notes(['C-4'], 4))

        lowBar4 = Bar()
        print(lowBar4.place_notes(['E-2'], 4))
        print(lowBar4.place_notes(['B-2'], 4))
        print(lowBar4.place_notes(['E-3'], 4))
        print(lowBar4.place_notes(['G-3'], 4))

        b1 = Bar()
        print(b1.place_notes(['G-5', ], 4))
        print(b1.place_notes(['E-5', ], 8))
        print(b1.place_notes(['F-5', ], 8))
        print(b1.place_notes(['G-5', ], 4))
        print(b1.place_notes(['E-5', ], 8))
        print(b1.place_notes(['F-5', ], 8))

        b2 = Bar()

        print(b2.place_notes(['G-5', ], 8))
        print(b2.place_notes(['G-4', ], 8))
        print(b2.place_notes(['A-4', ], 8))
        print(b2.place_notes(['B-4', ], 8))
        print(b2.place_notes(['C-5', ], 8))
        print(b2.place_notes(['D-5', ], 8))
        print(b2.place_notes(['E-5', ], 8))
        print(b2.place_notes(['F-5', ], 8))

        b3 = Bar()
        print(b3.place_notes(['E-5', ], 4))
        print(b3.place_notes(['C-5', ], 8))
        print(b3.place_notes(['D-5', ], 8))
        print(b3.place_notes(['E-5', ], 4))
        print(b3.place_notes(['E-4', ], 8))
        print(b3.place_notes(['F-4', ], 8))

        b4 = Bar()
        print(b4.place_notes(['G-4', ], 8))
        print(b4.place_notes(['A-4', ], 8))
        print(b4.place_notes(['G-4', ], 8))
        print(b4.place_notes(['F-4', ], 8))
        print(b4.place_notes(['G-4', ], 8))
        print(b4.place_notes(['C-5', ], 8))
        print(b4.place_notes(['B-4', ], 8))
        print(b4.place_notes(['C-5', ], 8))

        # m1 = self.synthInstrument('Celesta')
        # m1.names.append('Celesta')
        highTrack = Track()
        highTrack.add_bar(b1)
        highTrack.add_bar(b2)
        highTrack.add_bar(b3)
        highTrack.add_bar(b4)

        # m2 = self.synthInstrument('Marimba')
        # m2.names.append('Marimba')
        bassTrack = Track()
        bassTrack.add_bar(lowBar1)
        bassTrack.add_bar(lowBar2)
        bassTrack.add_bar(lowBar3)
        bassTrack.add_bar(lowBar4)

        self.sd.playTracks([bassTrack,highTrack],[0,1])'''

    def test_loadSoundFont(self):
        self.sd.playNote(self.n)
        time.sleep(2)
        self.sd.loadSoundFont(r'c:\sounds\grand-piano-YDP-20160804.sf2')
        self.sd.playNote(self.n)
        time.sleep(2)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(test_sound)