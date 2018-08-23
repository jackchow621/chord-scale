# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from chord import *
 
root = Tk()
root.title('chord-scale')
root.resizable(width=False, height=False)
#root.geometry()

s = Style()
s.configure('My.TFrame', background='white')

node = ("C","#C","D","bE","E","F","#F","G","#G","A","bB","B")
fretNum = 18
global fretLabelType
global noteStr
fretLabelType = 0#0:letter    1:Arabic numeral
pro = ("maj","min","dim","half-dim","aug","aug-maj","dom","min-maj")
interval = ("-","7","9","11","13","sus","sus2")
scale = ("Ionian(major)","Dorian","Phrygian","Lydian","Mixolydian","Aeolian(minor)",\
         "Locrian","----------------","Pentatonic-maj","Pentatonic-min","Blues-major","Blues-minor")
noteStyle = ("Letter","Arabic numeral")

p_line = PhotoImage(file='./line.gif')
p_line_dot = PhotoImage(file='./line-dot.gif')
p_line_root = PhotoImage(file='./line-root.gif')
p_line_0 = PhotoImage(file='./line-style3.gif')
p_line_dot_0 = PhotoImage(file='./line-style3-dot.gif')
p_line_root_0 = PhotoImage(file='./line-style3-root.gif')
p_line_12f = PhotoImage(file='./line-style2.gif')

p_style_up = PhotoImage(file='./line-style1-up.gif')
p_style_up_dot = PhotoImage(file='./line-style1-up-dot.gif')
p_style_up_root = PhotoImage(file='./line-style1-up-root.gif')
p_style_down = PhotoImage(file='./line-style1-down.gif')
p_style_down_dot = PhotoImage(file='./line-style1-down-dot.gif')
p_style_down_root = PhotoImage(file='./line-style1-down-root.gif')

line1=[node[4],]#1 string
line2=[node[11],]#2 string
line3=[node[7],]#3 string
line4=[node[2],]#4 string
line5=[node[9],]#5 string
line6=[node[4],]#6 string

#init fretboard
for i in range(fretNum):
    line1.append(node[(i+5)%12])#E
    line2.append(node[(i+12)%12])#B
    line3.append(node[(i+8)%12])#G
    line4.append(node[(i+3)%12])#D
    line5.append(node[(i+10)%12])#A
    line6.append(node[(i+5)%12])#E

lines=(line1,line2,line3,line4,line5,line6)

labels=[]

c=chord()

slFrame = Frame(root,width=1200, height=50)
slFrame.grid(row=0, column=0)


frerBoard = Frame(root,width=90*fretNum, height=340,style='My.TFrame')
frerBoard.grid(row=2, column=0)




Label(slFrame, text="key").grid(row=0,column=0)
Label(slFrame, text="attribute").grid(row=0,column=2)
Label(slFrame, text="advance").grid(row=0,column=4)
Label(slFrame, text="scale").grid(row=0,column=6)
Label(slFrame, text="board style").grid(row=0,column=8)

rootNoteCombo = Combobox(slFrame,width = 8,exportselection="true")
rootNoteCombo.grid(row=0,column=1)
rootNoteCombo["values"] = node
rootNoteCombo.current(0)
#rootNoteCombo.bind("<<ComboboxSelected>>",node)

proCombo = Combobox(slFrame,width = 8,exportselection="true")
proCombo.grid(row=0,column=3)
proCombo["values"] = pro
proCombo.current(0)

intervalCombo = Combobox(slFrame,width = 8,exportselection="true")
intervalCombo.grid(row=0,column=5)
intervalCombo["values"] = interval
intervalCombo.current(0)

scaleTypeCombo = Combobox(slFrame,width = 12,exportselection="true")
scaleTypeCombo.grid(row=0,column=7)
scaleTypeCombo["values"] = scale
scaleTypeCombo.current(0)

noteTypeCombo = Combobox(slFrame,width = 12,exportselection="true")
noteTypeCombo.grid(row=0,column=9)
noteTypeCombo["values"] = noteStyle
noteTypeCombo.current(0)


def scale():
    global noteStr
    noteStr=c.getScales(rootNoteCombo.get(),scaleTypeCombo.get())
    resultLabel.config(text=list(noteStr.values()))
    drawBoard(noteStr)
def chord():
    global noteStr
    noteStr=c.getChord(rootNoteCombo.get(),proCombo.get(),intervalCombo.get())
    resultLabel.config(text=list(noteStr.values()))
    drawBoard(noteStr)
def clear():
    resultLabel.config(text='To be continued...')
    drawBoard("")
    
def initNote():
    for i in range(6):
        label=[]
        for j in range(fretNum):
            labelTmp = Label(frerBoard,compound = 'center')
            labelTmp.grid(row=i,column=j)
            label.append(labelTmp)
        labels.append(label)

