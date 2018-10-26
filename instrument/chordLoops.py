# -*- coding:utf-8 -*-
import six
from mingus.containers import Bar, NoteContainer, Note

from chord import chord
from instrument.MusicalInstrument import MusicalInstrument

mi = MusicalInstrument('ARACHNO')
c = chord()

presets = {'piano': ['preset1', 'preset2', 'preset3', 'preset4'],
           'guitar': ['preset1', 'preset2'],
           'bass': ['preset1'],
           'drum': ['preset']}


def getLoop(root, octave, pro, interval, style, preset):
    assert style in presets.keys()
    octave = int(octave)
    notes = list(c.getChord(root, pro, interval, octave).values())
    if style in ('piano'):
        return getPianoLoop(notes, preset)
    elif style in ('guitar'):
        return getGuitarLoop(notes, preset)


def getPianoLoop(notes, preset):
    b = Bar()
    if preset == 'preset1':
        b.place_notes([notes[0], notes[1:]], 4)
        b.place_notes(notes[1:], 4)
        b.place_notes(notes[1:], 4)
        b.place_notes(notes[1:], 4)
    elif preset == 'preset2':
        b.place_notes([notes[0], notes[1:]], 8)
        b.place_notes(notes[2], 8)
        b.place_notes(notes[1:], 8)
        b.place_notes(notes[2], 8)
        b.place_notes(notes[1:], 8)
        b.place_notes(notes[2], 8)
        b.place_notes(notes[1:], 8)
        b.place_notes(notes[2], 8)
    elif preset == 'preset3':
        b.place_notes(notes[0], 4)
        b.place_notes(notes[2], 4)
        b.place_notes(changeOctave(notes[0], 1), 4)
        b.place_notes(changeOctave(notes[1:], 1), 4)
    elif preset == 'preset4':
        b.place_notes(notes[0], 4)
        b.place_notes(notes[1], 8)
        b.place_notes(notes[2], 4)
        b.place_notes(notes[3], 8)
    return b


def getGuitarLoop(notes, preset):
    b = Bar()
    if preset == 'preset1':
        b.place_notes(notes[0], 4)
        b.place_notes(notes[2], 4)
        b.place_notes([changeOctave(notes[0], 1), changeOctave(notes[1], 1)], 4)
        b.place_notes(notes[2], 4)
    if preset == 'preset2':
        b.place_notes(notes[0], 8)
        b.place_notes(notes[2], 8)
        b.place_notes(changeOctave(notes[0], 1), 8)
        b.place_notes(notes[2], 8)
        b.place_notes(changeOctave(notes[1], 1), 8)
        b.place_notes(notes[2], 8)
        b.place_notes(changeOctave(notes[0], 1), 8)
        b.place_notes(notes[2], 8)
    return b


def changeOctave(notes, value):
    result = []
    if isinstance(notes, list):
        for note in notes:
            n = Note(note)
            n.change_octave(value)
            result.append(n)
    else:
        n = Note(notes)
        n.change_octave(value)
        result = n
    return result


def playLoop(bar):
    mi.sd.playBar(bar, 0, 90)


def getStyles():
    return list(presets.keys())


def getPresets(instrument=None):
    if instrument:
        result = []
        assert instrument in list(presets.keys())
        for l in list(presets.get(instrument)):
            result.append(instrument + '-' + l)
        return result
    else:
        result = []
        for k in presets.keys():
            result.extend(getPresets(k))
        return result


if __name__ == '__main__':
    # for p in list(presets.get('guitar')):
    for i, j, k, l in [['C', 'maj', 4, '9'], ['A', 'min', 3, '7'], ['D', 'min', 4, '7'], ['G', '-', 3, '7']]:
        b = getLoop(i, k, j, l, 'guitar', 'preset2')
        print(b)
        playLoop(b)
