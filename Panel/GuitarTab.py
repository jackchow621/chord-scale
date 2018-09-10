# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QScrollArea, QMessageBox, QLineEdit, QLabel
from Network.TabSites.TabCrawler import *
from PyQt5.QtCore import Qt, QSize
from Panel.widgets.ComboCheckBox import ComboCheckBox
from Panel.widgets.LinkLabel import LinkLabel
from Panel.widgets.PicScrool import PicScrool
from Panel.widgets.PicViewer import PicViewer
from Panel.widgets.TabList import TabList


class GuitarTab(QWidget):
    sites = {'虫虫吉他': 'TabCcjt', '吉他谱': 'TabJtp'}

    def __init__(self):
        super().__init__()
        # .availableGeometry() #获取可用桌面大小:
        # .screenGeometry()   #获取设备屏幕大小
        '''self.setGeometry(QApplication.desktop().availableGeometry())
        self.setWindowTitle('tab')
        qPalette = QPalette()
        qPalette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(qPalette)'''
        self.initUI()
        # self.show()

    def initUI(self):
        # 查询条件区域
        self.layout_condition_h = QHBoxLayout()
        keyLabel = QLabel('关键字')
        self.keyText = QLineEdit()
        query = QPushButton('查询')
        siteLabel = QLabel('吉他谱网站')
        self.sitesCombo = ComboCheckBox(list(self.sites.keys()))
        self.sitesCombo.setMinimumSize(QSize(400, 20))
        self.sitesCombo.selectAll(2)
        query.clicked.connect(self.query)
        reset = QPushButton('重置')
        reset.clicked.connect(self.reset)
        self.layout_condition_h.addWidget(keyLabel)
        self.layout_condition_h.addWidget(self.keyText)
        self.layout_condition_h.addWidget(siteLabel)
        self.layout_condition_h.addWidget(self.sitesCombo)
        self.layout_condition_h.addWidget(query)
        self.layout_condition_h.addWidget(reset)

        # 内容区域
        self.layout_content_h = QHBoxLayout()

        # 内容区域-左-列表
        self.tabArea = QWidget()
        # self.tabArea.setMinimumSize(QSize(800, 800))

        self.tabList = TabList()  # console
        # self.tabList.setMinimumSize(QSize(14000, 540))
        # self.tabList.setTitle('查询结果')

        # 滚动条
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setAutoFillBackground(True)
        self.scroll.setWidget(self.tabList)

        self.layout_content_list_v = QVBoxLayout()
        self.layout_content_list_v.addWidget(self.scroll)
        self.tabArea.setLayout(self.layout_content_list_v)

        # 内容区域-右-图像
        self.layout_content_pic_h = QHBoxLayout()
        # key1Label = QLabel('result')
        # self.layout_content_pic_h.addWidget(key1Label)

        #
        # self.layout_content_h.addStretch(15)
        self.layout_content_h.addWidget(self.tabArea)
        self.layout_content_h.setStretch(0, 1)
        # self.layout_content_h.addStretch(15)
        self.layout_content_h.addLayout(self.layout_content_pic_h)
        self.layout_content_h.setStretch(1, 2)

        self.vbox = QVBoxLayout()
        self.vbox.setStretch(0, 1)
        self.vbox.addLayout(self.layout_condition_h)
        self.vbox.setStretch(1, 30)
        self.vbox.addLayout(self.layout_content_h)

        # 图片区域
        self.picViewer = PicViewer()

        # 滚动条2
        self.picScroll = PicScrool()
        self.picScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.picScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.picScroll.setWidgetResizable(True)
        self.picScroll.setAutoFillBackground(True)
        self.picScroll.setWidget(self.picViewer)
        self.picScroll.zoomSignal.connect(self.zoomPic)

        self.layout_content_pic_h.addWidget(self.picScroll)

        self.setLayout(self.vbox)

    def query(self):
        if self.keyText.text() == '':
            QMessageBox().information(self, '错误', '请输入关键字')
        else:
            self.tabList.removeItem()
            siteK = []
            for item in self.sitesCombo.Selectlist():
                print(self.sites.get(item))
                siteK.append(self.sites.get(item))
            self.crawler = TabCrawler(siteK)
            self.crawler.start()
            ls = self.crawler.getList(self.keyText.text())
            if len(ls) > 0:
                for l in ls:
                    try:
                        a = LinkLabel("<a style='color: green;' href = '" + l[1] + "'> " + l[0] + "</a>", l[0], l[1])
                        a.currentLink.connect(self.viewImg)
                        self.tabList.addItem(a)
                    except Exception as ex:
                        print(ex)
            else:
                QMessageBox().information(self, '错误', '查询无数据')

    def reset(self):
        self.tabList.removeItem()

    def viewImg(self, currentImg, currentUrl):
        print('click........', currentImg, '...', currentUrl)
        images = self.crawler.getPics(currentImg, currentUrl)
        self.picViewer.view(images)

    def zoomPic(self, zoomIn=True):
        if len(self.picViewer.images) == 0:
            return
        self.picViewer.zoomPic(zoomIn)