def drawBoard(noteStr):
    global fretLabelType
    fretLabelType = noteStyle.index(noteTypeCombo.get())
    if labels==[]:
        initNote()
    for i in range(6):
        for j in range(fretNum):
            if(noteStr == ""):#none
                drawBoardLine(0,i,j,lines[i][j])
            else:
                for c in list(noteStr):
                    #print(lines[i][j] ,'***',noteStr.get(str(c)),'**',lines[i][j] == noteStr.get(str(c)))
                    if lines[i][j] == noteStr.get(str(c)):
                        if c == '1':
                            drawBoardLine(2,i,j,c)#root note
                            break
                        else:
                            drawBoardLine(1,i,j,c)#normal note
                            break
                    else:
                        drawBoardLine(0,i,j,c)#none

def drawBoardLabel(note,noteType,noteName):
    if fretLabelType == 0:
        if noteType==0:        
            note.config(text = '',foreground='black')
        elif noteType==1:        
            note.config(text = noteStr.get(noteName),foreground='black')
        elif noteType==2:        
            note.config(text = noteStr.get(noteName),foreground='white')
        else:
            print('error noteType')
    elif fretLabelType == 1:
        if noteType==0:        
            note.config(text = '',foreground='black')
        elif noteType==1:        
            note.config(text = noteName,foreground='black')
        elif noteType==2:        
            note.config(text = '1',foreground='white')
        else:
            print('error noteType')
    else:
        print('error fretLabelType')

def drawBoardLine(noteType,i,j,noteName):
    if j == 0:#********0 fret*******
        if noteType==0:        
            labels[i][j].config(image=p_line_0)
            drawBoardLabel(labels[i][j],noteType,noteName)
        elif noteType==1:        
            labels[i][j].config(image=p_line_dot_0)
            drawBoardLabel(labels[i][j],noteType,noteName)
        elif noteType==2:        
            labels[i][j].config(image=p_line_root_0)
            drawBoardLabel(labels[i][j],noteType,noteName)
    elif j in(3,5,7,9,15,17):#*******3,5,7,9,15,17 fret********		
        if i==2:        
            if noteType==0:#none
                labels[i][j].config(image=p_style_up)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==1:#normal note        
                labels[i][j].config(image=p_style_up_dot)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==2:#root note
                labels[i][j].config(image=p_style_up_root)
                drawBoardLabel(labels[i][j],noteType,noteName)
        elif i==3:        
            if noteType==0:        
                labels[i][j].config(image=p_style_down)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==1:        
                labels[i][j].config(image=p_style_down_dot)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==2:        
                labels[i][j].config(image=p_style_down_root)
                drawBoardLabel(labels[i][j],noteType,noteName)
        else:        
            if noteType==0:        
                labels[i][j].config(image=p_line)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==1:        
                labels[i][j].config(image=p_line_dot)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==2:        
                labels[i][j].config(image=p_line_root)
                drawBoardLabel(labels[i][j],noteType,noteName)
    elif j==12:#********12 fret*******        
        if i in(1,4):        
            if noteType==0:        
                labels[i][j].config(image=p_line_12f)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==1:        
                labels[i][j].config(image=p_line_dot)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==2:        
                labels[i][j].config(image=p_line_root)
                drawBoardLabel(labels[i][j],noteType,noteName)
        else:        
            if noteType==0:        
                labels[i][j].config(image=p_line)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==1:        
                labels[i][j].config(image=p_line_dot)
                drawBoardLabel(labels[i][j],noteType,noteName)
            elif noteType==2:        
                labels[i][j].config(image=p_line_root)
                drawBoardLabel(labels[i][j],noteType,noteName)
    else:#********normal fret*******        
        if noteType==0:        
            labels[i][j].config(image=p_line)
            drawBoardLabel(labels[i][j],noteType,noteName)
        elif noteType==1:        
            labels[i][j].config(image=p_line_dot)
            drawBoardLabel(labels[i][j],noteType,noteName)
        elif noteType==2:        
            labels[i][j].config(image=p_line_root)
            drawBoardLabel(labels[i][j],noteType,noteName)
            

btn1 = Button(slFrame, text="chord", width = 8,command=chord)
btn1.grid(row=0,column=10)

btn = Button(slFrame, text="scale", width = 8,command=scale)
btn.grid(row=0,column=11)

btn2 = Button(slFrame, text="more", width = 8,command=clear)
btn2.grid(row=0,column=12)

resultLabel = Label(slFrame)
resultLabel.grid(row=0,column=13)

slFrame.grid_propagate(0)
frerBoard.grid_propagate(0)


root.mainloop()
