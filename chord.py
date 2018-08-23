# -*- coding: utf-8 -*-
import collections
class chord():
    global musicNotes
    global tmp
    tmp = collections.OrderedDict()
    musicNotes = ["C","#C","D","bE","E","F","#F","G","#G","A","bB","B"]
    
    def getChord(self,root,pro,interval):
        if root in musicNotes:
            index = musicNotes.index(root)
            global tmp
            tmp = {}
            tmp['1'] = root
            if interval=="-":#triad chords
                if pro=="maj":
                    tmp['3'] = musicNotes[(index+4)%12]
                    tmp['5'] = musicNotes[(index+7)%12]
                elif pro=="min":
                    tmp['3'] = musicNotes[(index+3)%12]
                    tmp['5'] = musicNotes[(index+7)%12]
                elif pro=="aug":
                    tmp['3'] = musicNotes[(index+4)%12]
                    tmp['5'] = musicNotes[(index+8)%12]
                elif pro=="dim":
                    tmp['3'] = musicNotes[(index+3)%12]
                    tmp['5'] = musicNotes[(index+6)%12]
                else:
                    tmp['1'] = "triad type error."
            elif interval=="7":#senventh chords
                self.getChord(root,"maj","-")
                if pro=="maj":
                    tmp['7'] = musicNotes[(index+11)%12]
                elif pro=="min":
                    tmp['7'] = musicNotes[(index+10)%12]
                elif pro=="dom":
                    tmp['7'] = musicNotes[(index+10)%12]
                elif pro=="min-maj":
                    tmp['7'] = musicNotes[(index+11)%12]
                elif pro=="dim":
                    tmp['7'] = musicNotes[(index+9)%12]
                elif pro=="half-dim":
                    tmp['7'] = musicNotes[(index+10)%12]
                elif pro=="aug":
                    tmp['7'] = musicNotes[(index+10)%12]
                elif pro=="aug-maj":
                    tmp['7'] = musicNotes[(index+11)%12]
                else:
                    tmp['1'] = "triad type error."
            elif interval=="9":   
                self.getChord(root,pro,"7")
                tmp['9'] = musicNotes[(index+2)%12]
            elif interval=="11":   
                self.getChord(root,pro,"9")
                tmp['11'] = musicNotes[(index+5)%12]
            elif interval=="13":   
                self.getChord(root,pro,"11")
                tmp['13'] = musicNotes[(index+9)%12]
            elif interval=="sus":
                self.getChord(root,pro,"-")
                tmp['3']=musicNotes[(index+5)%12]#sus:replace third note with 4th note
            elif interval=="sus2":
                self.getChord(root,pro,"-")
                tmp['3']=musicNotes[(index+2)%12]#sus:replace third note with second note
            else:
                tmp['1'] = "chord unsupported yet."
        else:
            tmp['1'] = 'error root note'
        return tmp
    

    def getScales(self,root,pro):
        if root in musicNotes:
            index = musicNotes.index(root)
            global tmp
            tmp = {}
            tmp['1'] = root
            if pro.startswith("Ionian"):
                for i in range(1,7):
                    if(i in (1,2)):
                        tmp[str(i+1)] = musicNotes[(index+i*2)%12]
                    elif(i in (3,)):
                        tmp[str(i+1)] = musicNotes[(index+5)%12]
                    elif(i == 7):
                       tmp[str(i+1)] = root
                    else:
                       tmp[str(i+1)] = musicNotes[(index+i*2-1)%12]
            elif pro.startswith("Lydian"):
                tmp = self.getScales(root,"Ionian")
                tmp['3'] = musicNotes[(index+4)%12]
                tmp['4'] = musicNotes[(index+6)%12]
            elif pro.startswith("Mixolydian"):
                tmp = self.getScales(root,"Ionian")
                tmp['6'] = musicNotes[(index+9)%12]
                tmp['7'] = musicNotes[(index+10)%12]
            elif pro.startswith("Aeolian"):
                for i in range(1,7):
                    if(i==1):
                        tmp['2'] = musicNotes[(index+2)%12]
                    elif(i==2):
                        tmp['3'] = musicNotes[(index+3)%12]
                    elif(i in(3,4)):
                        tmp[str(i+1)] = musicNotes[(index+i*2-1)%12]
                    elif(i==5):
                        tmp[str(i+1)] = musicNotes[(index+8)%12]
                    elif(i==7):
                        tmp[str(i+1)] = root
                    else:
                        tmp[str(i+1)] = musicNotes[(index+i*2-2)%12]
            elif pro.startswith("Dorian"):
                tmp = self.getScales(root,"Aeolian")
                tmp['6'] = musicNotes[(index+9)%12]
                tmp['7'] = musicNotes[(index+10)%12]
            elif pro.startswith("Phrygian"):
                tmp = self.getScales(root,"Aeolian")
                tmp['2'] = musicNotes[(index+1)%12]
                tmp['3'] = musicNotes[(index+3)%12]
            elif pro.startswith("Locrian"):
                tmp = self.getScales(root,"Phrygian")
                tmp['4'] = musicNotes[(index+5)%12]
                tmp['5'] = musicNotes[(index+6)%12]
            elif pro.startswith("Pentatonic-maj"):
                for i in range(1,5):
                    if(i in (1,2)):
                        tmp[str(i+1)] = musicNotes[(index+i*2)%12]
                    else:
                        tmp[str(i+1)] = musicNotes[(index+i*2+1)%12]
            elif pro.startswith("Pentatonic-min"):
                for i in range(1,5):
                    if(i == 1):
                        tmp[str(i+1)] = musicNotes[(index+3)%12]
                    elif(i in (2,3)):
                        tmp[str(i+1)] = musicNotes[(index+i*2+1)%12]
                    else:
                        tmp[str(i+1)] = musicNotes[(index+10)%12]
            elif pro.startswith("Blues-maj"):
                tmp = self.getScales(root,"Pentatonic-maj")
                tmp['b3'] = musicNotes[(index+3)%12]#add a b3 on pen-maj
            elif pro.startswith("Blues-min"):
                tmp = self.getScales(root,"Pentatonic-min")
                tmp['#4'] = musicNotes[(index+6)%12]#add a #4 on pen-min
            elif pro.startswith("----"):
                tmp['1'] = "please select a scale type."
            else:
                tmp['1'] = "scale unsupported yet."
        else:
            tmp['1'] = 'error root note'
        return tmp


    '''def replaceNote(self,noteStr):
        notes = noteStr.split(",")
        if len(notes[0].split("/"))>1:
            notes[0] = notes[0].split("/")[1]
        print("**************",notes)
        for note in notes:
            if "/" in note:
                index = notes.index(note)
                splits = note.split("/")
                if splits[0].replace("#","") in notes:
                    notes[index] = splits[1]
                else:
                    notes[index] = splits[0]
        return ",".join(notes)'''
                
        
'''c=chord()  
print(c.getScales("C","Ionian").values())
print(c.getScales("F","Lydian").values())
print(c.getScales("G","Mixolydian").values())
print(c.getScales("A","Aeolian").values())
print(c.getScales("D","Dorian").values())
print(c.getScales("E","Phrygian").values())
print(c.getScales("B","Locrian").values())
'''
