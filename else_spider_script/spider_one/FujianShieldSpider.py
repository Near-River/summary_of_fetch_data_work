# -*- coding: utf-8 -*-

"""
采集福建红盾网上的企业注册信息：
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
from urllib.request import ProxyHandler

URL = 'http://wsgs.fjaic.gov.cn/webquery/basicQuery.do?method=query&loginId='
Headers = {
    'Host': 'wsgs.fjaic.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Connection': 'Keep-Alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://wsgs.fjaic.gov.cn/webquery/basicQuery.do?method=query&loginId='
}


class CompanyInfoSpider(object):
    def __init__(self):
        self.opener = None
        self.companies_info = None

    def get_opener(self, headers):
        # cj = http.cookiejar.CookieJar()
        # processor = urllib.request.HTTPCookieProcessor(cj)
        # opener = urllib.request.build_opener(processor)

        proxy = {'http': '121.56.224.52:8888'}
        proxy_support = ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

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

    def get_html(self, url, postData=None, retries=3):  # 失败后的重连机制
        try:
            response = self.opener.open(fullurl=url, data=postData, timeout=3)  # 设置超时时间为3秒
            data = response.read()
            return self.ungzip(data)
        except urllib.request.HTTPError as e:
            if retries > 0: return self.get_html(retries - 1, postData)
            print(url)
            return b'url failed'

    def savetities_to_csvfile(self, titles, filename):
        tempDir = os.path.abspath('../')
        file_name = os.path.join(tempDir, 'data', filename)
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(titles)

    def save_to_csvfile(self, info, filename):
        tempDir = os.path.abspath('../')
        file_name = os.path.join(tempDir, 'data', filename)
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(info)

    def parse_company_info(self, url):
        company_info = []
        html = self.get_html(url)
        html_info = html.decode(encoding='utf-8', errors='ignore')
        if html_info == 'url failed': return 'http_error'
        pattern1 = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
        result = pattern1.findall(html_info)
        if len(result) == 6:
            _pattern = re.compile(
                r'<td.*?>(.*?)</td>',
                re.DOTALL
            )
            _result = _pattern.findall(html_info)
            # 企业名称、注册号、住所、法定代表人、注册资本、经济性质、经营方式、营业期限、登记机关、经营范围
            info = []
            for elem in _result:
                elem = elem.replace('&nbsp;', ' ').replace('\r\n', '').replace(' ', '').replace('	', '').strip()
                info.append(elem)
            info.insert(5, '')
            info.insert(8, '')
            # print(info)
            company_info.append(info)
        elif len(result) == 7:
            _pattern = re.compile(
                r'<td.*?>(.*?)</td>',
                re.DOTALL
            )
            _result = _pattern.findall(html_info)
            # 企业名称、注册号、住所、法定代表人姓名、注册资本、企业状态、公司类型、成立日期、营业期限、登记机关、经营范围
            info = []
            for elem in _result:
                elem = elem.replace('&nbsp;', ' ').replace('\r\n', '').replace(' ', '').replace('	', '').strip()
                info.append(elem)
            info.insert(7, '')
            # print(info)
            company_info.append(info)
        return company_info

    def load_company_info(self, url, postData):
        html = self.get_html(url, postData)
        html_doc = html.decode(encoding='utf-8', errors='ignore')
        # 网络故障：目标网页未获取
        if html_doc == 'url failed': return 'http_error'
        # 匹配 没有目标企业
        # <tr><td>没有找到符合条件的数据！</td></tr>
        pattern1 = re.compile(
            r'<tr>(.*?)</tr>',
            re.DOTALL
        )
        if len(pattern1.findall(html_doc)) == 1: return 'no_result'
        # <td align="center"><a href="javascript:doView('3502XM119980610000013');">[详细信息]</a></td>
        pattern2 = re.compile(
            r'<td.*?>.*?<a href="javascript:doView\((.*?)\);">.*?</td>',
            re.DOTALL
        )
        result = pattern2.findall(html_doc)
        if len(result) == 0: return []
        etpsId = result[0][1:-1]
        # print(etpsId)
        # url = 'http://wsgs.fjaic.gov.cn/webquery/basicQuery.do?method=view&etpsId=3502XM119950116000001'
        info_url = 'http://wsgs.fjaic.gov.cn/webquery/basicQuery.do?method=view&etpsId=' + str(etpsId)
        return self.parse_company_info(info_url)

    def collection_companies_info(self):
        """ 采集福建红盾网上的企业注册信息 """
        self.opener = self.get_opener(Headers)
        search_url = 'http://wsgs.fjaic.gov.cn/webquery/basicQuery.do?method=list&loginId='
        start = 0
        count = 1
        end = 100
        # 企业名称、注册号、住所、法定代表人、注册资本、经济性质、经营方式、营业期限、登记机关、经营范围
        # 企业名称、注册号、住所、法定代表人姓名、注册资本、企业状态、公司类型、成立日期、营业期限、登记机关、经营范围
        titles = ['企业名称', '注册号', '住所', '法定代表人', '注册资本', '企业状态', '公司类型(经济性质)', '经营方式', '成立日期', '营业期限', '登记机关',
                  '经营范围']  # 标题信息
        company_info = []
        if start == 0: self.savetities_to_csvfile(titles=titles, filename='company.csv')
        for i in range(start, end):
            regNo = '3502041001655'
            regNo = '350200100004137'
            # http://wsgs.fjaic.gov.cn/webquery/basicQuery.do?method=list&loginId=
            # 表单数据：regNo     etpsName     leader
            postDict = {
                'regNo': regNo,
                'etpsName': '',
                'leader': ''
            }
            postData = urlencode(postDict).encode()  # 给Post数据编码
            result = self.load_company_info(search_url, postData)
            if result == 'http_error':
                print('http_error: %s' % regNo)
            elif result == 'no_result':
                print('no_result: %s' % regNo)
            elif result:
                company_info.extend(result)
            # if count % 3 == 0:
            #     time.sleep(2)
            #     print('Current position at:', i)

            print(count)
            count += 1
            time.sleep(1)

        self.save_to_csvfile(info=company_info, filename='company.csv')


if __name__ == '__main__':
    spider = CompanyInfoSpider()
    spider.collection_companies_info()
