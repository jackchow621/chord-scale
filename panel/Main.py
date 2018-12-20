# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPalette, QColor,QIcon
import sys
from panel.GuitarTab import GuitarTab
from panel.InstrumentTab import InstrumentTab
from panel.StationTab import StationTab


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(QApplication.desktop().availableGeometry())
        self.setFixedSize(self.width(), self.height())  # 禁止改变窗口大小

        self.setWindowTitle('chord-scale')
        self.setWindowIcon(QIcon(r'images/music.ico'))
        qPalette = QPalette()
        qPalette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(qPalette)
        self.initUI()
        self.show()

    def initUI(self):
        gt = GuitarTab()
        it = InstrumentTab()
        st = StationTab()
        tabBox = QTabWidget()
        tabBox.addTab(st, '创作器')
        tabBox.addTab(it, '乐器指板')
        tabBox.addTab(gt, '在线吉他谱')
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(tabBox)
        self.setLayout(self.vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Main()
    sys.exit(app.exec_())
