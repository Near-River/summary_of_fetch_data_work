# -*- coding: utf-8 -*-

"""
采集水滴信用网上的企业链接信息：
"""

__author__ = 'YangXiao'

import csv
import re
import time
import threading
from util.loadID import load_all_ids
from spider.BaseSpider import BaseSpider

Headers = {
    'Host': 'www.shuidixy.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Connection': 'Keep-Alive',
    'Upgrade-Insecure-Requests': '1'
}

ALL_IDS = load_all_ids()
lock = threading.Lock()


class LinksSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.opener = self.get_opener(Headers)
        self.ids = None

    def save_to_csvfile(self, links_info):
        with open('../data/links.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            data = []
            for elem in links_info:
                data.append((elem['company_name'], elem['url']))
            writer.writerows(data)

    def load_all_links(self, start, end):
        i = start
        links_info = []
        try:
            retrial_count = 0
            while i < end:
                _id = self.ids[i]
                url = 'http://www.shuidixy.com/search?key=' + _id
                result = 'empty'
                try:
                    html = self.get_html(url)
                    html_doc = html.decode(encoding='utf-8', errors='ignore')
                    pattern = re.compile(
                        r'<div class="or_search_list">.*?<div class="or_search_row_content">.*?<a href="(.*?)".*?>(.*?)</a>',
                        re.DOTALL
                    )
                    result = pattern.findall(html_doc)
                    if len(result) > 0:
                        link_info = {'url': 'http://www.shuidixy.com' + result[0][0],
                                     'company_name': result[0][1].replace('\t', '').replace('\r\n', '').strip()}
                        # print(link_info)
                        links_info.append(link_info)
                        i += 1
                        if i % 10 == 0: print('Curr:', i)
                        retrial_count = 0
                    else:
                        self.change_opener(Headers)
                except Exception:
                    if result != 'empty' and len(result) == 0: i += 1
                    retrial_count += 1
                    # if retrial_count % 10 == 0: print('Retry Count:', retrial_count)
                    if retrial_count > 50:
                        self.change_opener(Headers)
                        retrial_count = 0
        finally:
            lock.acquire()
            self.save_to_csvfile(links_info)
            lock.release()


def multi_threads_running(threads_count, areaNo=0):
    """
    :param threads_count: 线程数量
    :param areaNo: 起始区号
    """
    with open('../data/record.txt', 'r') as f:
        areaRecord = []
        lines = f.readlines()
        for line in lines:
            sArr = line.strip('\n').split(':')
            areaRecord.append((sArr[0], sArr[1]))
        areaRecord = sorted(areaRecord, key=lambda x: int(x[0]))
    linksNumberRecord = [e2 for (e1, e2) in areaRecord]
    print(linksNumberRecord)

    t1 = time.time()
    _spider = LinksSpider()
    for i in range(areaNo, len(linksNumberRecord)):
        record = linksNumberRecord[i]
        if len(record) > 0:
            record = list(map(lambda x: int(x), record.split(' ')))
            _spider.ids = ALL_IDS[i]
            for _id in record:
                begin = _id * 1000
                step = 1000 // threads_count if 1000 % threads_count == 0 else 1000 // threads_count + 1
                threads_pool = []
                for j in range(threads_count):
                    start = begin + j * step
                    end = start + step
                    if end > (begin + 1000): end = begin + 1000
                    t = threading.Thread(target=_spider.load_all_links, args=(start, end))
                    threads_pool.append(t)
                for t in threads_pool:
                    t.start()
                    time.sleep(1)
                for t in threads_pool:
                    t.join()
        print('Finished Area:', i + 1)
    t2 = time.time()
    print('LinksSpider Cost: %f' % (t2 - t1))


'''
if __name__ == '__main__':
    spider = LinksSpider()
    multi_threads_running(threads_count=10)
'''
