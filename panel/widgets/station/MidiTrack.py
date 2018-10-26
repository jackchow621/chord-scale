# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, \
    QVBoxLayout, QDial, QGridLayout, QSpinBox

from PyQt5.Qt import *
from mingus.containers.track import *

from instrument.MusicalInstrument import MusicalInstrument
from panel.widgets.station.CustomDial import CustomDial
from panel.widgets.station.MidiBar import MidiBar


class MidiTrack(QWidget):
    trackDelSignal = pyqtSignal(object)
    trackChanProSignal = pyqtSignal(int, str)
    trackChanSignal = pyqtSignal(object)
    trackPlaySignal = pyqtSignal(object, int, int)  # track channel volume

    def __init__(self, channel=0, ins=None):
        super().__init__()
        self.channel = channel
        self.track = Track()
        self.instrument = ins
        self.volume = 100
        self.bars = []
        self.midiBars = []
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.selectInstrument(self.instrument), 0, 0, 1, 1)
        self.layout.addWidget(self.controlInstrument(), 0, 1, 2, 1)

        palette = QPalette()
        self.setAutoFillBackground(True)
        palette.setColor(self.backgroundRole(), QColor(112, 128, 144))
        self.barSection = QWidget()
        self.barSection.setPalette(palette)
        self.barScroll = QScrollArea()
        self.barScroll.setFixedHeight(100)
        self.barScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.barScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.barScroll.setWidgetResizable(True)
        self.barLayout = QGridLayout()
        self.barLayout.setAlignment(Qt.AlignLeft)
        self.barLayout.setSpacing(0)
        self.barLayout.setContentsMargins(0, 0, 0, 0)
        self.barLayoutIndex = 1  # to expand the layout (add button already exists)
        self.addBtn = QPushButton()
        self.addBtn.setFixedSize(QSize(100, 100))
        self.addBtn.setStyleSheet("QPushButton{border-image:url(images/add.png);}")
        self.addBtn.clicked.connect(self.addBar)
        self.barLayout.addWidget(self.addBtn, 0, 0)
        self.barSection.setLayout(self.barLayout)
        self.barScroll.setWidget(self.barSection)
        self.layout.addWidget(self.barScroll, 0, 2, 2, 1)

        self.barNum = 0
        self.setBarMaxNum()

        self.setFixedHeight(100)
        # self.setFixedWidth(1000)
        palette = QPalette()
        self.setAutoFillBackground(True)
        palette.setColor(self.backgroundRole(), QColor(47, 79, 79))
        # palette.setBrush(self.backgroundRole(),QBrush(QPixmap('../../../Document/images/17_big.jpg')))  # 设置背景图片
        self.setPalette(palette)

        self.setLayout(self.layout)

    def setBarMaxNum(self, num=16):
        self.maxBarNum = num

    def selectInstrument(self, ins=None):
        instrumentProp = InstrumentProp(self.channel, ins)
        instrumentProp.deleteSignal.connect(self.deleteTrack)
        instrumentProp.programSignal.connect(self.changeInstrumentProgram)
        return instrumentProp

    def controlInstrument(self):
        control = InstrumentControl()
        control.volSignal.connect(self.setVolume)
        return control

    def addBar(self):
        if (self.barNum < self.maxBarNum):
            self.lastBarDict = {}
            if len(self.bars) > 0:
                self.lastBarDict = self.midiBars[len(self.bars) - 1].dict
            b = MidiBar(self.lastBarDict)
            b.dict['instrument'] = self.instrument
            b.barDeleteSignal.connect(self.deleteBar)
            b.barChangeSignal.connect(self.changeBar)
            b.barPlaySignal.connect(self.playTrack)
            self.bars.append(b.bar)
            self.midiBars.append(b)
            self.barNum += 1
            self.barLayoutIndex += 1
            self.barLayout.addWidget(b, 0, self.barLayoutIndex, 2, 1)
            self.generateTrack()
        else:
            QMessageBox().information(self, '错误', '小节数不能超过' + str(self.maxBarNum))

    def deleteBar(self, midiBar):
        index = self.barLayout.indexOf(midiBar)
        self.barLayout.removeWidget(midiBar)
        midiBar.deleteLater()
        del (self.bars[index - 1])
        del (self.midiBars[index - 1])
        self.barNum -= 1
        self.generateTrack()

    def changeBar(self, midiBar):
        index = self.barLayout.indexOf(midiBar)
        # the bar has a ADD BUTTON ,which is self.barLayout[0]
        self.bars[index - 1] = midiBar.bar
        self.generateTrack()

    def playTrack(self, bar):
        t = Track()
        t.add_bar(bar)
        self.trackPlaySignal.emit(t, self.channel, self.volume)

    #  mingus didn't support replace bar
    # clear the track then add bars again
    def generateTrack(self):
        self.track.bars = []
        for bar in self.bars:
            if bar:
                self.track.add_bar(bar)
        # print(self.bars)
        self.trackChanSignal.emit(self)

    def deleteTrack(self):
        self.trackDelSignal.emit(self)

    def changeInstrumentProgram(self, program):
        self.instrument = program
        # set the instrument of each bar
        for mb in self.midiBars:
            mb.dict['instrument'] = self.instrument
        self.trackChanProSignal.emit(self.channel, program)

    def setVolume(self, value):
        self.volume = value


