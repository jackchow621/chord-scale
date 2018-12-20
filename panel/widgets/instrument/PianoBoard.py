from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget
from panel.widgets.instrument.PianoKey import PianoKey


class PianoBoard(QWidget):
    def __init__(self, piano, oct):
        super().__init__()
        self.screenWidth = QApplication.desktop().availableGeometry().width() - 50
        self.setFixedWidth(self.screenWidth)
        self.oct = oct
        self.piano = piano
        self.piano.initFretBoard(oct)
        self.notes = self.piano.notes
        if not self.oct in range(1, 8):
            return
        self.layout = QHBoxLayout()
        self.drawBoard()

    def drawBoard(self):
        self.pks = []
        self.whiteKeyWidth = int(self.screenWidth / self.oct / 7)
        self.blackKeyWidth = int(self.whiteKeyWidth / 1.3)
        self.currentX = 0
        for i in range(self.oct):
            for j in range(7):  # white note
                pk = PianoKey('', 0, self.whiteKeyWidth, self.currentX)
                if j in (0, 1, 2):  # (0, 1, 2)--> (0 2 4)
                    pk.setText('\r\n\r\n\r\n\r\n\r\n\r\n\r\n' + self.notes[i * 12 + j * 2])
                else:  # (3,4,5,6)--> (5 7 9 11)
                    pk.setText('\r\n\r\n\r\n\r\n\r\n\r\n\r\n' + self.notes[i * 12 + j * 2 - 1])
                pk.currentKey.connect(self.piano.playNote)
                self.pks.append(pk)
                self.currentX = self.currentX + self.whiteKeyWidth
                self.layout.addWidget(pk)

            for j in range(5):  # black note
                self.tmp = 0
                if j > 1:  # (2,3,4)-->>(6,8,10)
                    self.tmp = self.whiteKeyWidth * 7 * i + (self.whiteKeyWidth * (j + 2) - self.blackKeyWidth / 2)
                    pk = PianoKey('', 1, self.blackKeyWidth, self.tmp)
                    pk.setText(self.notes[i * 12 + j * 2 + 2])
                else:  # (0,1)-->(1,3)
                    self.tmp = self.whiteKeyWidth * 7 * i + (self.whiteKeyWidth * (j + 1) - self.blackKeyWidth / 2)
                    pk = PianoKey('', 1, self.blackKeyWidth, self.tmp)
                    pk.setText(self.notes[i * 12 + j * 2 + 1])
                pk.currentKey.connect(self.piano.playNote)
                self.pks.append(pk)
                self.layout.addWidget(pk)

        self.setLayout(self.layout)

    def highlightNotes(self, notes):
        if notes == None:
            pass
        else:
            ns = []
            for n in notes:
                if len(n.split('-')) > 1:  # chord
                    n = n.split('-')[0]
                ns.append(n)
            for pk in self.pks:
                if pk.text().replace('\r\n', '').split('-')[0] in ns:
                    pk.highlight(True)
                else:
                    pk.highlight(False)
