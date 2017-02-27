# -*- coding: utf-8 -*-

"""
信用山西：
"""

__author__ = 'Nate_River'

import requests
import csv
import time
import threading
from random import random
from bs4 import BeautifulSoup

lock = threading.Lock()
headers = {
    "Host": "www.shanxicredit.gov.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}


class InfoSpider(object):
    def __init__(self):
        pass

    def save_to_csvfile(self, raw_data):
        with open('enterprise_info.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(raw_data)

    def collection_info(self, start, end):
        session = requests.session()
        session.headers.update(headers)
        url = 'http://www.shanxicredit.gov.cn/shanxi/group_license2?page='
        titles = ['企业名称', '统一社会信用代码/注册号', '类型', '法人代表', '注册资本', '成立日期',
                  '住所', '营业期限自', '营业期限至', '经营范围', '登记机关', '核准日期', '登记状态']  # 标题信息
        if start == 1: self.save_to_csvfile(raw_data=[titles])
        i = start
        lst = []
        with open('../temp/help.txt', encoding='utf-8') as f:
            for line in f.readlines():
                tempArr = line.split(' ')
                if len(tempArr) > 2 and tempArr[0].strip() == 'Page':
                    lst.append(int(tempArr[1]))
        while i < end:
            if i in lst:
                i += 1
                continue
            currPage = str(i)
            try:
                search_url = url + currPage
                html = session.get(url=search_url)
                # print(html.text)
                soup = BeautifulSoup(html.text, 'html.parser')
                ul = soup.find('ul', {'class': 'card-showcase'})
                if ul is None: continue
            except Exception as e:
                continue
            else:
                a_s = ul.findAll('a')
                links = []
                for a in a_s:
                    links.append('http://www.shanxicredit.gov.cn/shanxi/' + a['href'])
                print('parsed page %s over.' % currPage)
                enterpriseLst = self.load_enterprise_info(session, list(set(links)))
                lock.acquire()
                self.save_to_csvfile(raw_data=enterpriseLst)
                lock.release()
                print('Page %d Over.' % i)
                # time.sleep(3)
                i += 1

    def load_enterprise_info(self, session, links):
        enterprise_info = []
        i = 0
        while i < len(links):
            try:
                link = links[i]
                html_txt = session.get(link).text
                soup = BeautifulSoup(html_txt, 'html.parser')
                table = soup.find('table', {'class': 'table table-bordered table-hover'})
                if table is None:
                    # time.sleep(random() * 3)
                    continue
            except Exception as e:
                continue
            else:
                tds = table.findAll('td')
                info = [e.get_text().replace('\n', '').replace('\t', '') for i, e in enumerate(tds) if i % 2 == 1]
                enterprise_info.append(info[:-1])
                # time.sleep(random() * 2)
                print('parse over:', info[0])
                i += 1
        return enterprise_info


def multi_threads_running(threads_count, begin=1, length=0, final=-1):
    step = length
    t1 = time.time()
    threads_pool = []
    _spider = InfoSpider()
    for i in range(threads_count):
        start = begin + i * step
        end = start + step
        if end >= final != -1:
            end = final
        # print(start, end)
        t = threading.Thread(target=_spider.collection_info, args=(start, end))
        threads_pool.append(t)
    for t in threads_pool:
        t.start()
    for t in threads_pool:
        t.join()
    t2 = time.time()
    print('cost: %f' % (t2 - t1))


if __name__ == '__main__':
    # with open('../temp/help.txt', encoding='utf-8') as f:
    #     for line in f.readlines():
    #         if line.startswith('Page'):
    #             print(line.strip())
    # multi_threads_running(threads_count=20, begin=2733, length=3)  # not finished
    # 103363 pages

    # test cases:
    spider = InfoSpider()
    spider.collection_info(2947, 10001)