class InstrumentProp(QWidget):
    deleteSignal = pyqtSignal()
    programSignal = pyqtSignal(str)

    def __init__(self, channel, ins):
        super().__init__()
        self.instrument = MusicalInstrument()
        self.channel = channel
        self.ins = ins
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setContentsMargins(10, 10, 0, 0)
        self.insPic = QLabel()
        self.insLabel = QLineEdit()
        self.insLabel.setStyleSheet("background:transparent;color:white")
        self.layout.addWidget(self.insPic, 0, 0)
        self.layout.addWidget(self.insLabel, 1, 0)
        self.selectInstrument()
        self.setFixedWidth(100)
        self.setFixedHeight(100)
        self.setLayout(self.layout)
        self.setToolTip('midi channel:' + str(self.channel))

    def contextMenuEvent(self, QContextMenuEvent):
        self.mapper = QSignalMapper(self)
        menu = QMenu()

        delAction = QAction('delete')
        delAction.triggered.connect(self.deleteTrack)
        menu.addAction(delAction)
        menu.addSeparator()

        menu1 = QMenu('piano')
        for text in self.instrument.programs[:7]:
            action = QAction(text, self)
            self.mapper.setMapping(action, text)
            action.triggered.connect(self.mapper.map)
            menu1.addAction(action)

        menu2 = QMenu('guitar')
        for text in self.instrument.programs[24:31]:
            action = QAction(text, self)
            self.mapper.setMapping(action, text)
            # self.mapper.setMapping(action, text)
            action.triggered.connect(self.mapper.map)
            menu2.addAction(action)

        self.mapper.mapped['QString'].connect(self.selectInstrument)
        menu.addMenu(menu1)
        menu.addMenu(menu2)
        menu.exec_(QCursor.pos())

    def selectInstrument(self, ins=None):
        if ins == None:
            img = QImage(r'images/music.ico')
            ins = 'No instrument'
        elif 'Piano' in ins:
            img = QImage(r'images/piano.ico')
        elif 'Guitar' in ins:
            img = QImage(r'images/guitar.ico')
        else:
            return
        img = img.scaled(QSize(60, 60), Qt.IgnoreAspectRatio)
        self.insPic.resize(QSize(60, 60))
        self.insPic.setPixmap(QPixmap.fromImage(img))
        self.insLabel.setText(ins)
        if ins != 'No instrument':
            self.programSignal.emit(ins)

    def deleteTrack(self):
        self.deleteSignal.emit()


class InstrumentControl(QWidget):
    volSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setAutoFillBackground(True)
        # self.setStyleSheet('QWidget{border-right: 21px solid gray;background:#222222}')

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 5, 0, 5)

        self.volBtn = QPushButton()
        self.volBtn.setFixedSize(QSize(20, 20))
        self.volBtn.clicked.connect(self.setVolBtn)

        self.volCtl = CustomDial('volume')
        self.volCtl = QSlider()
        self.setVol(50)
        self.volCtl.setFixedHeight(65)
        self.volCtl.setStyleSheet('QSlider{background:#63B8FFborder-radius:2px;}')
        self.volCtl.valueChanged[int].connect(self.setVol)

        self.silentMode = False
        self.fakeVol = 0

        self.gainCtl = CustomDial('')

        self.chorusCtl = CustomDial('')

        self.chorusCtl1 = CustomDial('')

        self.layout.addWidget(self.volCtl, 0, 0)
        self.layout.addWidget(self.volBtn, 1, 0)
        '''self.layout.addWidget(self.gainCtl, 0, 1)
        self.layout.addWidget(self.chorusCtl, 1, 0)
        self.layout.addWidget(self.chorusCtl1, 1, 1)'''
        self.setLayout(self.layout)

    def setVol(self, value):
        self.volSignal.emit(value)
        if value == 0:
            self.volBtn.setStyleSheet('QPushButton{border-image:url(images/speaker2.png);}')
        else:
            self.volBtn.setStyleSheet('QPushButton{border-image:url(images/speaker.png);}')
        self.volCtl.setValue(value)
        self.volCtl.setToolTip(str(value))

    def setVolBtn(self):
        # If current mode is Silent mode,set value stored before to the vol-control,
        # and set silent mode to false
        if self.silentMode:
            self.setVol(self.fakeVol)
            self.silentMode = False
        # set silent mode to true(set vol = 0)
        # store current volume for reduction
        else:
            self.fakeVol = self.volCtl.value()
            self.setVol(0)
            self.silentMode = True
