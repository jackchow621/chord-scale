# -*- coding: utf-8 -*-
import collections


class chord():
    def __init__(self):
        self.tmp = collections.OrderedDict()
        self.musicNotes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def getNextNote(self, index, distance, octave):
        noteOctave = octave
        if index + distance > 23:
            noteOctave += 2
        elif index + distance > 11:
            noteOctave += 1
        return self.musicNotes[(index + distance) % 12] + '-' + str(noteOctave)

    def getChord(self, root, pro, interval, octave=4):
        if root in self.musicNotes:
            index = self.musicNotes.index(root)
            self.tmp = {}
            self.tmp['1'] = root + '-' + str(octave)
            if interval == '-':  # triad chords
                if pro == 'maj':
                    self.tmp['3'] = self.getNextNote(index, 4, octave)
                    self.tmp['5'] = self.getNextNote(index, 7, octave)
                elif pro == 'min':
                    self.tmp['3'] = self.getNextNote(index, 3, octave)
                    self.tmp['5'] = self.getNextNote(index, 7, octave)
                elif pro == 'aug':
                    self.tmp['3'] = self.getNextNote(index, 4, octave)
                    self.tmp['5'] = self.getNextNote(index, 8, octave)
                elif pro == 'dim':
                    self.tmp['3'] = self.getNextNote(index, 3, octave)
                    self.tmp['5'] = self.getNextNote(index, 6, octave)
                else:
                    self.tmp['1'] = 'triad type error.'
            elif interval == '7':  # senventh chords
                if pro == '-':# 属七和弦/大小七和弦
                    self.getChord(root, 'maj', '-', octave)
                    self.tmp['7'] = self.getNextNote(index, 10, octave)
                elif pro == 'maj':  # 大七和弦
                    self.getChord(root, 'maj', '-', octave)
                    self.tmp['7'] = self.getNextNote(index, 11, octave)
                elif pro == 'min':  # 小七和弦
                    self.getChord(root, 'min', '-', octave)
                    self.tmp['7'] = self.getNextNote(index, 10, octave)
                elif pro == 'min-maj':  # 小大七和弦
                    self.getChord(root, 'min', '-', octave)
                    self.tmp['7'] = self.getNextNote(index, 11, octave)
                elif pro == 'half-dim':  # 半减七和弦
                    self.getChord(root, 'dim', '-', octave)
                    self.tmp['7'] = self.getNextNote(index, 10, octave)
                elif pro == 'dim':  # 减七和弦
                    self.getChord(root, 'dim', '-', octave)
                    self.tmp['7'] = self.getNextNote(index, 9, octave)
                elif pro == 'aug':  # 增七和弦
                    self.getChord(root, 'aug', '-', octave)
                    self.tmp['7'] = self.getNextNote(index, 10, octave)
                elif pro == 'augM':  # 增大七和弦
                    self.getChord(root, 'aug', '-', octave)
                    self.tmp['7'] = self.getNextNote(index, 11, octave)
                else:
                    self.tmp['1'] = 'triad type error.'
            elif interval == '9':
                self.getChord(root, pro, '7',octave)
                self.tmp['9'] = self.getNextNote(index, 14, octave)
            elif interval == '11':
                self.getChord(root, pro, '9',octave)
                self.tmp['11'] = self.getNextNote(index, 17, octave)
            elif interval == '13':
                self.getChord(root, pro, '11',octave)
                self.tmp['13'] = self.getNextNote(index, 21, octave)
            elif interval == 'sus':
                self.getChord(root, pro, '-',octave)
                # sus:replace third note with 4th note
                self.tmp['3'] = self.getNextNote(index, 5, octave)
            elif interval == 'sus2':
                self.getChord(root, pro, '-',octave)
                # sus2:replace third note with second note
                self.tmp['3'] = self.getNextNote(index, 2, octave)
            else:
                self.tmp['1'] = 'chord unsupported yet.'
        else:
            self.tmp['1'] = 'error root note'
        return self.tmp

    def getScales(self, root, pro):
        if root in self.musicNotes:
            index = self.musicNotes.index(root)
            self.tmp = {}
            self.tmp['1'] = root
            if pro.startswith('Ionian'):
                for i in range(1, 7):
                    if (i in (1, 2)):
                        self.tmp[str(i + 1)] = self.musicNotes[(index + i * 2) % 12]
                    elif (i in (3,)):
                        self.tmp[str(i + 1)] = self.musicNotes[(index + 5) % 12]
                    elif (i == 7):
                        self.tmp[str(i + 1)] = root
                    else:
                        self.tmp[str(i + 1)] = self.musicNotes[(index + i * 2 - 1) % 12]
            elif pro.startswith('Lydian'):
                self.tmp = self.getScales(root, 'Ionian')
                self.tmp['3'] = self.musicNotes[(index + 4) % 12]
                self.tmp['4'] = self.musicNotes[(index + 6) % 12]
            elif pro.startswith('Mixolydian'):
                self.tmp = self.getScales(root, 'Ionian')
                self.tmp['6'] = self.musicNotes[(index + 9) % 12]
                self.tmp['7'] = self.musicNotes[(index + 10) % 12]
            elif pro.startswith('Aeolian'):
                for i in range(1, 7):
                    if (i == 1):
                        self.tmp['2'] = self.musicNotes[(index + 2) % 12]
                    elif (i == 2):
                        self.tmp['3'] = self.musicNotes[(index + 3) % 12]
                    elif (i in (3, 4)):
                        self.tmp[str(i + 1)] = self.musicNotes[(index + i * 2 - 1) % 12]
                    elif (i == 5):
                        self.tmp[str(i + 1)] = self.musicNotes[(index + 8) % 12]
                    elif (i == 7):
                        self.tmp[str(i + 1)] = root
                    else:
                        self.tmp[str(i + 1)] = self.musicNotes[(index + i * 2 - 2) % 12]
            elif pro.startswith('Dorian'):
                self.tmp = self.getScales(root, 'Aeolian')
                self.tmp['6'] = self.musicNotes[(index + 9) % 12]
                self.tmp['7'] = self.musicNotes[(index + 10) % 12]
            elif pro.startswith('Phrygian'):
                self.tmp = self.getScales(root, 'Aeolian')
                self.tmp['2'] = self.musicNotes[(index + 1) % 12]
                self.tmp['3'] = self.musicNotes[(index + 3) % 12]
            elif pro.startswith('Locrian'):
                self.tmp = self.getScales(root, 'Phrygian')
                self.tmp['4'] = self.musicNotes[(index + 5) % 12]
                self.tmp['5'] = self.musicNotes[(index + 6) % 12]
            elif pro.startswith('Pentatonic-maj'):
                for i in range(1, 5):
                    if (i in (1, 2)):
                        self.tmp[str(i + 1)] = self.musicNotes[(index + i * 2) % 12]
                    else:
                        self.tmp[str(i + 1)] = self.musicNotes[(index + i * 2 + 1) % 12]
            elif pro.startswith('Pentatonic-min'):
                for i in range(1, 5):
                    if (i == 1):
                        self.tmp[str(i + 1)] = self.musicNotes[(index + 3) % 12]
                    elif (i in (2, 3)):
                        self.tmp[str(i + 1)] = self.musicNotes[(index + i * 2 + 1) % 12]
                    else:
                        self.tmp[str(i + 1)] = self.musicNotes[(index + 10) % 12]
            elif pro.startswith('Blues-maj'):
                self.tmp = self.getScales(root, 'Pentatonic-maj')
                self.tmp['b3'] = self.musicNotes[(index + 3) % 12]  # add a b3 on pen-maj
            elif pro.startswith('Blues-min'):
                self.tmp = self.getScales(root, 'Pentatonic-min')
                self.tmp['#4'] = self.musicNotes[(index + 6) % 12]  # add a #4 on pen-min
            elif pro.startswith('----'):
                self.tmp['1'] = 'please select a scale type.'
            else:
                self.tmp['1'] = 'scale unsupported yet.'
        else:
            self.tmp['1'] = 'error root note'
        return self.tmp

    '''def replaceNote(self,noteStr):
        notes = noteStr.split(',')
        if len(notes[0].split('/'))>1:
            notes[0] = notes[0].split('/')[1]
        print('**************',notes)
        for note in notes:
            if '/' in note:
                index = notes.index(note)
                splits = note.split('/')
                if splits[0].replace('#','') in notes:
                    notes[index] = splits[1]
                else:
                    notes[index] = splits[0]
        return ','.join(notes)'''


'''c=chord()  
print(c.getScales('C','Ionian').values())
print(c.getScales('F','Lydian').values())
print(c.getScales('G','Mixolydian').values())
print(c.getScales('A','Aeolian').values())
print(c.getScales('D','Dorian').values())
print(c.getScales('E','Phrygian').values())
print(c.getScales('B','Locrian').values())

c = chord()
for n in c.musicNotes:
    b = c.getChord(n, 'maj', '13', 4)
    print(b.values())
    # playLoop(b)
'''
