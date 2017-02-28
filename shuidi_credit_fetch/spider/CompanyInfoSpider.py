# -*- coding: utf-8 -*-

"""
采集水滴信用网上的企业注册信息：
"""

__author__ = 'YangXiao'

import re
import csv
import os
import time
import threading
from util.loadID import load_company_info
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

lock = threading.Lock()


class CompanyInfoSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.opener = self.get_opener(Headers)
        self.companies_info = load_company_info()

    def savetities_to_csvfile(self, titles, filename):
        file_name = os.path.join(os.path.abspath('../'), 'data', filename)
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(titles)

    def save_to_csvfile(self, info, filename):
        file_name = os.path.join(os.path.abspath('../'), 'data', filename)
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(info)

    def load_company_info(self, url):
        try:
            html = self.get_html(url)
            html_doc = html.decode(encoding='utf-8', errors='ignore')
        except Exception as e:
            # 网络故障：目标网页未获取
            return 'http_error'
        # <div class="sd_left_list" id="registerInfoTurnTo">...</div>
        pattern1 = re.compile(
            r'<div.*?id="registerInfoTurnTo".*?>.*?<div class="panel_body">(.*?)</div>.*?</div>',
            re.DOTALL
        )
        temp_result = pattern1.findall(html_doc)
        if len(temp_result) == 0: return 'empty_result'
        info_txt = temp_result[0]
        pattern2 = re.compile(
            r'<tr>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>.*?</tr>',
            re.DOTALL
        )
        result = pattern2.findall(info_txt)
        info = []
        if len(result) > 0:
            count = 1
            for i in range(len(result) - 1):
                elem = result[i]
                elem = list(map(
                    lambda x: x.replace('&nbsp;', ' ').replace('\r\n', '').replace('\t', '').replace(' ', '').strip(),
                    elem))
                if count == 2:
                    name = elem[0]
                    _pattern = re.compile(r'<a.*?>(.*?)</a>', re.DOTALL)
                    elem[0] = _pattern.findall(name)[0]
                info.extend(elem)
                count += 1
            pattern3 = re.compile(
                r'<tr>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>.*?</tr>',
                re.DOTALL
            )
            result2 = pattern3.findall(info_txt)
            for elem in result2[-3:]:
                elem = elem.replace('&nbsp;', ' ').replace('\r\n', '').replace('\t', '').replace(' ', '').strip(),
                info.extend(elem)
        return info

    def collection_company_info(self, start, end):
        titles = ['企业名称', '工商注册号', '登记状态', '法人代表', '注册资本', '企业信用代码', '登记机关', '成立日期', '营业期限', '企业类型', '企业地址',
                  '经营范围']  # 标题信息
        if start == 0: self.savetities_to_csvfile(titles=titles, filename='company.csv')
        company_info = []
        i = start
        try:
            retrial_count = 0
            while i < end:
                info = self.companies_info[i]
                company_name, search_url = info[0], info[1]
                result = self.load_company_info(search_url)
                if result == 'http_error':
                    retrial_count += 1
                    print('Retry Count:', retrial_count)
                    if retrial_count > 25:
                        self.change_opener(Headers)
                        retrial_count = 0
                    continue
                elif result == 'empty_result':
                    print('Not Found: %s' % company_name)
                elif result:
                    result.insert(0, company_name)
                    company_info.append(result)
                i += 1
                if i % 10 == 0: print('current:', i)
        finally:
            lock.acquire()
            self.save_to_csvfile(info=company_info, filename='company.csv')
            lock.release()
        print('finished ' + threading.current_thread().name)


def multi_threads_running(threads_count, begin=0):
    t1 = time.time()
    _spider = CompanyInfoSpider()
    _size = len(_spider.companies_info)
    step = _size // threads_count if _size % threads_count == 0 else _size // threads_count + 1
    threads_pool = []
    for i in range(threads_count):
        start = begin + i * step
        end = start + step
        # print(start, end)
        if end > _size: end = _size
        t = threading.Thread(target=_spider.collection_company_info, args=(start, end))
        threads_pool.append(t)
    for t in threads_pool:
        t.start()
        time.sleep(1)
    for t in threads_pool:
        t.join()
    t2 = time.time()
    print('cost: %f' % (t2 - t1))


'''
if __name__ == '__main__':
    # 多线程的爬取
    multi_threads_running(threads_count=100, begin=0)
'''
