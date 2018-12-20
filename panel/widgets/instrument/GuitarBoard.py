from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QGridLayout, QVBoxLayout, QWidget, QLabel

from chord import chord
from panel.widgets.instrument.GuitarFret import GuitarFret


class GuitarBoard(QWidget):
    frets = []
    positions = ['C', 'A', 'G', 'E', 'D']

    def __init__(self, guitar, fretboardNum):
        super().__init__()
        self.screenWidth = QApplication.desktop().availableGeometry().width()
        self.guitar = guitar
        self.fretboardNum = int(fretboardNum) + 1  # include fret zero
        self.c = chord()
        self.roots = self.c.musicNotes
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.fretBoardLayout = QGridLayout()
        self.fretBoardLayout.setSpacing(0)

        self.numLayout = QGridLayout()
        # self.numLayout.setSpacing(1)

        self.background = QLabel()
        self.background.setPixmap(QPixmap(r'images/fretboard.jpg'))
        # self.background.setStyleSheet("background-color:yellow");
        self.fretBoardLayout.addWidget(self.background, 0, 0, 6, self.fretboardNum)

        if self.fretboardNum in list(range(12, 26)):
            fretWidth = int(self.screenWidth / self.fretboardNum)
            self.setFixedHeight(fretWidth * 3.5)

            self.guitar.initFretBoard(self.fretboardNum)
            self.__clearNote()
            for i in range(6):
                ftmp = []
                for j in range(self.fretboardNum):
                    fret = GuitarFret(fretWidth, fretWidth / 2)
                    fret.setToolTip(self.guitar.notes[i][j])
                    fret.currentKey.connect(self.guitar.playNote)
                    self.fretBoardLayout.addWidget(fret, i, j)
                    ftmp.append(fret)
                self.frets.append(ftmp)

            # this special frets have a white dot on it
            # use the label below the fretboard instead.
            for j in range(self.fretboardNum):
                # if j in (0, 3, 5, 7, 9, 12, 15, 17, 19, 21):
                # lb = QLabel('Fret' + str(j))
                lb = QLabel()
                lb.setFixedWidth(fretWidth)
                lb.setFixedHeight(fretWidth / 2)
                if j in (0, 3, 5, 7, 9, 12, 15, 17, 19, 21):
                    lb.setText('Fret' + str(j))
                lb.setAttribute(Qt.WA_TranslucentBackground)
                # lb.setStyleSheet("background-color:red");
                lb.setAlignment(Qt.AlignCenter)
                self.numLayout.addWidget(lb, 0, j)

            self.layout.addLayout(self.fretBoardLayout)
            self.layout.addLayout(self.numLayout)
            self.setLayout(self.layout)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        QPaintEvent.rect()
        # painter.drawPixmap(0, 0, self.width(), self.height(), QPixmap('images/fretboard.jpg'))
        return super().paintEvent(QPaintEvent)

    def __clearNote(self):
        if len(self.frets) > 0:
            for fret in self.frets:
                for f in fret:
                    self.fretBoardLayout.removeWidget(f)
                    f.deleteLater()
        self.frets = []

    def displayNote(self, notes=None, root=None, fretScopeMin=None, fretScopeMax=None):
        if notes == None:
            for i in range(6):
                for j in range(fretScopeMin, fretScopeMax + 1):
                    self.frets[i][j].setText(self.guitar.notes[i][j])
                    self.frets[i][j].setImage(1)
        else:
            # root = notes[0].split('-')[0]
            for i in range(6):
                for j in range(fretScopeMin, fretScopeMax + 1):
                    for n in notes:
                        if n.split('-')[0] == self.guitar.notes[i][j].split('-')[0]:  # 和弦内或音阶内的音
                            self.frets[i][j].setText(self.guitar.notes[i][j])
                            if root.split('-')[0] == self.guitar.notes[i][j].split('-')[0]:  # 根音
                                self.frets[i][j].setImage(2)
                                break
                            else:  # 普通音
                                self.frets[i][j].setImage(1)
                                break
                        else:  # 非和弦内或音阶内的音
                            self.frets[i][j].setText('')
                            self.frets[i][j].setImage(0)

    # caged system
    def displayPattern(self, notes, root, position):
        # notes[0] as the root note of the scale compared
        if position == 'C':
            for note in self.guitar.notes[4]:
                # If the note is the root note,pick up all the root note positions,
                # then determin whether to display this [guitar position].
                # The same below
                if note.split('-')[0] == notes[0]:
                    # the root note of the C position is on the 5th string
                    indexs = [i for i, j in enumerate(self.guitar.notes[4]) if j == note]
                    for index in indexs:
                        if index > 2 and index < self.fretboardNum:
                            # the C position takes 4 frets(including zero fret),and root note starts from 4th of the scope
                            self.displayNote(notes, root, index - 3, index)
        elif position == 'A':
            for note in self.guitar.notes[4]:
                if note.split('-')[0] == notes[0]:
                    # the root note of the A position is on the 5th string
                    indexs = [i for i, j in enumerate(self.guitar.notes[4]) if j == note]
                    for index in indexs:
                        if index > 0 and index + 3 < self.fretboardNum:
                            # the A position takes 5 frets(including zero fret),and root note starts from 2nd of the scope
                            self.displayNote(notes, root, index - 1, index + 3)
        elif position == 'G':
            for note in self.guitar.notes[5]:
                if note.split('-')[0] == notes[0]:
                    # the root note of the G position is on the 6th string
                    indexs = [i for i, j in enumerate(self.guitar.notes[5]) if j == note]
                    for index in indexs:
                        if index > 3 and index < self.fretboardNum:
                            # the G position takes 5 frets(including zero fret),and root note starts from 5th of the scope
                            self.displayNote(notes, root, index - 4, index)
        elif position == 'E':
            for note in self.guitar.notes[5]:
                if note.split('-')[0] == notes[0]:
                    # the root note of the E position is on the 6th string
                    indexs = [i for i, j in enumerate(self.guitar.notes[5]) if j == note]
                    for index in indexs:
                        if index > 2 and index + 2 < self.fretboardNum:
                            # the E position takes 4 frets(including zero fret),and root note starts from 2nd of the scope
                            self.displayNote(notes, root, index - 1, index + 2)
        elif position == 'D':
            for note in self.guitar.notes[3]:
                if note.split('-')[0] == notes[0]:
                    # the root note of the D position is on the 4th string
                    indexs = [i for i, j in enumerate(self.guitar.notes[3]) if j == note]
                    for index in indexs:
                        if index > 2 and index + 3 < self.fretboardNum:
                            # the D position takes 5 frets(including zero fret),and root note starts from 2nd of the scope
                            self.displayNote(notes, root, index - 1, index + 3)
        elif position == '-':
            self.displayNote(notes, root, 0, self.fretboardNum - 1)

    def displayPatternNote(self, notes, mode, position):
        if position == '-':
            self.displayPattern(notes, notes[0], position)
            return
        rootIndex = self.roots.index(notes[0])
        posIndex = self.positions.index(position)
        if mode == 'Ionian':
            calNote = self.roots[(rootIndex + 0) % 12]
            self.displayPattern(list(self.c.getScales(calNote, 'Ionian').values()), notes[0],
                                self.positions[(posIndex + 0) % 5])
        elif mode == 'Dorian':
            calNote = self.roots[(rootIndex + 10) % 12]
            self.displayPattern(list(self.c.getScales(calNote, 'Ionian').values()), notes[0],
                                self.positions[(posIndex + 1) % 5])
        elif mode == 'Phrygian':
            calNote = self.roots[(rootIndex + 8) % 12]
            self.displayPattern(list(self.c.getScales(calNote, 'Ionian').values()), notes[0],
                                self.positions[(posIndex + 2) % 5])
        elif mode == 'Lydian':
            calNote = self.roots[(rootIndex + 7) % 12]
            self.displayPattern(list(self.c.getScales(calNote, 'Ionian').values()), notes[0],
                                self.positions[(posIndex + 2) % 5])
        elif mode == 'Mixolydian':
            calNote = self.roots[(rootIndex + 5) % 12]
            self.displayPattern(list(self.c.getScales(calNote, 'Ionian').values()), notes[0],
                                self.positions[(posIndex + 3) % 5])
        elif mode == 'Aeolian':
            calNote = self.roots[(rootIndex + 3) % 12]
            self.displayPattern(list(self.c.getScales(calNote, 'Ionian').values()), notes[0],
                                self.positions[(posIndex + 4) % 5])
        elif mode == 'Locrian':
            calNote = self.roots[(rootIndex + 1) % 12]
            self.displayPattern(list(self.c.getScales(calNote, 'Ionian').values()), notes[0],
                                self.positions[(posIndex + 0) % 5])
        else:
            self.displayPattern(notes, notes[0], position)
