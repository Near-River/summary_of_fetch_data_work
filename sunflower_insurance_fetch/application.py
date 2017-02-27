# -*- coding: utf-8 -*-

"""
向日葵网：http://a.xiangrikui.com/
保险代理人信息采集
"""

__author__ = 'YangXiao'

from spider.linksSpider import LinksSpider
from spider.infoSpider import InfoSpider


class Application(object):
    def init_links(self):
        links_spider = LinksSpider()
        links_spider.collection_links()

    def run(self):
        info_spider = InfoSpider()
        info_spider.collection_info()


if __name__ == '__main__':
    app = Application()
    # app.init_links()  # 初始化链接数据
    app.run()
