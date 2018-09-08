# -*- coding: utf-8 -*-
class MusicInstrument(object):
    notesAll = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    roots = ("C", "#C", "D", "bE", "E", "F", "#F", "G", "#G", "A", "bB", "B")
    pros = ("maj", "min", "dim", "half-dim", "aug", "aug-maj", "dom", "min-maj")
    intervals = ("-", "7", "9", "11", "13", "sus", "sus2")
    scales = ("Ionian(major)", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian(minor)", \
              "Locrian", "----------------", "Pentatonic-maj", "Pentatonic-min", "Blues-major", "Blues-minor")
    noteStyles = ("Letter", "Arabic numeral")

    def __init__ (self):
        print('**')