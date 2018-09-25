# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QComboBox, \
    QVBoxLayout, QSlider, QRadioButton, QTabWidget, QGroupBox
from PyQt5.QtCore import Qt
from Instrument.MusicalInstrument import MusicalInstrument
from Panel.InstrumentPanel import InstrumentPanel
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
        self.vbox = QVBoxLayout()
        # 往上对齐
        self.vbox.setAlignment(Qt.AlignTop)

        # 查询条件
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(10)

        commonBox = QGroupBox('音阶/和弦')
        commonBox.setStyleSheet("QGroupBox{ border: 1px groove grey; border-radius:5px;border-style: outset;}")

        rootLabel = QLabel('根音')
        self.rootCombo = QComboBox(commonBox)
        self.rootCombo.addItems(self.instrument.roots)
        self.rootCombo.setMinimumWidth(150)
        proLabel = QLabel('三音')
        self.proCombo = QComboBox(commonBox)
        self.proCombo.addItems(self.instrument.pros)
        self.proCombo.setMinimumWidth(150)
        invervelLabel = QLabel('五音')
        self.invervelCombo = QComboBox(commonBox)
        self.invervelCombo.addItems(self.instrument.intervals)
        self.invervelCombo.setMinimumWidth(150)
        scaleLabel = QLabel('音阶类型')
        self.scaleCombo = QComboBox(commonBox)
        self.scaleCombo.addItems(self.instrument.scales)
        self.scaleCombo.setMinimumWidth(150)

        commonLayout = QHBoxLayout()
        commonLayout.setAlignment(Qt.AlignRight)
        commonLayout.addWidget(rootLabel)
        commonLayout.addWidget(self.rootCombo)
        commonLayout.addWidget(proLabel)
        commonLayout.addWidget(self.proCombo)
        commonLayout.addWidget(invervelLabel)
        commonLayout.addWidget(self.invervelCombo)
        commonLayout.addWidget(scaleLabel)
        commonLayout.addWidget(self.scaleCombo)

        commonBox.setLayout(commonLayout)

        self.guitarSlider = QSlider(Qt.Horizontal, self)
        self.guitarSlider.setFixedWidth(300)
        self.guitarSlider.setMinimum(12)
        self.guitarSlider.setMaximum(24)
        self.guitarSlider.setValue(21)

        self.pianoSlider = QSlider(Qt.Horizontal, self)
        self.pianoSlider.setFixedWidth(300)
        self.pianoSlider.setMinimum(3)
        self.pianoSlider.setMaximum(7)
        self.pianoSlider.setValue(4)

        self.pianoSlider.hide()

        self.fretLabel = QLabel('品数:21')

        self.mode = 0  # 0:scale mode ; 1:chord mode
        self.scaCheck = QRadioButton('音阶')
        self.scaCheck.setChecked(True)

        self.chordCheck = QRadioButton('和弦')

        instLabell = QLabel('音色')
        self.guitarInstCheck = QComboBox()
        self.guitarInstCheck.addItems(
            list(self.instrument.programs[24:31]))  # Arachno SoundFont - Version 1.0     024~030

        self.pianoInstCheck = QComboBox()
        self.pianoInstCheck.addItems(
            list(self.instrument.programs[:7]))  # Arachno SoundFont - Version 1.0     024~030

        self.pianoInstCheck.hide()

        self.generateBtn = QPushButton('生成')

        self.playBtn = QPushButton('播放')

        self.hbox.addWidget(commonBox)
        self.hbox.addWidget(QWidget())
        self.hbox.setStretch(0, 1)
        self.hbox.addWidget(instLabell)
        self.hbox.addWidget(self.guitarInstCheck)
        self.hbox.addWidget(self.scaCheck)
        self.hbox.addWidget(self.chordCheck)
        self.hbox.addWidget(self.fretLabel)
        self.hbox.addWidget(self.guitarSlider)
        self.hbox.addWidget(self.generateBtn)
        self.hbox.addWidget(self.playBtn)

        # 垂直布局
        self.vbox.addLayout(self.hbox)

        self.tabBox = QTabWidget()

        self.panels = InstrumentPanel(self.instrument).createInstrumentPanel(['Guitar', 'Piano'])
        for pn in self.panels:
            self.tabBox.addTab(pn, pn.name)

        self.vbox.addWidget(self.tabBox)
        self.setLayout(self.vbox)

    def bindEvent(self):
        self.guitarSlider.valueChanged[int].connect(self.reDrawInstrument)
        self.pianoSlider.valueChanged[int].connect(self.reDrawInstrument)
        self.generateBtn.clicked.connect(self.reDrawInstrument)
        self.scaCheck.toggled.connect(self.switchMode)
        self.chordCheck.toggled.connect(self.switchMode)
        self.guitarInstCheck.currentTextChanged.connect(self.changeInstrumentProgram)
        self.pianoInstCheck.currentTextChanged.connect(self.changeInstrumentProgram)
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
            self.hbox.replaceWidget(self.pianoSlider, self.guitarSlider)
            self.hbox.replaceWidget(self.pianoInstCheck, self.guitarInstCheck)
            self.fretLabel.setText('品数:' + str(self.guitarSlider.value()))
        elif self.INSTRUMENT_INDEX == 1:  # PIANO
            self.pianoSlider.show()
            self.guitarSlider.hide()
            self.pianoInstCheck.show()
            self.guitarInstCheck.hide()
            self.hbox.replaceWidget(self.guitarSlider, self.pianoSlider)
            self.hbox.replaceWidget(self.guitarInstCheck, self.pianoInstCheck)
            self.fretLabel.setText('八度:' + str(self.pianoSlider.value()))

    def reDrawInstrument(self):
        notes = self.getNotes()
        if self.panels[self.INSTRUMENT_INDEX].name == 'Guitar':
            freStr = 'Fret num ' + str(self.guitarSlider.value())
            sound = self.guitarInstCheck.currentText()
            self.panels[self.INSTRUMENT_INDEX].initPanel(int(self.guitarSlider.value()), notes)
        elif self.panels[self.INSTRUMENT_INDEX].name == 'Piano':
            freStr = 'Octave num ' + str(self.pianoSlider.value())
            sound = self.pianoInstCheck.currentText()
            self.panels[self.INSTRUMENT_INDEX].initPanel(int(self.pianoSlider.value()), notes)
        else:
            pass
        self.fretLabel.setText(freStr)

        infoStr = '[instrument] ' + self.panels[self.INSTRUMENT_INDEX].name
        infoStr = infoStr + '\r\n[program] ' + sound
        infoStr = infoStr + '\r\n[scope] ' + freStr
        infoStr = infoStr + '\r\n[note mode] ' + ('scale' if self.mode == 0 else 'chord')
        infoStr = infoStr + '\r\n[notes] ' + str(notes)
        self.panels[self.INSTRUMENT_INDEX].detail.setText(infoStr)

    def switchMode(self):
        self.mode = self.scaCheck.isChecked()
        self.mode = self.chordCheck.isChecked()
        if self.mode == 0:  # scale
            self.scaCheck.setChecked(True)
            self.chordCheck.setChecked(False)
        else:  # chord
            self.scaCheck.setChecked(False)
            self.chordCheck.setChecked(True)

    # change instrument's program
    def changeInstrumentProgram(self, value):
        self.panels[self.INSTRUMENT_INDEX].changeProgram(value)

    # play a note or chord
    def playSound(self):
        self.panels[self.INSTRUMENT_INDEX].playNote(self.getNotes())

    def getNotes(self):
        if self.mode == 0:  # scale
            notes = list(self.chord.getScales(self.rootCombo.currentText(),
                                              self.scaleCombo.currentText()).values())
        else:  # chord
            notes = list(self.chord.getChord(self.rootCombo.currentText(),
                                             self.proCombo.currentText(),
                                             self.invervelCombo.currentText()).values())
        return notes
