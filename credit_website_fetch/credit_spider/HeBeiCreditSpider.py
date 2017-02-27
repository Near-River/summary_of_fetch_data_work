# -*- coding: utf-8 -*-

"""
信用河北：
"""

__author__ = 'Nate_River'

import requests
import csv
import time
import threading
from bs4 import BeautifulSoup

lock = threading.Lock()


class InfoSpider(object):
    def save_to_csvfile(self, raw_data, title=False):
        if title:
            with open('enterprise_info_over.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(raw_data)
        else:
            data = []
            for enterprise in raw_data:
                data.append(
                    (
                        enterprise['企业名称'], enterprise['法定代表人'], enterprise['住所'],
                        enterprise['工商注册号'], enterprise['工商登记机关'], enterprise['企业类型'],
                        enterprise['注册资本(万元)'], enterprise['经营范围'], enterprise['成立日期'],
                        enterprise['状态'], enterprise['税务登记代码'], enterprise['经营期限']
                    )
                )
            with open('enterprise_info_over.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(data)

    def collection_info(self, start, end):
        allEnterpriseLst = []
        search_url = 'http://www.credithebei.gov.cn/queryList.jspx?keyword=%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&object=2&areas=&sources='
        try:
            titles = ['企业名称', '法定代表人', '住所', '工商注册号', '工商登记机关', '企业类型',
                      '注册资本(万元)', '经营范围', '成立日期', '状态', '税务登记代码', '经营期限']  # 标题信息
            if start == 1: self.save_to_csvfile(raw_data=[titles], title=True)
            i = start
            while i < end:
                currPage = str(i)
                try:
                    html = requests.post(url=search_url, data={'pageNo': currPage})
                    soup = BeautifulSoup(html.text, 'html.parser')
                    content_div = soup.find('div', {'class': 'cx_jg'})
                    trs = content_div.findAll('tr')[1:]
                except Exception as e:
                    continue
                else:
                    print('loaded page %s, preparing for parse.' % currPage)
                    links = []
                    for tr in trs:
                        link = tr.find('a')
                        links.append('http://www.credithebei.gov.cn' + link['href'])
                    enterpriseLst = self.load_enterprise_info(links)
                    lock.acquire()
                    self.save_to_csvfile(raw_data=enterpriseLst)
                    lock.release()
                    # allEnterpriseLst.extend(enterpriseLst)
                    print('Page %d Over.' % i)
                    i += 1
        finally:
            pass
            # lock.acquire()
            # self.save_to_csvfile(raw_data=allEnterpriseLst)
            # lock.release()

    def load_enterprise_info(self, links):
        i = 0
        enterpriseLst = []
        while i < len(links):
            try:
                url = links[i]
                html = requests.get(url=url)
                soup = BeautifulSoup(html.text, 'html.parser')
                xq_divs = soup.findAll('div', {'class', 'xq_div'})
            except Exception as e:
                continue
            else:
                empty_count = 0
                enterprise = {}
                xq_div1 = xq_divs[0]
                xq_div2 = xq_divs[3]
                # 工商信息
                tds1 = xq_div1.findAll('td')
                enterprise['企业名称'] = tds1[1].get_text()
                if tds1[9].get_text() != '无':
                    enterprise['法定代表人'] = tds1[9].get_text()
                else:
                    enterprise['法定代表人'] = '无'
                    empty_count += 1
                if tds1[7].get_text() != '无':
                    enterprise['住所'] = tds1[7].get_text()
                else:
                    enterprise['住所'] = '无'
                    empty_count += 1
                if tds1[3].get_text() != '无':
                    enterprise['工商注册号'] = tds1[3].get_text()
                else:
                    enterprise['工商注册号'] = '无'
                    empty_count += 1
                if tds1[5].get_text() != '无':
                    enterprise['工商登记机关'] = tds1[5].get_text()
                else:
                    enterprise['工商登记机关'] = '无'
                    empty_count += 1
                if tds1[17].get_text() != '无':
                    enterprise['企业类型'] = tds1[17].get_text()
                else:
                    enterprise['企业类型'] = '无'
                    empty_count += 1
                if tds1[15].get_text() != '无':
                    enterprise['注册资本(万元)'] = tds1[15].get_text()
                else:
                    enterprise['注册资本(万元)'] = '无'
                    empty_count += 1
                if tds1[19].get_text() != '无':
                    enterprise['经营范围'] = tds1[19].get_text()
                else:
                    enterprise['经营范围'] = '无'
                    empty_count += 1
                if tds1[21].get_text() != '无':
                    enterprise['成立日期'] = tds1[21].get_text()
                else:
                    enterprise['成立日期'] = '无'
                    empty_count += 1
                if tds1[23].get_text() != '无':
                    enterprise['状态'] = tds1[23].get_text()
                else:
                    enterprise['状态'] = '无'
                    empty_count += 1
                # 税务登记信息
                tds2 = xq_div2.findAll('td')
                if len(tds2) >= 8:
                    enterprise['税务登记代码'] = tds2[1].get_text()
                    if tds2[5].get_text().strip() != '无':
                        enterprise['经营期限'] = tds2[5].get_text() + ' 至 ' + tds2[7].get_text()
                    else:
                        enterprise['经营期限'] = tds2[5].get_text()
                else:
                    enterprise['税务登记代码'] = '无'
                    enterprise['经营期限'] = '无'
                if empty_count < 8:
                    enterpriseLst.append(enterprise)
                    print(enterprise['企业名称'])
                i += 1
        return enterpriseLst


def multi_threads_running(threads_count, begin=1, length=0, final=0):
    step = length
    t1 = time.time()
    _spider = InfoSpider()
    threads_pool = []
    for i in range(threads_count):
        start = begin + i * step
        end = start + step
        if end >= final:
            end = final
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
    spider = InfoSpider()
    spider.collection_info(start=1, end=100)
    # with open('help.txt', encoding='utf-8') as f:
    #     arr = []
    #     for line in f.readlines():
    #         if line.startswith('Page'):
    #             num = int(line.strip().split(' ')[1])
    #             arr.append(num)
    # left_set = set([29901 + i for i in range(100)]) - set(arr)
    # print(left_set)
    # spider = InfoSpider()
    # for e in left_set: spider.collection_info(start=e, end=e + 1)
