# -*- coding: utf-8 -*-

"""
测试一个城市下每个区的有效的生成企业注册号个数：
"""

__author__ = 'YangXiao'

import re
import time
from util.loadID import load_all_ids
from spider.BaseSpider import BaseSpider
import threading

lock = threading.Lock()

Headers = {
    'Host': 'www.shuidixy.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Connection': 'Keep-Alive',
    'Upgrade-Insecure-Requests': '1'
}
All_ids = load_all_ids()


class LinksSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.opener = self.get_opener(Headers)

    def check_ids(self, start, stop, step, length, all_ids, area):
        info_count = 0
        end = start + step
        i = start
        while end < stop:
            retrial_count = 0
            while i < end:
                id = all_ids[i]
                url = 'http://www.shuidixy.com/search?key=' + str(id)
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
                        info_count += 1
                    i += 1
                    print('Area', area, 'Curr:', i)
                except Exception:
                    if result != 'empty' and len(result) == 0: i += 1
                    retrial_count += 1
                    print('Retry Count:', retrial_count)
                    if retrial_count > 25:
                        self.change_opener(Headers)
                        retrial_count = 0
            start += length
            end = start + step
        return info_count

    def load_links_number(self, loops):
        global All_ids
        t1 = time.time()
        threads_pool = []
        for i in range(len(All_ids)):
            t = threading.Thread(target=self.load_area_links_number, args=(i, All_ids[i], loops))
            threads_pool.append(t)
        for t in threads_pool:
            t.start()
            time.sleep(1)
        for t in threads_pool:
            t.join()

        t2 = time.time()
        print('LinkSpiderTest Cost: %f' % (t2 - t1))

    def load_area_links_number(self, area, all_ids, loops):
        record = []
        begin = 0
        step = 1000
        for j in range(loops):
            start = begin + j * step
            end = start + step
            # print(start, end)
            links_count = self.check_ids(start=start, stop=end, step=5, length=100, all_ids=all_ids, area=area)
            if links_count == 0: continue
            record.append(j)
        record = ' '.join(list(map(lambda x: str(x), record)))
        lock.acquire()
        with open('../data/record.txt', 'a') as f:
            f.write(str(area) + ':' + str(record) + '\n')
        lock.release()


'''
if __name__ == '__main__':
    spider = LinksSpider()
    spider.load_links_number()
'''
