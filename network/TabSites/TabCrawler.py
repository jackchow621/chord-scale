# -*- coding: utf-8 -*-

import threading
from network.TabSites import *
from network.TabSites.TabBase import *


class TabCrawler(threading.Thread):
    tabCrawlers = []
    tabBase = None
    rootFileLocate = r'C:\picstmp'

    def __init__(self, sites):
        super(TabCrawler, self).__init__()
        self.sites = sites
        self.tabBase = TabBase()
        self.tabCrawlers = []
        for site in sites:
            try:
                print(site)
                tabCrawler = self.createInstance('network.TabSites.' + site, site)
                # print(tabCrawler.tag)
                self.tabCrawlers.append(tabCrawler)
            except Exception as ex:
                print(ex)

    def run(self):
        print(self.sites)
        print('running')

    def getList(self, keyword):
        lists = []
        for tabCrawler in self.tabCrawlers:
            list = tabCrawler.searchList(keyword)
            lists.extend(list)
        return lists

    def getPics(self, name, url):
        images = []
        ns = name.split('-')
        if len(ns) != 3:
            print('img name error')
        else:
            file = self.rootFileLocate + os.sep + ns[0] + os.sep + name
            if not os.path.exists(file):
                for tabCrawler in self.tabCrawlers:
                    if tabCrawler.tag == ns[0]:
                        tabCrawler.searchPic(self.rootFileLocate, name, url)
                        break
                file = self.rootFileLocate + os.sep + ns[0] + os.sep + name
            for root, dirs, files in os.walk(file):
                for f in files:
                    images.append(os.path.join(root, f))
        return images

    def createInstance(self, module_name, class_name, *args, **kwargs):
        module_meta = __import__(module_name, globals(), locals(), [class_name])
        class_meta = getattr(module_meta, class_name)
        obj = class_meta(*args, **kwargs)
        return obj
