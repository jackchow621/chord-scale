# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from Network.TabSites.TabBase import *


class TabJtp(TabBase):
    def __init__(self):
        super().__init__()
        self.tag = '吉他谱'
        self.rootUrl = 'http://www.jitapu.com/'

    # orverride
    def searchList(self, keyword):
        # print(parse.quote(key,encoding='gb2312'))
        url = self.rootUrl + 'searchResults.aspx?KeyWord=' + parse.quote(keyword,
                                                                         encoding='gb2312') + r'&location=0'
        print(url)

        data = self._getPage(url)
        self.total = int(
            re.findall('共搜索到：.*条记录', data)[0].replace('共搜索到：', '').replace('条记录', '').replace('<strong>', '').replace(
                '</strong>', ''))

        result = []

        obj = BeautifulSoup(data, 'html.parser')
        main = obj.findAll(name='div', attrs={"id": 'searchMain'})[0]
        if main != None and not '抱歉' in str(main):
            lists = main.findAll(name='li')
            index = 1
            for li in lists:
                if 'IMG' in re.findall('.*</span>', str(li))[0]:
                    a = li.findAll(name='a', target=True)[0]
                    result.append([self.tag + '-' + keyword + str(index) + '-' + a.text, self.rootUrl + a['href']])
                    index = index + 1
        return result

    # orverride
    def searchPic(self, rootDir, name, url):
        picPage = self._getPage(url)
        obj = BeautifulSoup(picPage, 'html.parser')
        pics = obj.findAll(name='div', attrs={"id": 'imgTab'})

        for p in pics:
            img = self.rootUrl + p.findAll(name='img')[0]['src'].replace('../../', '').replace('\\', '/').replace(' ',                                                                                        '')
            self._downloadImg(self.tag, rootDir, name, img)
