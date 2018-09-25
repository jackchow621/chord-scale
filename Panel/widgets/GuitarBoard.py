from PyQt5.QtGui import QPainter,QPixmap
from PyQt5.QtWidgets import QApplication, QGridLayout,QWidget
from Panel.widgets.GuitarFret import GuitarFret


class GuitarBoard(QWidget):
    frets = []

    def __init__(self, guitar, fretboardNum):
        super().__init__()
        self.screenWidth = QApplication.desktop().availableGeometry().width()
        self.guitar = guitar
        self.fretboardNum = int(fretboardNum)
        self.initUI()

    def initUI(self):
        self.fretBoardLayout = QGridLayout()
        self.fretBoardLayout.setSpacing(1)
        if self.fretboardNum in list(range(12, 25)):
            fretWidth = int(self.screenWidth / self.fretboardNum)
            self.setFixedHeight(fretWidth * 3)

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
            self.setLayout(self.fretBoardLayout)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        QPaintEvent.rect()
        painter.drawPixmap(0, 0, self.width(), self.height(), QPixmap('images/fretboard.bmp'))
        return super().paintEvent(QPaintEvent)

    def __clearNote(self):
        if len(self.frets) > 0:
            for fret in self.frets:
                for f in fret:
                    self.fretBoardLayout.removeWidget(f)
                    f.deleteLater()
        self.frets = []

    # 显示音的名，可显示全部，也可显示执行的音阶。当传入音阶时，默认将第一个音当做根音
    def displayNote(self, notes=None):
        if notes == None:
            for i in range(6):
                for j in range(self.fretboardNum):
                    self.frets[i][j].setText(self.guitar.notes[i][j])
                    self.frets[i][j].setImage(1)
        else:
            root = notes[0]
            for i in range(6):
                for j in range(self.fretboardNum):
                    for n in notes:
                        if n == self.guitar.notes[i][j].split('-')[0]:  # 和弦内或音阶内的音
                            self.frets[i][j].setText(self.guitar.notes[i][j])
                            if root == self.guitar.notes[i][j].split('-')[0]:  # 根音
                                self.frets[i][j].setImage(2)
                                break
                            else:  # 普通音
                                self.frets[i][j].setImage(1)
                                break
                        else:  # 非和弦内或音阶内的音
                            self.frets[i][j].setText('')
                            self.frets[i][j].setImage(0)

