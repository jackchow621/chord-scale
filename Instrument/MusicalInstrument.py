# -*- coding: utf-8 -*-
from sounds.sound import *

class MusicalInstrument(object):
    notesAll = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    roots = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
    pros = ("maj", "min", "dim", "half-dim", "aug", "aug-maj", "dom", "min-maj")
    intervals = ("-", "7", "9", "11", "13", "sus", "sus2")
    scales = ("Ionian(major)", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian(minor)", \
              "Locrian", "----------------", "Pentatonic-maj", "Pentatonic-min", "Blues-major", "Blues-minor")
    noteStyles = ("Letter", "Arabic numeral")

    notes = []

    #program 000 to 127 on bank 0
    __ins = ('GrandPiano',
             'BrightPiano',
             'RockPiano',
             'Honky-TonkPiano',
             'ElectricPiano',
             'CrystalPiano',
             'Harpsichord',
             'Clavinet',
             'Celesta',
             'Glockenspiel',
             'MusicBox',
             'Vibraphone',
             'Marimba',
             'Xylophone',
             'TubularBells',
             'Dulcimer(Santur)',
             'DrawBarOrgan',
             'PercussiveOrgan',
             'RockOrgan',
             'ChurchOrgan',
             'ReedOrgan',
             'Accordion',
             'Harmonica',
             'Bandoneon',
             'NylonGuitar',
             'SteelStringGuitar',
             'JazzGuitar',
             'CleanGuitar',
             'MutedGuitar',
             'OverdriveGuitar',
             'DistortionGuitar',
             'GuitarHarmonics',
             'AcousticBass',
             'FingeredBass',
             'PickedBass',
             'FretlessBass',
             'SlapBass1',
             'SlapBass2',
             'SynthBass1',
             'SynthBass2',
             'Violin',
             'Viola',
             'Cello',
             'ContraBass',
             'TremoloStrings',
             'PizzicatoStrings',
             'OrchestralHarp',
             'Timpani',
             'StringsEnsemble1',
             'StringsEnsemble2',
             'SynthStrings1',
             'SynthStrings2',
             'ChoirAahs',
             'VoiceOohs',
             'SynthVoice',
             'OrchestraHit',
             'Trumpet',
             'Trombone',
             'Tuba',
             'MutedTrumpet',
             'FrenchHorns',
             'BrassSection',
             'SynthBrass1',
             'SynthBrass2',
             'SopranoSax',
             'AltoSax',
             'TenorSax',
             'BaritoneSax',
             'Oboe',
             'EnglishHorns',
             'Bassoon',
             'Clarinet',
             'Piccolo',
             'Flute',
             'Recorder',
             'PanFlute',
             'BlownBottle',
             'Shakuhachi',
             'Whistle',
             'Ocarina',
             'SquareWave',
             'SawWave',
             'SynthCalliope',
             'ChifferLead',
             'Charang',
             'SoloVoice',
             '5thSawWave',
             'Bass&Lead',
             'Fantasia(NewAge)',
             'WarmPad',
             'PolySynth',
             'SpaceVoice',
             'BowedGlass',
             'MetalPad',
             'HaloPad',
             'SweepPad',
             'IceRain',
             'SoundTrack',
             'Crystal',
             'Atmosphere',
             'Brightness',
             'Goblin',
             'EchoDrops',
             'StarTheme',
             'Sitar',
             'Banjo',
             'Shamisen',
             'Koto',
             'Kalimba',
             'BagPipe',
             'Fiddle',
             'Shannai',
             'TinkleBell',
             'Agogo',
             'SteelDrums',
             'WoodBlock',
             'TaikoDrum',
             'MelodicTom',
             'SynthDrum',
             'ReverseCymbal',
             'GuitarFretNoise',
             'BreathNoise',
             'SeaShore',
             'BirdTweets',
             'Telephone',
             'Helicopter',
             'Applause',
             'GunShot')
    programs = []
    for ins in __ins:
        programs.append(ins)

    # bank 128
    drumDict = {'StandardDrumKit': '0',
                'RoomDrumKit': '8',
                'PowerDrumKit': '16',
                'ElectronicDrumKit': '24',
                'TR-808/909DrumKit': '25',
                'JazzDrumKit': '32',
                'BrushDrumKit': '40',
                'OrchestralDrumKit': '48',
                'FixRoomDrumKit': '49',
                '7 MT-32DrumKit': '127'
                }
    drums = []
    for ins in __ins:
        drums.append(ins)

    def __init__(self):
        self.sd = sound('ARACHNO')

    def initFretBoard(self,num):
        # reload
        pass

    def playNote(self,note):
        self.sd.playNote(note)

    def playScale(self,scale):
        for note in scale:
            self.sd.playNote(note)

    def playChord(self,chord):
        self.sd.playNoteContainer(chord)

    def changeProgram(self,program):
        self.sd.setInstrument(program)

    def stop(self):
        self.sd.stopEverything()