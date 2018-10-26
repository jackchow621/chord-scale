# -*- coding: utf-8 -*-
import collections
from PyQt5.Qt import *

from panel.widgets.station.CustomDial import CustomDial
from panel.widgets.station.MidiTrack import MidiTrack
from sounds.StationSequencer import StationSequencer


class StationTab(QWidget):
    trackIndex = range(16)
    usedIndex = []

    def __init__(self):
        self.trackNum = 0
        self.sequencer = StationSequencer()
        self.midiTracks = [None] * 16
        self.playState = False
        self.isReplay = False
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.controlArea())

        self.station = QWidget()
        # self.station.setFixedWidth(1366)
        self.stationScroll = QScrollArea()
        self.stationScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.stationScroll.setWidgetResizable(True)
        self.trackLayout = QGridLayout()
        self.trackLayout.setAlignment(Qt.AlignTop)
        self.addTrackBtn = QPushButton()
        self.addTrackBtn.setFixedSize(QSize(100, 100))
        self.addTrackBtn.clicked.connect(self.addTrack)
        self.addTrackBtn.setStyleSheet("QPushButton{border-image:url(images/ins.png);}");
        self.trackLayout.addWidget(self.addTrackBtn, 0, 0)
        self.trackLayoutIndex = 1  # to expand the layout (notice:add button already exists)
        palette = QPalette()
        self.setAutoFillBackground(True)
        palette.setColor(self.backgroundRole(), QColor(202, 225, 255))
        # palette.setBrush(self.backgroundRole(),QBrush(QPixmap('../../../Document/images/17_big.jpg')))  # 设置背景图片
        self.setPalette(palette)
        self.station.setLayout(self.trackLayout)
        self.stationScroll.setWidget(self.station)
        self.layout.addWidget(self.stationScroll)
        self.setLayout(self.layout)

    def addTrack(self, ins=None):
        if self.trackNum > 15:
            QMessageBox().information(self, '错误', '轨数不能超过15')
            return
        self.trackLayoutIndex += 1
        self.trackNum += 1
        index = self.getFreeChannel()
        self.usedIndex.append(index)
        t = MidiTrack(index, ins)
        self.midiTracks[t.channel] = t
        try:
            t.trackDelSignal.connect(self.deleteTrack)
        except Exception as s:
            print(s)
        t.trackChanProSignal.connect(self.changeTrackProgram)
        t.trackChanSignal.connect(self.changeTrack)
        t.trackPlaySignal.connect(self.playTrack)
        self.trackLayout.removeWidget(self.addTrackBtn)
        self.trackLayout.addWidget(t, self.trackLayoutIndex, 0)
        self.trackLayout.addWidget(self.addTrackBtn, self.trackLayoutIndex + 1, 0)

        self.test_show()

    def changeTrack(self, midiTrack):
        self.midiTracks[midiTrack.channel] = midiTrack

        self.test_show()

    def changeTrackProgram(self, channel, program):
        self.sequencer.changeProgram(channel, program)

    def deleteTrack(self, midiTrack):
        self.trackNum -= 1
        self.trackLayout.removeWidget(midiTrack)
        midiTrack.deleteLater()
        self.midiTracks[midiTrack.channel] = None
        self.usedIndex.remove(midiTrack.channel)

        self.test_show()

    def playTrack(self, track, index, vol):
        self.sequencer.play([track], [index], [vol], False)

    def test_show(self):
        self.str1 = ''
        for ind in self.usedIndex:
            self.str1 += 'u:' + str(ind) + '(chanel:' + str(self.midiTracks[ind].channel) + ')***'
        self.test.setText(self.str1)

        self.str2 = ''
        for ind in self.usedIndex:
            self.str2 += 'u:' + str(ind) + '(chanel:' + str(self.midiTracks[ind].track) + ')\r\n'
        self.set.setText(self.str2)

    def playSound(self):
        # stopped 0
        # playing 1
        # paused 2
        if self.playState == 1:  # while the sequencer is playing,set to pause state.Pause state has a PLAY ico
            self.playBtn.setStyleSheet("QPushButton{border-image:url(images/play.png);min-width: 60;min-height: 60;}");
            self.sequencer.pause()
            self.playState = 2
        elif self.playState in (0, 2):  # while the sequencer is paused or stopped,start to play and set to play state
            self.playBtn.setStyleSheet("QPushButton{border-image:url(images/pause.png);min-width: 60;min-height: 60;}");
            tracks = []
            vols = []
            for t in self.midiTracks:
                if t != None and t.track:
                    tracks.append(t.track)
                    vols.append(t.volume)
            if len(tracks) > 0:
                try:
                    self.sequencer.play(tracks, self.usedIndex, vols, self.playState)
                    self.playState = 1
                except Exception as ex:
                    QMessageBox().information(self, '播放错误', str(ex))

    def stopSound(self):
        self.playBtn.setStyleSheet("QPushButton{border-image:url(images/play.png);min-width: 60;min-height: 60;}");
        self.playState = 0
        self.sequencer.stop()

    # get a channel which hadn't been used
    # midi channel : 0 to 15
    def getFreeChannel(self):
        unusedIndex = set(self.trackIndex).difference(self.usedIndex)
        return list(unusedIndex)[0]

    def controlArea(self):
        select = QWidget()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        self.test = QLabel('add')
        self.set = QLabel('set')

        self.playBtn = QPushButton()
        self.playBtn.setStyleSheet("QPushButton{border-image:url(images/play.png);min-width: 60;min-height: 60;}");
        self.playBtn.clicked.connect(self.playSound)
        self.stopBtn = QPushButton()
        self.stopBtn.setStyleSheet("QPushButton{border-image:url(images/stop.png);min-width: 60;min-height: 60;}");
        self.stopBtn.clicked.connect(self.stopSound)
        self.pre = QPushButton()
        self.pre.setStyleSheet("QPushButton{border-image:url(images/previous.png);min-width: 60;min-height: 60;}");
        self.next = QPushButton()
        self.next.setStyleSheet("QPushButton{border-image:url(images/next.png);min-width: 60;min-height: 60;}");

        layout.addWidget(self.pre, 0, 0)
        layout.addWidget(self.playBtn, 0, 1)
        layout.addWidget(self.stopBtn, 0, 2)
        layout.addWidget(self.next, 0, 3)
        # layout.addWidget(self.test, 0, 4)
        # layout.addWidget(self.set, 1, 4)

        # gain group
        gainGroup = QGroupBox('Gain')
        gainLabel = QLabel('gain:')
        gainDial = CustomDial('gain')
        l1 = QGridLayout()
        l1.setSpacing(5)
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(gainLabel, 0, 0)
        l1.addWidget(gainDial, 1, 0)
        gainGroup.setLayout(l1)
        layout.addWidget(gainGroup, 0, 4, 2, 1)

        # reverb group
        reverbGroup = QGroupBox('Reverb')
        reverbRoomLabel = QLabel('room:')
        reverbRoomDial = CustomDial('room')
        reverbDampLabel = QLabel('damp:')
        reverbDampDial = CustomDial('damp')
        reverbWidthLabel = QLabel('width:')
        reverbWidthDial = CustomDial('width')
        reverbLevelDLabel = QLabel('level:')
        reverbLevelDial = CustomDial('level')
        l2 = QGridLayout()
        l2.setSpacing(5)
        l2.setContentsMargins(0, 0, 0, 0)
        l2.addWidget(reverbRoomLabel, 0, 0)
        l2.addWidget(reverbRoomDial, 1, 0)
        l2.addWidget(reverbDampLabel, 0, 1)
        l2.addWidget(reverbDampDial, 1, 1)
        l2.addWidget(reverbWidthLabel, 0, 2)
        l2.addWidget(reverbWidthDial, 1, 2)
        l2.addWidget(reverbLevelDLabel, 0, 3)
        l2.addWidget(reverbLevelDial, 1, 3)
        reverbGroup.setLayout(l2)
        layout.addWidget(reverbGroup, 0, 5, 2, 1)

        # chorus group
        chorusGroup = QGroupBox('Chorus')
        chorusNLabel = QLabel('N:')
        chorusNDial = CustomDial('N')
        chorusLevelLabel = QLabel('level:')
        chorusLevelDial = CustomDial('level')
        chorusSpeedLabel = QLabel('speed:')
        chorusSpeedDial = CustomDial('speed')
        chorusDepthLabel = QLabel('depth:')
        chorusDepthDial = CustomDial('depth')
        l3 = QGridLayout()
        l3.setSpacing(5)
        l3.setContentsMargins(0, 0, 0, 0)
        l3.addWidget(chorusNLabel, 0, 0)
        l3.addWidget(chorusNDial, 1, 0)
        l3.addWidget(chorusLevelLabel, 0, 1)
        l3.addWidget(chorusLevelDial, 1, 1)
        l3.addWidget(chorusSpeedLabel, 0, 2)
        l3.addWidget(chorusSpeedDial, 1, 2)
        l3.addWidget(chorusDepthLabel, 0, 3)
        l3.addWidget(chorusDepthDial, 1, 3)
        chorusGroup.setLayout(l3)
        layout.addWidget(chorusGroup, 0, 6, 2, 1)

        select.setLayout(layout)
        return select
