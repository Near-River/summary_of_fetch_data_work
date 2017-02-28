# -*- coding: utf-8 -*-

"""
保险代理人信息采集：

根据peopleId字段进行采集
"""

__author__ = 'YangXiao'

import urllib.request
import http.cookiejar
import csv
import re
import time
import threading

lock = threading.Lock()
csv_file = 'info.csv'

Headers = {
    'Host': 'iir.circ.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Connection': 'Keep-Alive',
    'Referer': 'iir.circ.gov.cn',
    'Upgrade-Insecure-Requests': '1'
}


class InfoSpider(object):
    def __init__(self):
        self.opener = self.get_opener(Headers)

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

    def get_html(self, url, retries=6):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, timeout=10).read()  # 设置超时时间为10秒
            return data
        except urllib.request.URLError as e:
            if retries > 0: return self.get_html(retries - 1)
            return b''

    def savetities_to_csvfile(self, titles):
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(titles)

    def save_to_csvfile(self, list_info):
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(list_info)

    def load_basic_info(self, peopleId=0):
        try:
            url = 'http://iir.circ.gov.cn/web/nametoinfo!toinfo.html?peopleId=' + str(peopleId)
            html = self.get_html(url)
            html_doc = html.decode(encoding='gbk', errors='ignore')
        except Exception as e:
            # 网络故障：目标网页未获取
            return 'empty_result'
        pattern = re.compile(
            r'<tr>.*?<th>.*?</th>.*?<td>(.*?)</td>.*?</tr>',
            re.DOTALL
        )
        result = pattern.findall(html_doc)
        info = []
        if len(result) > 0:
            info = result[:4] + result[5:11]
            # print(info)
        return info

    def collection_info(self, start, end):
        titles = ['姓名', '性别', '资格证书号码', '资格证书状态', '执业证编号', '执业证状态', '有效截止日期'
            , '业务范围', '执业区域', '所属公司']  # 标题信息
        basic_info = []
        if start == 0: self.savetities_to_csvfile(titles=titles)
        try:
            i = start
            while i < end:
                result = self.load_basic_info(peopleId=i)
                if result == 'empty_result':
                    pass
                elif result:
                    basic_info.append(result)
                i += 1
                print('Current:', i)
            print('finished %s' % threading.current_thread().getName())
        finally:
            lock.acquire()
            self.save_to_csvfile(basic_info)
            lock.release()


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
    main(threads_count=200, begin=17000000, step=5000)
    # running: 1900, 0000 -- 2000, 0000: over
    # running: 1800, 0000 -- 1900, 0000: over
    # running: 1700, 0000 -- 1800, 0000: over
