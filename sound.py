# -*- coding: utf-8 -*-

from mingus.containers import NoteContainer, Note
from mingus.midi import *
import time
import sys


class sound:
    global speed
    speed = 1.0

    def __init__(self, soundType):
        if soundType == 'PIANO':
            str = r'C:\sounds\Acoustic Guitars JNv2.4.sf2'
        elif soundType == 'GUITAR':
            str = r'C:\sounds\Acoustic Guitars JNv2.4.sf2'
        else:
            print("unsupported sound")
            sys.exit(1)
        if not fluidsynth.init(str):
            print("Couldn't load soundfont")
            sys.exit(1)

    def playNote(self, noteStr):
        fluidsynth.play_Note(Note(noteStr))
        print('play', noteStr)
        time.sleep(speed / 2)

    def playNotes(self, noteStrs):
        for noteStr in noteStrs:
            self.playNote(noteStr)

    def playChord(self, chordStr):
        fluidsynth.play_NoteContainer(NoteContainer(chordStr))
        time.sleep(speed)

    def playChords(self, chordStrs):
        for chordStr in chordStrs:
            self.playChord(chordStr)
            time.sleep(speed / 2)
            fluidsynth.play_NoteContainer(NoteContainer(chordStr))


'''s = sound()
g = Guitar(15)
for n in g.notes:
    print(n)
    s.playNotes(n)'''

# s.playChord(['C-4','E-4','G-4'])
# s.playChords([['C-4','E-4','G-4'],['F-4','A-4','C-5'],['G-4','B-4','D-2']])
