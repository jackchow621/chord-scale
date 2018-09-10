# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QHBoxLayout, QComboBox, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import sys
from Panel.GuitarPanel import GuitarPanel, Fret
from Panel.PianoPanel import PianoPanel
from Panel.GuitarTab import GuitarTab


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(QApplication.desktop().availableGeometry())
        print(QApplication.desktop().availableGeometry())
        self.setFixedSize(self.width(), self.height())  # 禁止改变窗口大小
        self.setWindowTitle('chord-scale')
        qPalette = QPalette()
        qPalette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(qPalette)
        self.initUI()
        self.show()

    def initUI(self):
        gt = GuitarTab()
        gp = GuitarPanel()
        pp = PianoPanel()
        tabBox = QTabWidget()
        tabBox.addTab(gt, '在线吉他谱')
        tabBox.addTab(gp, '吉他指板')
        tabBox.addTab(pp, '钢琴指板')

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(tabBox)

        self.setLayout(self.vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Main()
    sys.exit(app.exec_())
