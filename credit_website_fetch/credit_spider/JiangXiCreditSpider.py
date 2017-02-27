# -*- coding: utf-8 -*-

"""
信用江西：
"""

__author__ = 'Nate_River'

import requests
import json
import csv
import time
import threading
from bs4 import BeautifulSoup

postData = {
    'cxnr': '有限公司',
    'cxfw': '',
    'szdq': '',
    'hylx': '',
    'ztlx': '',
    'cxlx': '1',
    'cxfs': '0',
    'pageSize': '15'
}

lock = threading.Lock()


class InfoSpider(object):
    def save_to_csvfile(self, data):
        with open('enterprise_info_over.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data)

    def collection_info(self, start, end):
        global postData
        allEnterpriseLst = []
        search_url = 'http://www.creditjx.gov.cn/DataQuery/company/listNew.json'

        def load_else_info(url):
            html = requests.get(url=url)
            soup = BeautifulSoup(html.text, 'html.parser')
            div = soup.findAll('div', {'class': 'pa w h sorry_Back'})
            if len(div) > 0: return 'not_exist'
            trs = soup.findAll('table')[0].findAll('tr')
            return str(trs[2].td.get_text()).strip(), str(trs[4].findAll('td')[1].get_text()).strip()

        try:
            titles = ['企业名称', '统一社会信用代码', '法定代表人', '注册地址', '状态', '纳税人识别号', '工商注册号', '组织机构代码',
                      '成立日期', '注册资本(万元)', '经营范围']  # 标题信息
            if start == 1: self.save_to_csvfile(data=[titles])
            i = start
            while i < end:
                postData['page'] = str(i)
                try:
                    html = requests.post(url=search_url, data=postData)
                    html_doc = html.text
                    ret = json.loads(html_doc)
                    enterpriseLst = ret['list']
                except Exception as e:
                    continue
                else:
                    # 企业名称： 	新余常康贸易有限公司 	 统一社会信用代码：
                    # 法定代表人： 	邓文萍 	                 注册地址： 	    江西省新余市渝水区四小办公大楼三楼东侧
                    # 状态： 	    正常 	                 纳税人识别号： 	360502677961145
                    # 工商注册号： 	360502210003652 	     组织机构代码： 	677961145
                    # 成立日期： 	2008-07-23 	             注册资本(万元)： 	118
                    # 经营范围： 	医疗器械(Ⅱ、Ⅲ类凭许可证经营）维修销售、机电产品、水暖材料销售.
                    for enterprise in enterpriseLst:
                        enterprise_info = {}
                        enterprise_info['qymc'] = enterprise['qymc'] if enterprise['qymc'] else ''
                        enterprise_info['tyshxydm'] = enterprise['tyshxydm'] if enterprise['tyshxydm'] else ''
                        enterprise_info['fddbr'] = enterprise['fddbr'] if enterprise['fddbr'] else ''
                        enterprise_info['zs'] = enterprise['zs'] if enterprise['zs'] else ''
                        enterprise_info['state'] = ''
                        enterprise_info['nsrsbm'] = enterprise['nsrsbm'] if enterprise['nsrsbm'] else ''
                        enterprise_info['yyzzzch'] = enterprise['yyzzzch'] if enterprise['yyzzzch'] else ''
                        enterprise_info['jgdm'] = enterprise['jgdm'] if enterprise['jgdm'] else ''
                        enterprise_info['insertTime'] = enterprise['insertTime'] if enterprise['insertTime'] else ''
                        enterprise_info['zczb'] = ''
                        enterprise_info['jyfw'] = enterprise['jyfw'] if enterprise['jyfw'] else ''

                        _id = enterprise['xybsm']
                        url = 'http://www.creditjx.gov.cn/DataQuery/company/infoNew/' + str(_id) + '/1'
                        while True:
                            try:
                                if load_else_info(url) == 'not_exist': break
                                state, zczb = load_else_info(url)
                            except Exception as e:
                                continue
                            else:
                                enterprise_info['state'], enterprise_info['zczb'] = state, zczb
                                allEnterpriseLst.append(
                                    (enterprise_info['qymc'], enterprise_info['tyshxydm'],
                                     enterprise_info['fddbr'], enterprise_info['zs'],
                                     enterprise_info['state'], enterprise_info['nsrsbm'],
                                     enterprise_info['yyzzzch'], enterprise_info['jgdm'],
                                     enterprise_info['insertTime'], enterprise_info['zczb'],
                                     enterprise_info['jyfw'])
                                )
                                break
                    print('Page %d Over.' % i)
                    i += 1
        finally:
            lock.acquire()
            self.save_to_csvfile(data=allEnterpriseLst)
            lock.release()


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
    multi_threads_running(threads_count=20, begin=1, length=30) # not finished
    # 61367 pages
