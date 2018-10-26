# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from network.TabSites.TabBase import *


class TabCcjt(TabBase):
    def __init__(self):
        super().__init__()
        self.tag = '虫虫吉他'
        self.rootUrl = 'http://www.ccguitar.cn/'

    # orverride
    def searchList(self, keyword):
        # print(parse.quote(key,encoding='gb2312'))
        url = self.rootUrl.replace('www', 'so') + '/tosearch.aspx?searchname=' + parse.quote(keyword,
                                                                                             encoding='gb2312') + r'&searchtype=1'
        print(url)

        data = self._getPage(url)
        total = int(re.findall('共.*页', data)[0].replace('共', '').replace('页', ''))

        result = []
        index = 1
        if total > 0:
            for page in range(1, total):
                data = self._getPage(url + '&currentPage=' + str(page))
                lists = re.findall('<div class="list_searh">.*', data)
                for li in lists:
                    liUrl = re.findall('http.*.htm', li)[0]

                    liName = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}.*a>', li)[0]
                    liName = liName.replace(r'<span class="searchkey_css">', '').replace(r'</a>', '').replace(
                        r'</span>', '')
                    liName = self._replaceIlegalStr(liName)
                    result.append([self.tag + '-' + keyword + str(index) + '-' + liName, liUrl])
                    index = index + 1
        return result

    # orverride
    def searchPic(self, rootDir, name, url):
        picPage = self._getPage(url)
        obj = BeautifulSoup(picPage, 'html.parser')
        pics = obj.findAll(name='div', attrs={"class": 'swiper-slide'})

        for p in pics:
            img = self.rootUrl + p.findAll(name='img')[0]['src']
            self._downloadImg(self.tag, rootDir, name, img)
