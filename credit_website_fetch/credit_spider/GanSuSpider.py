# -*- coding: utf-8 -*-

"""
信用甘肃：
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
            with open('enterprise_info.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(raw_data)
        else:
            data = []
            for enterprise in raw_data:
                data.append(
                    (
                        enterprise['企业名称'], enterprise['统一社会信用代码'], enterprise['登记证号'],
                        enterprise['企业类型'], enterprise['法定代表人'], enterprise['所属行业'],
                        enterprise['注册资本（万元）'], enterprise['经营范围'], enterprise['成立日期'],
                        enterprise['注册地址'], enterprise['经营期限起'], enterprise['登记机关'],
                        enterprise['登记状态']
                    )
                )
            with open('enterprise_info_over.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(data)

    def collection_info(self, start, end):
        search_url = 'http://www.gscredit.gov.cn/queryXyxxList-L.jspx'
        titles = ['企业名称', '统一社会信用代码', '登记证号', '企业类型', '法定代表人', '所属行业', '注册资本（万元）',
                  '经营范围', '成立日期', '注册地址', '经营期限起', '登记机关', '登记状态']  # 标题信息
        if start == 1: self.save_to_csvfile(raw_data=[titles], title=True)
        i = start
        while i < end:
            currPage = str(i)
            postData = {
                'pageNo': currPage,
                'name': '有限公司',
                'gsdjh': '',
                'lcreditcode': '',
                'type': '1'
            }
            try:
                html = requests.post(url=search_url, data=postData)
                soup = BeautifulSoup(html.text, 'html.parser')
                buttons = soup.findAll('button', {'class': 'btn green fz12 '})
                # print(len(buttons))
            except Exception as e:
                continue
            else:
                print('loaded page %s, preparing for parse.' % currPage)
                links = []
                for button in buttons:
                    click_info = button['onclick']
                    link = click_info[click_info.index('(') + 2:click_info.index(')') - 1]
                    links.append('http://www.gscredit.gov.cn' + link)
                print('load links over on page', currPage)
                enterpriseLst = self.load_enterprise_info(links)
                lock.acquire()
                self.save_to_csvfile(raw_data=enterpriseLst)
                lock.release()
                print('Page %d Over.' % i)
                i += 1

    def load_enterprise_info(self, links):
        i = 0
        enterpriseLst = []
        while i < len(links):
            try:
                url = links[i]
                # print(url)
                html = requests.get(url=url)
                soup = BeautifulSoup(html.text, 'html.parser')
                trs = soup.findAll('tr')[:2]
                info_tables = soup.findAll('table', {'class', 'table-list-modl fz12 row'})
                info_table = None
                for table in info_tables:
                    first_th = table.find('th').get_text().strip()
                    if first_th == '企业类型':
                        info_table = table
                        break
            except Exception as e:
                continue
            else:
                enterprise = {}
                tr1, tr2 = trs[0], trs[1]
                tds1 = tr1.findAll('td')
                tds2 = tr2.findAll('td')
                enterprise['企业名称'] = tds1[1].get_text().strip()
                enterprise['统一社会信用代码'] = tds1[3].get_text().strip()
                enterprise['登记证号'] = tds2[1].get_text().strip()
                # 工商信息
                tds = info_table.findAll('td')
                info_lst = [t.get_text().strip() for t in tds]
                enterprise['企业类型'] = info_lst[0]
                enterprise['法定代表人'] = info_lst[1]
                enterprise['所属行业'] = info_lst[2]
                enterprise['注册资本（万元）'] = info_lst[3]
                enterprise['经营范围'] = info_lst[4]
                enterprise['成立日期'] = info_lst[5]
                enterprise['注册地址'] = info_lst[6] if info_lst[6] != 'null' else ''
                enterprise['经营期限起'] = info_lst[7]
                enterprise['登记机关'] = info_lst[8]
                enterprise['登记状态'] = info_lst[9]
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
    multi_threads_running(threads_count=20, begin=962, length=27, final=12522)  # not finished
    # 12521 pages

    # test cases:
    spider = InfoSpider()
    # spider.collection_info(1, 2)
    # enterprises = spider.load_enterprise_info(
    #     ['http://www.gscredit.gov.cn/queryXyxxview-2016034967-L.jspx'])
    # for e in enterprises: print(e)
