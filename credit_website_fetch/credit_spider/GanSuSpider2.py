# -*- coding: utf-8 -*-

"""
信用甘肃2：

接口二：采集的企业工商信息没有注册号
"""

__author__ = 'Nate_River'

import requests
import csv
import time
import threading
from bs4 import BeautifulSoup

lock = threading.Lock()


class InfoSpider(object):
    def save_to_csvfile(self, data):
        with open('enterprise_info.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data)

    def collection_info(self, start, end):
        search_url = 'http://www.gscredit.gov.cn/faces/enterpriseQuery/gsweb/qyDetialInfo.xhtml?m010101='
        titles = ['企业名称', '营业执照注册号', '注册地址', '工商登记机关', '归类行业', '注册资本（万元）', '市场主体类型',
                  '经营范围', '一般经营范围', '成立日期', '营业期限起始日期', '营业期限到期日期', '注册地址联系电话',
                  '社会信用代码', '法定代表人', '企业类型', '注册资金币种', '核准日期', '登记状态', '经营状态']  # 标题信息
        if start == 62000000000: self.save_to_csvfile(data=[titles])
        enterpriseLst = []
        try:
            i = start
            while i < end:
                randId = str(i)
                try:
                    html = requests.post(url=search_url + randId)
                    soup = BeautifulSoup(html.text, 'html.parser')
                    if '企业名称' not in html.text:
                        print('current:', i)
                        i += 1
                        continue
                except Exception as e:
                    continue
                else:
                    enterpriseLst.append(self.load_enterprise_info(soup))
                    print('current:', i)
                    i += 1
        finally:
            lock.acquire()
            self.save_to_csvfile(data=enterpriseLst)
            lock.release()

    def load_enterprise_info(self, soup):
        table = soup.find('table', 'tb_list')
        enterprise = []
        for tr in table.findAll('tr'):
            tds = tr.findAll('td')
            enterprise.append(tds[1].get_text())
            enterprise.append(tds[3].get_text())
        enterprise = [elem.strip() for elem in enterprise]
        return enterprise


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
    # 62000000000 -- 62020000000
    start = 62000000000
    multi_threads_running(threads_count=100, begin=start, length=1000)  # not finished
    # test cases:
    # spider = InfoSpider()
    # spider.collection_info(start=start, end=start + 18)
