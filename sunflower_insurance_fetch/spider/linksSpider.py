# -*- coding: utf-8 -*-

"""
采集每个省对应市的网页入口链接：
例如：
    江苏省 -> 南京市 -> http://a.xiangrikui.com/sf16-cs169/gs.html
    江苏省 -> 苏州市 -> http://a.xiangrikui.com/sf16-cs173/gs.html

最终将采集获得的信息保存到 data 文件夹下的 links.csv 文件中
"""

__author__ = 'YangXiao'

import urllib.request
import http.cookiejar
import gzip
import json
import xlwt
import csv

province_url = 'http://common.xiangrikui.com/api/v1/locate/provinces/'
Headers = {
    'Host': "www.xiangrikui.com",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive"
}


class LinksSpider(object):
    def __init__(self):
        self.opener = None
        self.links_info = []

    def get_opener(self, headers):
        cj = http.cookiejar.CookieJar()
        processor = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(processor)
        header_lst = []
        for key, value in headers.items():
            elem = (key, value)
            header_lst.append(elem)
        opener.addheaders = header_lst
        return opener

    def ungzip(self, data):
        try:
            data = gzip.decompress(data)
        except:
            # print('Uncompressed, no decompression.')
            pass
        return data

    def get_html(self, url, retries=3):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, timeout=10).read()  # 设置超时时间为10秒
            return self.ungzip(data)
        except urllib.request.URLError as e:
            if retries > 0: return self.get_html(retries - 1)
            print(e.reason)

    def parse_province(self, html):
        province_info = json.loads(html)
        # print(province_info)
        return province_info

    def load_all_province(self, url):
        """
        加载所有的省份信息
        :param url:
        :return:
        """
        html = self.get_html(url)
        # print(html)
        return self.parse_province(html.decode(encoding='utf-8', errors='ignore'))

    def load_all_links(self, province_info):
        """
        根据省份信息加载相应城市的网页链接
        :param province_info:
        :return:
        """
        # 示例：http://common.xiangrikui.com/api/v1/locate/provinces/17/cities
        """
       [
            {'province_name': '北京', 'id': 34},
            {'province_name': '天津', 'id': 35},
            ...
        ]
       """
        for elem in province_info:
            province_name, province_id = elem['province_name'], elem['id']
            # print(province_name, province_id)
            url = 'http://common.xiangrikui.com/api/v1/locate/provinces/' + str(province_id) + '/cities'
            html = self.get_html(url)
            city_info = json.loads(html.decode(encoding='utf-8', errors='ignore'))
            # print(city_info)
            for elem2 in city_info:
                city_name, city_id = elem2['city_name'], elem2['id']
                link = {
                    'province_name': province_name,
                    'city_name': city_name,
                    'url': 'http://a.xiangrikui.com/sf' + str(province_id) + '-cs' + str(city_id) + '/gs.html'
                }
                self.links_info.append(link)

    def save_to_xlsfile(self):
        titles = ['province_name', 'city_name', 'url']  # 标题信息
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("省_城市_链接信息")
        style = xlwt.easyxf('font: bold 1')
        for i in range(len(titles)):
            sheet.col(i).width = 256 * 20
        # 写入标题
        for i in range(len(titles)):
            sheet.write(0, i, titles[i], style)
        # 写入链接信息
        for i in range(len(self.links_info)):
            for j in range(len(titles)):
                title = titles[j]
                data = str(self.links_info[i][title]).replace('&nbsp;', '')
                sheet.write(i + 1, j, data)

        workbook.save('../data/links.xls')

    def save_to_csvfile(self):
        titles = ['省', '城市', '链接']  # 标题信息
        with open('data/links.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(titles)
            data = []
            for elem in self.links_info:
                data.append((elem['province_name'], elem['city_name'], elem['url']))
            writer.writerows(data)

    def collection_links(self):
        """
        采集链接信息
        :return:
        """
        self.opener = self.get_opener(Headers)
        province_info = self.load_all_province(province_url)
        self.load_all_links(province_info)

        # self.save_to_xlsfile()
        self.save_to_csvfile()


'''
if __name__ == '__main__':
    spider = LinksSpider()
    spider.collection_links()
'''
