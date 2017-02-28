# -*- coding: utf-8 -*-

"""
天眼查企业工商信息采集
"""

__author__ = 'YangXiao'

import urllib.request
import http.cookiejar
import csv
import time
import gzip
import threading
from util.loadID import load_all_ids

All_ids = load_all_ids()
lock = threading.Lock()

Headers = {
    'Host': 'www.tianyancha.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Connection': 'Keep-Alive',
    'Tyc-From': 'normal',
    'loop': 'null',
    'CheckError': 'check',
    'Referer': 'http://www.tianyancha.com/search?key=350800100015557&checkFrom=searchBox'
}


class InfoSpider(object):
    def __init__(self):
        self.opener = None

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

    def get_html(self, url, retries=10):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, timeout=10).read()  # 设置超时时间为10秒
            return self.ungzip(data)
        except urllib.request.URLError as e:
            if retries > 0: return self.get_html(retries - 1)
            return b''

    def load_basic_info(self, company_id):
        try:
            currTime = str(int(time.time() * 1000))
            Headers['Referer'] = 'http://www.tianyancha.com/search?key=' + str(company_id) + '&checkFrom=searchBox'
            self.opener = self.get_opener(Headers)
            url = 'http://www.tianyancha.com/search/' + str(company_id) + '.json?'
            print(url)
            html = self.get_html(url)
            html_doc = html.decode(encoding='utf-8', errors='replace')
        except Exception as e:
            # 网络故障：目标网页未获取
            return 'empty_result'
        else:
            print(html_doc)
            exit()
            info = []
        return info

    def collection_info(self, area=0):
        basic_info = []
        ids = All_ids[area][:3]
        print(ids)
        try:
            i = 0
            while i < len(ids):
                company_id = ids[i]
                result = self.load_basic_info(company_id=company_id)
                if result == 'empty_result':
                    pass
                elif result:
                    basic_info.append(result)
                i += 1
                print('Current:', i)
                time.sleep(1)
            print('finished %s' % threading.current_thread().getName())
        finally:
            # save the enterprise data
            pass


def main(threads_count=0, begin=0, step=0):
    t1 = time.time()
    # 多线程采集
    threads_pool = []
    for i in range(threads_count):
        start = begin + i * step
        end = start + step
        _spider = InfoSpider()
        threads_pool.append(threading.Thread(target=_spider.collection_info, args=(start, end)))
    for t in threads_pool:
        t.start()
        time.sleep(1)
    for t in threads_pool:
        t.join()
    t2 = time.time()
    print('Cost: %f' % (t2 - t1))


if __name__ == '__main__':
    # 多线程采集
    # main(threads_count=1, begin=0, step=5)

    spider = InfoSpider()
    spider.collection_info(area=0)
