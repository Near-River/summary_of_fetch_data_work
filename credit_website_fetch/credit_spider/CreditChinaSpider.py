# -*- coding: utf-8 -*-

"""
信用中国：

会封锁IP，需要改进为代理IP机制
"""

__author__ = 'Nate_River'

import requests
import csv
import time
import threading
import json
from bs4 import BeautifulSoup
from util.loadID import load_all_ids

All_ids = load_all_ids()

lock = threading.Lock()
headers = {
    "Host": "www.creditchina.gov.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    'Referer': 'http://www.creditchina.gov.cn/search_all'
}


class InfoSpider(object):
    def save_to_csvfile(self, raw_data):
        with open('credit_china_info.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(raw_data)

    def collection_info(self, start, end, area):
        global All_ids
        session = requests.session()
        session.headers.update(headers)
        url = 'http://www.creditchina.gov.cn/credit_info_search?t='
        i = start
        postData = {
            "keyword": "",
            "searchtype": "0",
            "areas": "",
            "creditType": "",
            "dataType": "1",
            "areaCode": "",
            "templateId": "",
            "exact": "0",
            "page": "1"
        }
        enterprise_info = []
        all_ids = All_ids[area]
        while i < end:
            keyword = str(all_ids[i])
            try:
                currTime = str(int(time.time() * 1000))
                search_url = url + currTime
                postData['keyword'] = keyword
                html_txt = session.post(url=search_url, data=postData).text
                jsonObj = json.loads(html_txt)
                if len(jsonObj['result']['results']) == 0:
                    i += 1
                    continue
                encryStr = jsonObj['result']['results'][0]['encryStr']
                idCardOrOrgCode = jsonObj['result']['results'][0]['idCardOrOrgCode']
            except Exception as e:
                time.sleep(1)
                continue
            else:
                if keyword == idCardOrOrgCode:
                    print('load:', keyword)
                    link = 'http://www.creditchina.gov.cn/credit_info_detail?objectType=2&encryStr=' + encryStr
                    enterprise_info.append(self.load_enterprise_info(session, link))
                i += 1
        lock.acquire()
        self.save_to_csvfile(raw_data=enterprise_info)
        lock.release()

    def load_enterprise_info(self, session, link):
        info = []
        while True:
            try:
                html_txt = session.get(link).text
                soup = BeautifulSoup(html_txt, 'html.parser')
                div = soup.find('div', {'class': 'creditsearch-tagsinfo'})
            except Exception as e:
                continue
            else:
                lis = div.findAll('li')
                for li in lis:
                    raw_txt = li.get_text().strip()
                    info.append(raw_txt.split('：')[-1])
                return info


def multi_threads_running(threads_count, rows=-1):
    cols = len(All_ids)
    if rows == -1: rows = len(All_ids[0])
    for c in range(cols):
        step = rows // threads_count if rows % threads_count == 0 else rows // threads_count + 1
        t1 = time.time()
        threads_pool = []
        begin = 0
        spider = InfoSpider()
        for i in range(threads_count):
            start = begin + i * step
            end = start + step
            if end >= rows: end = rows
            # print(start, end)
            t = threading.Thread(target=spider.collection_info, args=(start, end, c))
            threads_pool.append(t)
        for t in threads_pool:
            t.start()
            time.sleep(1)
        for t in threads_pool:
            t.join()
        t2 = time.time()
        print('cost: %f' % (t2 - t1))


if __name__ == '__main__':
    multi_threads_running(threads_count=10, rows=20000)  # not finished
    # spider = InfoSpider()
    # spider.save_to_csvfile(raw_data=[['工商注册号', '法人', '企业类型', '住所', '成立日期', '登记机关']])
