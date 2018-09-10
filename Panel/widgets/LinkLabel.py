# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QObject


class LinkLabel(QLabel, QObject):
    currentLink = pyqtSignal(str, str)

    def __init__(self, text, name, url):
        super(LinkLabel, self).__init__()
        self.text = text
        self.name = name
        self.url = url
        self.setText(self.text)
        self.setToolTip(self.url)

    def mousePressEvent(self, event):
        self.currentLink.emit(self.name, self.url)
