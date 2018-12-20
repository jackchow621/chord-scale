# -*- coding: utf-8 -*-
import time
from queue import Queue
from threading import Thread, Event

from mingus.containers import Track

from instrument.MusicalInstrument import MusicalInstrument


class StationSequencer():
    paragraphNum = 0
    trackNum = 0
    barNum = 0
    beat = 120

    tracks = []

    def __init__(self):
        pass
        self.instrument = MusicalInstrument('ARACHNO')

    # stopped 0
    # playing 1
    # paused 2
    def play(self, tracks, channels, volumes, playState):
        # 如果是停止状态，即从头播放，重新创建线程
        if playState == 0:
            self.tracks = tracks
            self.channels = channels
            self.volumes = volumes

            evt = Event()
            q = Queue()
            self.playThread = PlayProcess(0, evt, q, [tracks, channels, volumes, self.instrument])
            self.stopThread = PlayProcess(1, evt, q, [tracks, channels, volumes, self.instrument])

            self.playThread.start()
            self.stopThread.start()

        if playState == 2:  # 如果是暂停状态，将线程恢复
            self.stopThread.resume()

    def pause(self):
        try:
            self.stopThread.pause()
        except Exception as ex:
            print('Not playing')

    def stop(self):
        try:
            self.stopThread.stop()
        except Exception as ex:
            print('Not playing')

    def changeProgram(self, channel, program):
        self.instrument.changeProgram(self.instrument.programs.index(program), channel)


class PlayProcess(Thread):
    def __init__(self, threadFlag, evt, queue, args=None):
        Thread.__init__(self)
        # 初始化
        self.threadFlag = threadFlag
        self.evt = evt
        self.queue = queue
        self.args = args
        self.current_bar = 0
        self.finished = False

    def run(self):
        # Play the bars
        while self.current_bar < len(self.args[0][0]):
            if self.threadFlag == 0:
                print('playing...', self.current_bar)
                if self.queue.empty():
                    playbars = []
                    for tr in self.args[0]:
                        if len(tr) != 0:
                            playbars.append(tr[self.current_bar])
                    self.args[3].playBars(playbars, self.args[1], self.args[2])
                    self.current_bar += 1
                    if self.current_bar == len(self.args[0][0]) - 1:
                        self.finished = True
                else:
                    flag = self.queue.get()
                    print('flag:',flag)
                    if flag == 'pause':
                        self.evt.wait()
                    else:
                        break

    def pause(self):
        self.queue.put('pause')

    def resume(self):
        self.evt.set()

    def stop(self):
        self.current_bar = 0
        self.queue.put('stop')

    def isFinished(self):
        return self.finished
