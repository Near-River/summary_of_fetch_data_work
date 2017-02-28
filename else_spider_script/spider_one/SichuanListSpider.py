# -*- coding: utf-8 -*-

"""
采集国家企业信用信息公示系统（四川）：经营异常名录信息
"""

__author__ = 'YangXiao'

import urllib.request
import http.cookiejar
import gzip
import csv
import re
import time
import threading

lock = threading.Lock()

Headers = {
    'Host': 'gsxt.scaic.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Connection': 'Keep-Alive',
    'Referer': 'http://gsxt.scaic.gov.cn/ztxy.do?method=index&random=1479564272180',
    'Upgrade-Insecure-Requests': '1'
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

    def get_html(self, url, retries=6):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, timeout=10).read()  # 设置超时时间为10秒
            return data
        except urllib.request.URLError as e:
            if retries > 0: return self.get_html(retries - 1)
            # print(e.reason)
            return b''

    def savetities_to_csvfile(self, titles):
        with open('1800_2000.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(titles)

    def save_to_csvfile(self, list_info):
        with open('1800_2000.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(list_info)

    def load_list_info(self, page):
        # http://gsxt.scaic.gov.cn/xxcx.do?method=ycmlIndex&random=1479564209367&cxyzm=no&entnameold=&djjg=&maent.entname=&page.currentPageNo=1&yzm=
        try:
            random = str(int(1000 * time.time()))
            url = 'http://gsxt.scaic.gov.cn/xxcx.do?method=ycmlIndex&random=' + random + \
                  '&cxyzm=no&entnameold=&djjg=&maent.entname=&page.currentPageNo=' + str(page) + '&yzm='
            html = self.get_html(url)
            html_doc = html.decode(encoding='gbk', errors='ignore')
        except Exception as e:
            # 网络故障：目标网页未获取
            return 'http_error'
        # <div class="tb-a">...</div>
        pattern1 = re.compile(
            r'<div class="tb-a">.*?</div>',
            re.DOTALL
        )
        if len(pattern1.findall(html_doc)) == 0: return 'empty_result'
        '''
        <ul>
            <li style="cursor:pointer;" class="tb-a1">
                <a onclick="javascript:doOpen('5100000000088185');">四川意思房产营销策划有限公司</a>
            </li>
            <li class="tb-a2">510000000105354</li>
            <li class="tb-a3">2015年7月14日</li>
        </ul>
        '''
        pattern2 = re.compile(
            r'<div.*?class="tb-.*?>.*?<ul>.*?<li.*?>.*?<a.*?>(.*?)</a>.*?</li>.*?<li.*?>(.*?)</li>.*?<li.*?>(.*?)</li>.*?</ul>.*?</div>',
            re.DOTALL
        )
        result = pattern2.findall(html_doc)
        info = []
        if len(result) > 0:
            for elem in result:
                elem = list(map(
                    lambda x: x.replace('&nbsp;', ' ').replace('\r\n', '').replace('\t', '').strip(),
                    elem))
                info.append(elem)
        return info

    def collection_info(self, start, end):
        titles = ['企业名称', '注册号/统一社会信用代码', '被列入经营异常名录日期']  # 标题信息
        list_info = []
        if start == 0: self.savetities_to_csvfile(titles=titles)
        try:
            i = start
            count = 0
            while i < end:
                Headers['Referer'] = 'http://gsxt.scaic.gov.cn/ztxy.do?method=index&random=' + str(
                    int(1000 * time.time()))
                self.opener = self.get_opener(Headers)
                page = i + 1
                result = self.load_list_info(page=page)
                if result == 'http_error':
                    continue
                elif result == 'empty_result':
                    continue
                elif result:
                    list_info.extend(result)
                i += 1
                print('Current:', i)
                count += 1
                if count % 20 == 0: time.sleep(8)
            print('finished %s' % threading.current_thread().getName())
        finally:
            lock.acquire()
            self.save_to_csvfile(list_info)
            lock.release()


def main(threads_count=0):
    t1 = time.time()
    # 多线程采集
    threads_pool = []
    begin = 0
    for i in range(threads_count):
        start = begin + i * 10
        end = start + 10
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
    # main(threads_count=10)
    spider = InfoSpider()
    spider.collection_info(0, 100)
