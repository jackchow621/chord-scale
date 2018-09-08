# -*- coding: utf-8 -*-
from urllib import parse, request
import urllib
import os
from Network.TabSites import *
from Network.TabSites.TabCrawler import *


class TabBase():
    ilegalStr = ('\\', '/', ':', '*', '?', '"', '<', '>', '|', '-')

    def __init__(self):
        super().__init__()
        self.tag = None
        self.rootUrl = None

    # 需重写
    def searchList(self, keyword):
        pass

    # 需重写
    def searchPic(self, rootDir, name, url):
        pass

    def _replaceIlegalStr(self, text):
        for t in text:
            if t in self.ilegalStr:
                text = text.replace(t, '_')
        text = text.replace(' ', '')
        return text

    def _getPage(self, url):
        try:
            webPage = urllib.request.urlopen(url)
            page = webPage.read()
            page = page.decode('gbk')
        except Exception as ex:
            print('Error geting page...', ex)
        return page

    def _downloadImg(self, siteName, root, tabName, fileName):
        file = root + os.sep + siteName + os.sep + tabName
        self._createDir(file)
        file = file + os.sep + self._replaceIlegalStr(fileName)
        self._createImg(file, fileName)

    def _createDir(self, filePath):
        filePath = filePath.replace('\\', os.sep).replace('/', os.sep)
        fs = filePath.split(os.sep)
        file = fs[0]
        for i in range(1, len(fs)):
            file = file + os.sep + fs[i]
            if not os.path.exists(file):
                os.mkdir(file)

    def _createImg(self, file, url):
        if not os.path.exists(file):
            file = open(file, 'wb')
            file.write((urllib.request.urlopen(url)).read())
            file.close()
            print('【', url, '】downloaded.')
