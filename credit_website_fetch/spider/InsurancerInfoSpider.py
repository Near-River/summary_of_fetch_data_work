# -*- coding: utf-8 -*-

"""
保险中介人信息采集（重庆市）：
"""

__author__ = 'Nate_River'

import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import csv
import xlrd
import time
import re
import threading

Headers = {
    'Host': 'iir.circ.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Referer': 'http://iir.circ.gov.cn/web/',
    'Cookie': 'CNZZDATA1619462=cnzz_eid%3D464445928-1480036183-%26ntime%3D1481860064; _gscu_1407742603=81859318id5klw10; _gscbrs_1407742603=1; Hm_lvt_6a2f36cc16bd9d0b01b10c2961b8900c=1481859319; Hm_lpvt_6a2f36cc16bd9d0b01b10c2961b8900c=1481859319; JSESSIONID=0000lvRC2W3e938Qtk8GfQwpJx0:14jjlde74; bjh-20480-%3FVRF-CX%3FGroup_ZJY_YW=BOABGEAKHJCD',
    'Connection': 'Keep-Alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': '0'
}

lock = threading.Lock()


def load_name_list():
    data = xlrd.open_workbook('name_list.xls')
    table = data.sheet_by_index(0)
    rows = table.nrows
    name_lst = []
    for r in range(rows):
        val = str(table.cell(r, 0).value).strip()
        name_lst.append(val)
    return name_lst


class InfoSpider(object):
    def __init__(self):
        self.name_lst = load_name_list()
        self.opener = self.get_opener(Headers)

    def get_opener(self, headers):
        cj = http.cookiejar.CookieJar()
        processor = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(processor)
        header_lst = []
        for key, value in headers.items(): header_lst.append((key, value))
        opener.addheaders = header_lst
        return opener

    def get_html(self, url, data, retries=3):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, data=data, timeout=10).read()  # 设置超时时间为10秒
            return data
        except (urllib.request.URLError, urllib.request.HTTPError) as e:
            if retries > 0: return self.get_html(retries - 1, data)
            return b''

    def save_to_csvfile(self, data):
        with open('info.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data)

    def collection_info(self, start, end):
        postData = {
            'id_card': '',
            'certificate_code': '',
            'evelop_code': '',
            'name': '',
            'valCode': ''
        }
        search_url = 'http://iir.circ.gov.cn/web/baoxyx!searchInfoBaoxyx.html'
        i = start
        titles = ['姓名', '性别', '资格证书号码', '资格证书状态', '执业证编号', '执业证状态', '有效截止日期'
            , '业务范围', '执业区域', '所属公司']  # 标题信息
        if start == 0: self.save_to_csvfile(data=[titles])
        while i < end:
            postData['name'] = (self.name_lst[i]).encode('gbk')
            try:
                html = self.get_html(url=search_url, data=urlencode(postData).encode(encoding='gbk'))
                html_doc = html.decode(encoding='gbk', errors='ignore')
                soup = BeautifulSoup(html_doc, 'html.parser')
                _table = (soup.findAll('table'))[-2]
                temp_str = (_table.findAll('td'))[-2].get_text()
                all_count = (temp_str.strip().split('：'))[1]
                all_count = int(all_count)
                pages = all_count // 12 if all_count % 12 == 0 else all_count // 12 + 1
                currPage = 1
                insurancer_info = []
                while currPage <= pages:
                    try:
                        postData['currentPage'] = str(currPage)
                        postData['totalCount'] = str(all_count)
                        html = self.get_html(url=search_url, data=urlencode(postData).encode(encoding='gbk'))
                        html_doc = html.decode(encoding='gbk', errors='ignore')
                        soup = BeautifulSoup(html_doc, 'html.parser')
                        _trs = soup.find('table', {'class': 'cxjg'}).findAll('tr')
                        query_info = []
                        for tr in _trs:
                            _td = (tr.findAll('td'))[1]
                            query_keys = re.findall(r'\d+', _td.a['onclick'])
                            if len(query_keys) == 1: query_keys.append('')
                            query_info.append(query_keys)
                        sub_info = self.load_insurancer_info(query_info)
                        insurancer_info.extend(sub_info)
                    except Exception as e:
                        continue
                    else:
                        print('finished: %s on page %d / %d' % (self.name_lst[i], currPage, pages))
                        currPage += 1
            except Exception as e:
                continue
            else:
                print('finished: %s' % self.name_lst[i])
                i += 1
                lock.acquire()
                self.save_to_csvfile(data=insurancer_info)
                lock.release()

    def load_insurancer_info(self, query_info):
        i = 0
        insurancer_info = []
        try:
            while i < len(query_info):
                try:
                    query_keys = query_info[i]
                    postData = {
                        'peopleId': query_keys[0],
                        'certificateCode': query_keys[1]
                    }
                    query_url = 'http://iir.circ.gov.cn/web/nametoinfo!toinfo.html'
                    html = self.get_html(url=query_url, data=urlencode(postData).encode(encoding='gbk'))
                    html_doc = html.decode(encoding='gbk', errors='ignore')
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    _table = ((soup.findAll('table'))[1]).find('table')
                    _tds = _table.findAll('td')
                    insurancer = []
                    for _td in _tds:
                        insurancer.append((_td.get_text()).strip())
                    if (insurancer[-2]).startswith('重庆'):
                        insurancer_info.append(insurancer)
                    print('finished:', query_keys)
                except Exception as e:
                    pass
                i += 1
        finally:
            return insurancer_info


def multi_threads_running(threads_count, begin=1, length=0):
    step = length
    t1 = time.time()
    _spider = InfoSpider()
    threads_pool = []
    for i in range(threads_count):
        start = begin + i * step
        end = start + step
        # print(start, end)
        t = threading.Thread(target=_spider.collection_info, args=(start, end))
        threads_pool.append(t)
    for t in threads_pool:
        t.start()
        time.sleep(1)
    for t in threads_pool:
        t.join()
    t2 = time.time()
    print('cost: %f' % (t2 - t1))


if __name__ == '__main__':
    multi_threads_running(threads_count=1, begin=0, length=1) # not finished
