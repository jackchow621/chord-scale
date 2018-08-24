# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import Style, Combobox, Frame

node = ["C", "#C", "D", "bE", "E", "F", "#F", "G", "#G", "A", "bB", "B"]
fretNum = 18
# 0:letter    1:Arabic numeral
fretLabelType = 0
pro = ["maj", "min", "dim", "half-dim", "aug", "aug-maj", "dom", "min-maj"]
interval = ["-", "7", "9", "11", "13", "sus", "sus2"]
scale = ["Ionian(major)", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian(minor)", "Locrian", "----------------", "Pentatonic-maj", "Pentatonic-min", "Blues-major", "Blues-minor"]
noteStyle = ["Letter", "Arabic numeral"]


# 面板类
class Panel:
    def __init__(self):
        root = Tk()
        root.title('chord-scale')
        root.resizable(width=False, height=False)

        s = Style()
        s.configure('My.TFrame', background='white')

        slFrame = self.create_frame(root)
        self.create_board(root)
        self.create_label(slFrame)
        self.create_rootnote_combo(slFrame)
        self.create_pro_combo(slFrame)
        self.create_interval_combo(slFrame)
        self.create_scaletype_combo(slFrame)
        self.create_notetype_combo(slFrame)
        self.create_bottom(slFrame)
        root.mainloop()

    # 创建框架
    def create_frame(self, root):
        slFrame = Frame(root, width=1200, height=50)
        slFrame.grid(row=0, column=0)
        slFrame.grid_propagate(0)
        return slFrame

    # 创建面板
    def create_board(self, root):
        frerBoard = Frame(root, width=90 * fretNum, height=340, style='My.TFrame')
        frerBoard.grid(row=2, column=0)
        frerBoard.grid_propagate(0)

    # 创建标签
    def create_label(self, frame):
        labels = []
        labels.append(Label(frame, text="key").grid(row=0, column=0))
        labels.append(Label(frame, text="attribute").grid(row=0, column=2))
        labels.append(Label(frame, text="advance").grid(row=0, column=4))
        labels.append(Label(frame, text="scale").grid(row=0, column=6))
        labels.append(Label(frame, text="board style").grid(row=0, column=8))

    # 初始化下拉框
    def create_rootnote_combo(self, frame):
        rootNoteCombo = Combobox(frame, width=8, exportselection="true")
        rootNoteCombo.grid(row=0, column=1)
        rootNoteCombo["values"] = node
        rootNoteCombo.current(0)

    # 初始化下拉框
    def create_pro_combo(self, frame):
        proCombo = Combobox(frame, width=8, exportselection="true")
        proCombo.grid(row=0, column=3)
        proCombo["values"] = pro
        proCombo.current(0)

    # 初始化下拉框
    def create_interval_combo(self, frame):
        intervalCombo = Combobox(frame, width=8, exportselection="true")
        intervalCombo.grid(row=0, column=5)
        intervalCombo["values"] = interval
        intervalCombo.current(0)

    # 初始化下拉框
    def create_scaletype_combo(self, frame):
        scaleTypeCombo = Combobox(frame, width=12, exportselection="true")
        scaleTypeCombo.grid(row=0, column=7)
        scaleTypeCombo["values"] = scale
        scaleTypeCombo.current(0)

    # 初始化下拉框
    def create_notetype_combo(self, frame):
        noteTypeCombo = Combobox(frame, width=12, exportselection="true")
        noteTypeCombo.grid(row=0, column=9)
        noteTypeCombo["values"] = noteStyle
        noteTypeCombo.current(0)

    # 初始化按钮
    def create_bottom(self, frame):
        btn1 = Button(frame, text="chord", width=8)
        btn1.grid(row=0, column=10)

        btn = Button(frame, text="scale", width=8)
        btn.grid(row=0, column=11)

        btn2 = Button(frame, text="more", width=8)
        btn2.grid(row=0, column=12)

    def create_result_label(self, frame):
        resultLabel = Label(frame)
        resultLabel.grid(row=0,column=13)



if __name__ == '__main__':
    Panel()
