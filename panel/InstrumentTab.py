# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QComboBox, \
    QVBoxLayout, QRadioButton, QTabWidget, QGroupBox, QDial, QGridLayout
from PyQt5.QtCore import Qt
from instrument.MusicalInstrument import MusicalInstrument
from panel.InstrumentPanel import InstrumentPanel
from chord import chord


class InstrumentTab(QWidget):
    INSTRUMENT_INDEX = 0

    def __init__(self):
        super().__init__()
        self.instrument = MusicalInstrument()
        self.chord = chord()
        self.initUI()
        self.bindEvent()

    def initUI(self):
        self.layout = QVBoxLayout()
        # 往上对齐
        self.layout.setAlignment(Qt.AlignTop)

        # 查询条件
        self.hbox = QGridLayout()
        self.hbox.setSpacing(1)

        # 和弦/音阶选择条件区域
        rootLabel = QLabel('根音')
        self.rootCombo = QComboBox()
        self.rootCombo.addItems(self.instrument.roots)
        self.rootCombo.setMinimumWidth(100)
        proLabel = QLabel('三音')
        self.proCombo = QComboBox()
        self.proCombo.addItems(self.instrument.pros)
        self.proCombo.setMinimumWidth(100)
        intervelLabel = QLabel('五音')
        self.intervelCombo = QComboBox()
        self.intervelCombo.addItems(self.instrument.intervals)
        self.intervelCombo.setMinimumWidth(100)
        self.mode = 0  # 0:scale mode ; 1:chord mode
        self.scaCheck = QRadioButton('音阶')
        self.scaCheck.setChecked(True)
        self.chordCheck = QRadioButton('和弦')
        scaleLabel = QLabel('音阶')
        self.scaleCombo = QComboBox()
        self.scaleCombo.addItems(self.instrument.scales)
        self.scaleCombo.setMinimumWidth(100)

        commonBox = QGroupBox('音阶/和弦')
        commonBox.setStyleSheet("QGroupBox{ border: 1px groove grey; border-radius:5px;border-style: outset;}")
        commonLayout = QGridLayout()
        commonBox.setLayout(commonLayout)
        commonLayout.addWidget(self.scaCheck, 0, 0)
        commonLayout.addWidget(self.chordCheck, 0, 1)
        commonLayout.addWidget(scaleLabel, 0, 2)
        commonLayout.addWidget(self.scaleCombo, 0, 3, 1, 3)
        commonLayout.addWidget(rootLabel, 1, 0)
        commonLayout.addWidget(self.rootCombo, 1, 1)
        commonLayout.addWidget(proLabel, 1, 2)
        commonLayout.addWidget(self.proCombo, 1, 3)
        commonLayout.addWidget(intervelLabel, 1, 4)
        commonLayout.addWidget(self.intervelCombo, 1, 5)

        # 控制条件区域
        self.fretLabel = QLabel('品数')
        self.guitarSlider = QDial()
        self.guitarSlider.setNotchesVisible(True)
        self.guitarSlider.setMaximumHeight(60)
        self.guitarSlider.setToolTip('21')
        self.guitarSlider.setMinimum(12)
        self.guitarSlider.setMaximum(24)
        self.guitarSlider.setValue(21)
        # piano
        self.pianoSlider = QDial()
        self.pianoSlider.setNotchesVisible(True)
        self.pianoSlider.setMaximumHeight(60)
        self.pianoSlider.setToolTip('4')
        self.pianoSlider.setMinimum(3)
        self.pianoSlider.setMaximum(7)
        self.pianoSlider.setValue(4)
        self.pianoSlider.hide()

        self.speedLabel = QLabel('播放速度')
        self.speedSlider = QDial()
        self.speedSlider.setNotchesVisible(True)
        self.speedSlider.setMaximumHeight(60)
        self.speedLabel.setToolTip('4')
        self.speedSlider.setMinimum(1)
        self.speedSlider.setMaximum(6)
        self.speedSlider.setValue(4)
        self.speed = 0.25

        instLabel = QLabel('音色')
        self.guitarInstCheck = QComboBox()
        self.guitarInstCheck.addItems(
            list(self.instrument.programs[24:31]))  # Arachno SoundFont - Version 1.0     024~030

        self.pianoInstCheck = QComboBox()
        self.pianoInstCheck.addItems(
            list(self.instrument.programs[:7]))  # Arachno SoundFont - Version 1.0     0~6
        self.pianoInstCheck.hide()

        pos = ['-', 'C', 'A', 'G', 'E', 'D', '3-note-per-string']
        self.posLabel = QLabel('把位')
        self.posCombo = QComboBox()
        self.posCombo.addItems(pos)
        self.posCombo.setMinimumWidth(100)

        controlBox = QGroupBox('控制')
        controlBox.setStyleSheet("QGroupBox{ border: 1px groove grey; border-radius:5px;border-style: outset;}")
        self.controlLayout = QGridLayout()
        controlBox.setLayout(self.controlLayout)
        self.controlLayout.addWidget(self.guitarSlider, 0, 0)
        self.controlLayout.addWidget(self.fretLabel, 1, 0)
        self.controlLayout.addWidget(self.speedSlider, 0, 1)
        self.controlLayout.addWidget(self.speedLabel, 1, 1)
        self.controlLayout.addWidget(instLabel, 0, 2)
        self.controlLayout.addWidget(self.guitarInstCheck, 0, 3)
        self.controlLayout.addWidget(self.posLabel, 1, 2)
        self.controlLayout.addWidget(self.posCombo, 1, 3)

        self.generateBtn = QPushButton('生成')
        self.generateBtn.setMaximumWidth(100)
        self.generateBtn.setStyleSheet(
            "QPushButton{border:1px groove grey;border-radius:5px;border-style:outset; min-height:40px;}")
        self.playBtn = QPushButton('播放')
        self.playBtn.setMaximumWidth(100)
        self.playBtn.setStyleSheet(
            "QPushButton{border:1px groove grey;border-radius:5px;border-style:outset;min-height:40px;}")

        self.hbox.addWidget(commonBox, 0, 0, 2, 1)
        self.hbox.addWidget(controlBox, 0, 2, 2, 1)
        self.hbox.addWidget(self.generateBtn, 0, 3)
        self.hbox.addWidget(self.playBtn, 1, 3)
        self.hbox.addWidget(QWidget(), 0, 4, 2, 1)  # 占位

        # 垂直布局
        self.layout.addLayout(self.hbox)
        self.tabBox = QTabWidget()
        self.panels = InstrumentPanel(self.instrument).createInstrumentPanel(['Guitar', 'Piano'])
        for pn in self.panels:
            self.tabBox.addTab(pn, pn.name)

        self.switchMode()
        self.layout.addWidget(self.tabBox)
        self.setLayout(self.layout)

    def bindEvent(self):
        self.guitarSlider.valueChanged[int].connect(self.reDrawInstrument)
        self.pianoSlider.valueChanged[int].connect(self.reDrawInstrument)
        self.speedSlider.valueChanged[int].connect(self.switchSpeed)
        self.generateBtn.clicked.connect(self.reDrawInstrument)
        self.scaCheck.toggled.connect(self.switchMode)
        self.chordCheck.toggled.connect(self.switchMode)
        self.guitarInstCheck.currentTextChanged.connect(self.changeProgram)
        self.pianoInstCheck.currentTextChanged.connect(self.changeProgram)
        self.playBtn.clicked.connect(self.playSound)
        self.tabBox.currentChanged.connect(self.activeInstrument)

    # change the current instrument panel,show or hide the corresponding widget
    def activeInstrument(self, value):
        self.INSTRUMENT_INDEX = value
        if self.INSTRUMENT_INDEX == 0:  # GUITAR
            self.pianoSlider.hide()
            self.guitarSlider.show()
            self.pianoInstCheck.hide()
            self.guitarInstCheck.show()
            self.controlLayout.replaceWidget(self.pianoSlider, self.guitarSlider)
            self.controlLayout.replaceWidget(self.pianoInstCheck, self.guitarInstCheck)
            self.posLabel.setEnabled(True)
            self.posCombo.setEnabled(True)
            self.fretLabel.setText('品数')
        elif self.INSTRUMENT_INDEX == 1:  # PIANO
            self.pianoSlider.show()
            self.guitarSlider.hide()
            self.pianoInstCheck.show()
            self.guitarInstCheck.hide()
            self.controlLayout.replaceWidget(self.guitarSlider, self.pianoSlider)
            self.controlLayout.replaceWidget(self.guitarInstCheck, self.pianoInstCheck)
            self.posLabel.setEnabled(False)
            self.posCombo.setEnabled(False)
            self.fretLabel.setText('八度')

    def reDrawInstrument(self):
        notes = self.getNotes()

        if self.panels[self.INSTRUMENT_INDEX].name == 'Guitar':
            freStr = 'Fret num [' + str(self.guitarSlider.value()) + ']'
            self.guitarSlider.setToolTip(str(self.guitarSlider.value()))
            fretPosition = '\r\n[Guitar board position] POSITION ' + self.posCombo.currentText()
            sound = self.guitarInstCheck.currentText()
            if len(notes) > 1:
                notes1 = []
                for note in notes:
                    notes1.append(note.split('-')[0])
                mode = self.scaleCombo.currentText() if self.mode == 0 else '-'
                self.panels[self.INSTRUMENT_INDEX].initPanel(int(self.guitarSlider.value()), notes1,
                                                             mode,
                                                             self.posCombo.currentText())
        elif self.panels[self.INSTRUMENT_INDEX].name == 'Piano':
            freStr = 'Octave num [' + str(self.pianoSlider.value()) + ']'
            self.pianoSlider.setToolTip(str(self.pianoSlider.value()))
            fretPosition = ''
            sound = self.pianoInstCheck.currentText()
            if len(notes) > 1:
                self.panels[self.INSTRUMENT_INDEX].initPanel(int(self.pianoSlider.value()), notes)
        else:
            pass

        infoStr = '[Instrument] ' + self.panels[self.INSTRUMENT_INDEX].name
        infoStr = infoStr + '\r\n[Program] ' + sound
        infoStr = infoStr + '\r\n[Scope] ' + freStr
        infoStr = infoStr + '\r\n[Note mode] ' + ('scale' if self.mode == 0 else 'chord')
        infoStr = infoStr + '\r\n[Key] ' + notes[0]
        infoStr = infoStr + '\r\n[Notes] ' + str(notes)
        infoStr = infoStr + fretPosition
        infoStr = infoStr + '\r\n[Speed] ' + str(self.speed) + ' seconds'
        self.panels[self.INSTRUMENT_INDEX].detail.setText(infoStr)

    def switchMode(self):
        self.mode = self.scaCheck.isChecked()
        self.mode = self.chordCheck.isChecked()
        if self.mode == 0:  # scale
            self.scaCheck.setChecked(True)
            self.chordCheck.setChecked(False)
            self.scaleCombo.setEnabled(True)
            self.proCombo.setEnabled(False)
            self.intervelCombo.setEnabled(False)
        else:  # chord
            self.scaCheck.setChecked(False)
            self.chordCheck.setChecked(True)
            self.scaleCombo.setEnabled(False)
            self.proCombo.setEnabled(True)
            self.intervelCombo.setEnabled(True)

    def switchSpeed(self, value):
        sp = {1: 1, 2: 0.75, 3: 0.5, 4: 0.25, 5: 0.1, 6: 0.05}
        self.speed = sp.get(value)
        self.speedSlider.setToolTip(str(self.speed))

    # change instrument's program
    def changeProgram(self, value):
        self.panels[self.INSTRUMENT_INDEX].changeProgram(value)

    # play a note or chord
    def playSound(self):
        notes = self.getNotes()
        if len(notes) > 1:
            self.panels[self.INSTRUMENT_INDEX].playArpeggio(notes, self.speed)

    # get all notes
    def getNotes(self):
        if self.mode == 0:  # scale
            notes = list(self.chord.getScales(self.rootCombo.currentText(),
                                              self.scaleCombo.currentText()).values())
        else:  # chord
            notes = list(self.chord.getChord(self.rootCombo.currentText(),
                                             self.proCombo.currentText(),
                                             self.intervelCombo.currentText()).values())
        return notes
