# -*- coding: utf-8 -*-

from mingus.containers import Note
from sounds import myfluidsynth
import time

# 重要：font中，bank指的是0,128  ； preset指音色，如grand piano。可通过列出支持的bank或preset
# >>fluidsynth.exe "c:\sounds\arachno-soundfont-10-sf2\Arachno SoundFont - Version 1.0.sf2"
# >>inst 1

class sound():
    instruments = {'ARACHNO': r'C:\sounds\arachno-soundfont-10-sf2\Arachno SoundFont - Version 1.0.sf2'}
    speed = 1.0

    def __init__(self, instrument):
        assert instrument in list(self.instruments.keys())
        self.synth = myfluidsynth.Synth()
        self.synth.start()
        self.loadSoundFont(self.instruments.get(instrument))

    def loadSoundFont(self, path):
        self.synth.sfunload()
        self.synth.sfload(path)
        self.setInstrument(0, 0, 0)

    def listInstrument(self, chanel):
        pass

    def setInstrument(self, channel, program=0, bank=0):
        return self.synth.program_select(channel, bank, program)

    def destroy(self):
        self.synth.sfunload()
        self.synth.delete()

    def playNote(self, note, channel=0, velocity=100):
        if isinstance(note, Note):
            self.synth.noteon(channel, int(note) + 12, velocity)
        else:
            self.synth.noteon(channel, int(Note(note)) + 12, velocity)

    def stopNote(self, note, channel=1):
        self.synth.noteoff(channel, int(Note(note)) + 12)

    def playNoteContainer(self, nc, channel=1, velocity=100):
        for note in nc:
            self.playNote(note, channel, velocity)

    def stopNoteContainer(self, nc, channel=1):
        for note in nc:
            self.stopNote(note, channel)

    def playBar(self, bar, channel=1, bpm=120):
        qn_length = 60.0 / bpm
        for nc in bar:
            self.playNoteContainer(nc[2], channel, 100)
            if hasattr(nc[2], 'bpm'):
                bpm = nc[2].bpm
                qn_length = 60.0 / bpm
            ms = qn_length * (4.0 / nc[1])
            self.synth.sleep(ms)
            self.stopNoteContainer(nc[2], channel)
        return {'bpm': bpm}

    def playBars(self, bars, channels, bpm=120):
        qn_length = 60.0 / bpm  # length of a quarter note
        tick = 0.0  # place in beat from 0.0 to bar.length
        cur = [0] * len(bars)  # keeps the index of the NoteContainer under
        # investigation in each of the bars
        playing = []  # The NoteContainers being played.

        while tick < bars[0].length:
            # Prepare a and play a list of NoteContainers that are ready for it.
            # The list `playing_new` holds both the duration and the
            # NoteContainer.
            playing_new = []
            for (n, x) in enumerate(cur):
                (start_tick, note_length, nc) = bars[n][x]
                if start_tick <= tick:
                    self.playNoteContainer(nc, channels[n])
                    playing_new.append([note_length, n])
                    playing.append([note_length, nc, channels[n], n])

                    # Change the length of a quarter note if the NoteContainer
                    # has a bpm attribute
                    if hasattr(nc, 'bpm'):
                        bpm = nc.bpm
                        qn_length = 60.0 / bpm

            # Sort the list and sleep for the shortest duration
            if len(playing_new) != 0:
                playing_new.sort()
                shortest = playing_new[-1][0]
                ms = qn_length * (4.0 / shortest)
                self.synth.sleep(ms)
            else:
                # If somehow, playing_new doesn't contain any notes (something
                # that shouldn't happen when the bar was filled properly), we
                # make sure that at least the notes that are still playing get
                # handled correctly.
                if len(playing) != 0:
                    playing.sort()
                    shortest = playing[-1][0]
                    ms = qn_length * (4.0 / shortest)
                    self.synth.sleep(ms)
                else:
                    # warning: this could lead to some strange behaviour. OTOH.
                    # Leaving gaps is not the way Bar works. should we do an
                    # integrity check on bars first?
                    return {}

            # Add shortest interval to tick
            tick += 1.0 / shortest

            # This final piece adjusts the duration in `playing` and checks if a
            # NoteContainer should be stopped.
            new_playing = []
            for (length, nc, chan, n) in playing:
                duration = 1.0 / length - 1.0 / shortest
                if duration >= 0.00001:
                    new_playing.append([1.0 / duration, nc, chan, n])
                else:
                    self.stopNoteContainer(nc, chan)
                    if cur[n] < len(bars[n]) - 1:
                        cur[n] += 1
            playing = new_playing

        for p in playing:
            self.stopNoteContainer(p[1], p[2])
            playing.remove(p)
        return {'bpm': bpm}

    def playTrack(self, track, channel=1, bpm=120):
        """Play a Track object."""
        for bar in track:
            res = self.playBar(bar, channel, bpm)
            if res != {}:
                bpm = res['bpm']
            else:
                return {}
        return {'bpm': bpm}

    def playTracks(self, tracks, channels, programs=[], bpm=120):
        """Play a list of Tracks.

                If an instance of MidiInstrument is used then the instrument will be
                set automatically.
                """
        # Set the right instruments
        for x in range(len(tracks)):
            '''instr = tracks[x].instrument
            if isinstance(instr, MidiInstrument):
                try:
                    i = instr.names.index(instr.name)
                except:
                    i = 1
                self.set_instrument(channels[x], i)
            else:
                self.set_instrument(channels[x], 1)'''
            if len(programs) == 0:
                self.setInstrument(channels[x], 0)
            else:
                self.setInstrument(channels[x], programs[x])
        current_bar = 0
        max_bar = len(tracks[0])

        # Play the bars
        while current_bar < max_bar:
            playbars = []
            for tr in tracks:
                playbars.append(tr[current_bar])
            res = self.playBars(playbars, channels, bpm)
            if res != {}:
                bpm = res['bpm']
            else:
                return {}
            current_bar += 1
        return {'bpm': bpm}

    def playComposition(self, composition, channels=None, bpm=120):
        return self.synth.play_Composition(composition, channels, bpm)

    def controlChange(self, channel, control, value):
        return self.synth.control_change(channel, control, value)

    def stopEverything(self):
        for x in range(118):
            for c in range(16):
                self.stopNote(x, c)

    def modulation(self, channel, value):
        return self.synth.modulation(channel, value)

    def pan(self, channel, value):
        return self.synth.pan(channel, value)

    def mainVolume(self, channel, value):
        return self.synth.main_volume(channel, value)
