# -*- coding: utf-8 -*-

"""
天眼查企业工商信息采集
"""

__author__ = 'YangXiao'

import requests
import csv
import time
import threading
from bs4 import BeautifulSoup
from util.loadID import load_all_ids

All_ids = load_all_ids()
lock = threading.Lock()

Headers = {
    'Host': 'www.tianyancha.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Tyc-From': 'normal',
    'loop': 'null',
    'CheckError': 'check',
    'Connection': 'Keep-Alive',
    'Cache-Control': 'max-age=0'
}


class InfoSpider(object):
    def load_basic_info(self, session, company_id):
        try:
            header = {'Referer': 'http://www.tianyancha.com/search?key=' + company_id + '&checkFrom=searchBox'}
            session.headers.update(header)
            url = 'http://www.tianyancha.com/wxApi/getJsSdkConfig.json?url=http://www.tianyancha.com/search?key=120000000000028&checkFrom=searchBox'
            print(session.get(url).text)
            exit()
            # print('Referer:', session.headers['Referer'])
            url = 'http://www.tianyancha.com/search/' + company_id + '.json?'
            html_txt = session.get(url=url).text

            print(html_txt)
        except Exception as e:
            # 网络故障：目标网页未获取
            return 'empty_result'
        else:
            info = []
            time.sleep(1)
        return info

    def collection_info(self, area=0):
        session = requests.Session()
        session.headers.update(Headers)
        basic_info = []
        ids = All_ids[area][2:3]
        print(ids)
        try:
            i = 0
            while i < len(ids):
                company_id = ids[i]
                result = self.load_basic_info(session, company_id=company_id)
                if result == 'empty_result':
                    pass
                elif result:
                    basic_info.append(result)
                i += 1
                print('Current:', i)
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
