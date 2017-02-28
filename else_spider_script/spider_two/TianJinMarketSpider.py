# -*- coding: utf-8 -*-

"""
天津主体市场信用信息公示系统
"""

__author__ = 'YangXiao'

import os, sys

tempDir = os.path.abspath('../')
sys.path.append(tempDir)

import requests
import csv
import time
import threading
from bs4 import BeautifulSoup
from util.loadID import load_all_ids

All_ids = load_all_ids()
lock = threading.Lock()

Headers = {
    'Host': 'www.tjcredit.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Referer': 'http://www.tjcredit.gov.cn/gsxt/home/index?link=noticeListDiv',
    'Connection': 'Keep-Alive',
    'X-Requested-With': 'XMLHttpRequest'
}


class InfoSpider(object):
    def save_to_csvfile(self, raw_data):
        with open('../data/enterprise_info.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(raw_data)

    def parse_enterprise_info(self, session, search_id):
        url = 'http://www.tjcredit.gov.cn/gsxt/platform/viewInfo.json?gsdjlx=1&entId=' + search_id + '&wbjCode=scjgw&type=reginfo'
        while True:
            try:
                html_txt = session.get(url=url).text
                soup = BeautifulSoup(html_txt.replace('</br>', '/'), 'html.parser')
                info_table = soup.find('table', {'class', 'info-table'})
                if info_table is None: continue
            except Exception as e:
                continue
            else:
                try:
                    info = []
                    tds = info_table.findAll('td')[1:]
                    tds = [td for i, td in enumerate(tds) if i % 2 == 1]
                    for td in tds:
                        info.append(td.get_text().strip())
                    return info
                except:
                    return None

    def load_basic_info(self, session, company_id):
        while True:
            try:
                url = 'http://www.tjcredit.gov.cn/gsxt/platform/searchResult?searchName=' + company_id + '&searchType=WHOLE_WORD_SEARCH'
                html_txt = session.get(url=url).text
                soup = BeautifulSoup(html_txt, 'html.parser')
                div = soup.find('div', {'class': 'content-title'})
                if div is None: continue
                cont = soup.find('dl', {'class': 'content-list'})
                if cont is None: return None
            except Exception as e:
                continue
            else:
                onclick = cont.a['onclick'].strip()
                search_id = onclick[onclick.index("'") + 1:onclick.index("',")]
                # print(search_id)
                info = self.parse_enterprise_info(session, search_id)
                return info

    def collection_info(self, area=0, start=0, end=20000):
        session = requests.Session()
        session.headers.update(Headers)
        basic_info = []
        ids = All_ids[area][start:end]
        try:
            i = 0
            while i < len(ids):
                company_id = ids[i]
                result = self.load_basic_info(session, company_id=company_id)
                if result is not None:
                    basic_info.append(result)
                i += 1
                print('Current:', i)
            print('finished %s' % threading.current_thread().getName())
        finally:
            # save the enterprise data
            lock.acquire()
            self.save_to_csvfile(basic_info)
            lock.release()


def main(threads_count=0, length=20000):
    areas = len(All_ids)
    for area in range(areas):
        t1 = time.time()
        # 多线程采集
        threads_pool = []
        begin = 0
        step = length // threads_count if length % threads_count == 0 else length // threads_count + 1
        for i in range(threads_count):
            start = begin + i * step
            end = start + step
            if end > length: end = length
            _spider = InfoSpider()
            threads_pool.append(threading.Thread(target=_spider.collection_info, args=(area, start, end)))
        for t in threads_pool:
            t.start()
            time.sleep(1)
        for t in threads_pool:
            t.join()
        t2 = time.time()
        print('Cost: %f' % (t2 - t1))


if __name__ == '__main__':
    # 多线程采集
    main(threads_count=100, length=11700)

    # titles = ['营业执照注册号/统一社会信用代码', '名称', '类型', '法定代表人', '注册资本', '成立日期',
    #           '住所', '营业期限自', '营业期限至', '经营范围', '登记机关', '核准日期', '登记状态']  # 标题信息
    # spider = InfoSpider()
    # spider.save_to_csvfile(raw_data=[titles])
