# -*- coding: utf-8 -*-
import six
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QListWidget, QDialog, QGridLayout, QPushButton, QSpinBox, \
    QDialogButtonBox, QSpacerItem, QSizePolicy, QVBoxLayout, QTableWidget, QMessageBox
from mingus.containers import Bar

from instrument import MusicalInstrument, chordLoops


class BarSelector(QDialog):
    testPlaySignal = pyqtSignal(object)

    def __init__(self, values):
        super(BarSelector, self).__init__()
        self.initUI()
        if len(values) > 0:
            self.setDefaultValue(values)
            self.instrument = values.get('instrument')

    def initUI(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("QDialog{background-color: grey;border-top-left-radius:15px;border-top-right-radius:5px;}");
        grid = QGridLayout()
        grid.addWidget(QLabel(u'root', parent=self), 0, 0)

        self.rootList = CustomList('root', MusicalInstrument.notesAll, self)
        self.octaveSpin = QSpinBox()
        self.octaveSpin.setRange(1, 6)
        self.octaveSpin.setValue(4)
        self.octaveSpin.valueChanged[int].connect(self.clickEvent)
        self.proList = CustomList('pro', MusicalInstrument.pros, self)
        self.intervalList = CustomList('interval', MusicalInstrument.intervals, self)
        self.styleList = CustomList('style', chordLoops.getStyles(), self)
        self.presetList = CustomList('preset', chordLoops.getPresets(), self)

        grid.addWidget(self.rootList, 0, 0)
        grid.addWidget(self.octaveSpin, 1, 0)
        grid.addWidget(self.proList, 0, 1)
        grid.addWidget(self.intervalList, 0, 2)
        grid.addWidget(self.styleList, 2, 0)
        grid.addWidget(self.presetList, 2, 1)

        # 创建ButtonBox，用户确定和取消
        buttonBox = QDialogButtonBox(parent=self)
        buttonBox.setOrientation(Qt.Horizontal)  # 设置为水平方向
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)  # 确定和取消两个按钮
        # 连接信号和槽
        buttonBox.accepted.connect(self.accept)  # 确定
        buttonBox.rejected.connect(self.reject)  # 取消

        # 垂直布局，布局表格及按钮
        layout = QVBoxLayout()

        # 加入前面创建的表格布局
        layout.addLayout(grid)

        # 放一个间隔对象美化布局
        # spacerItem = QSpacerItem(20, 48, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # layout.addItem(spacerItem)

        # ButtonBox
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def setDefaultValue(self, values):
        try:
            labels = values.get('label')
            if not labels:
                self.rootList.setCurrentRow(0)
                self.octaveSpin.setValue(4)
                self.proList.setCurrentRow(0)
                self.intervalList.setCurrentRow(0)
                self.styleList.setCurrentRow(0)
                self.presetList.setCurrentRow(0)
            elif len(labels) == 6:
                self.rootList.select(labels[0])
                self.octaveSpin.setValue(int(labels[1]))
                self.proList.select(labels[2])
                self.intervalList.select(labels[3])
                self.styleList.select(labels[4])
                self.presetList.select(labels[5])
        except Exception as ex:
            print('label is empty')

    def getResult(self):
        result = {}
        result['instrument'] = self.instrument
        if self.allItemSelected():
            # a group of params to caculate a Bar and return label of the bar
            result['label'] = self._getListViewText()
            result['bar'] = self.getBar(self._getListViewText())
        return result

    def _getListViewText(self):
        return [self.rootList.getCurrentItemText(),
                self.octaveSpin.value(),
                self.proList.getCurrentItemText(),
                self.intervalList.getCurrentItemText(),
                self.styleList.getCurrentItemText(),
                self.presetList.getCurrentItemText()]

    def getBar(self, args):
        return chordLoops.getLoop(args[0], args[1], args[2], args[3], args[4], args[5].split('-')[1])

    def clickEvent(self, object):
        if not isinstance(object, six.integer_types) and object.name == 'style':
            self.presetList.clear()
            self.presetList.addItems(chordLoops.getPresets(object.getCurrentItemText()))
            self.presetList.setCurrentRow(0)
        elif self.allItemSelected():
            pass
            #self.testPlaySignal.emit(self.getBar(self._getListViewText()))

    def allItemSelected(self):
        return self.rootList.currentItem() != None and self.proList.currentItem() != None and \
               self.intervalList.currentItem() != None and self.styleList.currentItem() != None and self.presetList.currentItem() != None


class CustomList(QListWidget):
    clickedSignal = pyqtSignal(object)

    def __init__(self, name, items, parent):
        super().__init__()
        self.clickedSignal.connect(parent.clickEvent)
        self.initUI()
        self.name = name
        self.addItems(items)

    def initUI(self):
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setFont(QFont("Roman times", 11, QFont.Normal))

    def select(self, text):
        if self.count() > 0:
            for i in range(self.count()):
                if self.item(i).text() == text:
                    self.setCurrentRow(i)
                    break

    def getCurrentItemText(self):
        if self.currentItem() != None:
            return self.currentItem().text()

    def mousePressEvent(self, *args, **kwargs):
        super().mousePressEvent(*args, **kwargs)
        if self.currentItem() != None:
            self.clickedSignal.emit(self)
