# -*- coding: utf-8 -*-

"""
企查查：www.qichacha.com
获取企业对应的目标网址
"""

__author__ = 'YangXiao'

import urllib.request
import http.cookiejar
import gzip
import re
import csv
import os
import time
from urllib.parse import urlencode
from util.loadList import load_list, load_names
from util.cookies import Cookies

URL = 'www.qichacha.com'
Headers = {
    'Host': 'www.qichacha.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate,br',
    'Connection': 'Keep-Alive',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': Cookies[0]
}


class SearchSpider(object):
    def __init__(self):
        self.opener = self.get_opener(Headers)

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
            pass
        return data

    def get_html(self, url, retries=3):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, timeout=10).read()  # 设置超时时间为10秒
            return self.ungzip(data)
        except urllib.request.URLError as e:
            if retries > 0: return self.get_html(retries - 1)
            print(url)
            return b''

    def save_to_csvfile(self, company_info):
        tempDir = os.path.abspath('../')
        file_name = os.path.join(tempDir, 'data', 'links.csv')
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(company_info)

    def load_company_link(self, company_name):
        d = {
            'key': company_name,
            'index': 0
        }
        search_url = 'http://www.qichacha.com/search?' + urlencode(d)
        html = self.get_html(search_url)
        html_doc = html.decode(encoding='utf-8', errors='ignore')
        # <a href="/firm_bbe5875f3d54a99fc738206340d545ee.shtml" target="_blank" class="text-priamry"><em><em>英特易信息科技（厦门）有限公司</em></em></a>
        pattern = re.compile(
            r'<td class="tp2">.*?href="(.*?)".*?<em>(.*?)</em>.*?</td>',
            re.DOTALL
        )
        results = pattern.findall(html_doc)
        if len(results) == 0: return None
        res = results[0]
        company_link, name = URL + res[0], res[1].replace('<em>', '')
        return company_link if name == company_name else 'not existed'

    def collection_links(self):
        size = 1655
        # company_list = load_list(size=size)
        company_list = load_names(size=size)
        company_info = []
        start = 1440
        end = len(company_list)

        for i in range(start, end):
            # company = company_list[i]
            # no, company_name = company[0], company[1]
            company_name = company_list[i]
            try:
                company_link = self.load_company_link(company_name)
            except Exception:
                print('Request Failed at:', i)
                break

            if company_link is not None and company_link != 'not existed':
                company_info.append((i + 1, company_name, company_link))
            elif company_info == 'not existed':
                print('Not existed:', i)
            else:
                print('Failed at:', i)
                break
            time.sleep(1.2)
            print('Current position at:', i)
        self.save_to_csvfile(company_info)


# '''
if __name__ == '__main__':
    spider = SearchSpider()
    spider.collection_links()
# '''
