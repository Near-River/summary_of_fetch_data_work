# -*- coding: utf-8 -*-

"""
中国平安：http://life.pingan.com/
保险代理人信息采集
"""

import requests
import time
import random
import json
import csv
import threading
from bs4 import BeautifulSoup
from math import floor
from urllib.parse import urlencode

from util.load_province_city_info import get_province_city_info

lock = threading.Lock()
headers = {
    'Host': 'life.pingan.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,en-US;q=0.8,zh;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://life.pingan.com/kehufuwu/fuwugongju/return_select.shtml',
    'Connection': 'keep-alive'
}


class AgentInfoSpider(object):
    def __init__(self):
        self.province_city_info = get_province_city_info()

    def build_url(self, provinceId, cityId, currTime, randRex, signature, pageNo, pageSize=100):
        url = 'https://sales.pa18.com/life/toolbox.queryAgentsManualSelection.shtml?' + \
              'provinceCode=' + str(provinceId) + '&' + \
              'cityCode=' + str(cityId) + '&' + \
              'regionCode=&' + \
              'sex=&' \
              'age=&' + \
              'currentTime=' + str(currTime) + '&' + \
              'roundRex=' + randRex + '&' + \
              urlencode({'signature': signature}) + '&' + \
              'pageSize=' + str(pageSize) + '&' + \
              'pageNo=' + str(pageNo) + '&' + \
              'random=&' + \
              'jsoncallback=success_jsoncallback'
        return url

    def get_agent_info_by_page(self, session, provinceId, cityId, pageNo, flag=False):
        while True:
            # Step1：获取签名
            # http://life.pingan.com/binfenxiari/signOfAgent.do?provinceCode=1&cityCode=1&regionCode=&sex=&age=&currentTime=1484036252469&roundRex=58391&_=1484036252470
            randRex = ''
            for i in range(5): randRex += str(floor(random.random() * 10))  # 生成随机数
            currTime = int(time.time() * 1000)
            queries = {
                'provinceCode': provinceId,
                'cityCode': cityId,
                'regionCode': '',
                'sex': '',
                'age': '',
                'currentTime': currTime,
                'roundRex': randRex
            }
            url = 'http://life.pingan.com/binfenxiari/signOfAgent.do?' + urlencode(queries)
            html = session.get(url=url)
            signature = json.loads(html.text)['sign']
            # print('signature:', signature)

            # Step2: 请求并解析数据
            url = self.build_url(provinceId, cityId, currTime, randRex, signature, pageNo)
            # print(url)
            html_txt = session.get(url=url).text
            jsonObj = json.loads(html_txt[html_txt.index('(') + 1:html_txt.rindex(')')])
            if jsonObj['RESFLAG'] == 'Y':
                totalPages = jsonObj['pageBean']['totalPageSize']
                print('finished load page:', pageNo)
                if flag: print('totalResults:', jsonObj['pageBean']['totalResults'])
                return totalPages, jsonObj['resultList']
            else:
                print('empty result.')
                time.sleep(2)

    def parse_agent_info(self, agents):
        agent_info = []
        # https://sales.pa18.com/recruitment.queryHomePageDetail.shtml?empNo=1010456085
        for agent in agents:
            name = agent['NAME']
            intro = agent['SELFINTRODUCE']
            email = agent['EMAIL']
            mobile = agent['MOBILE']
            agentId = agent['AGENTID']
            try:
                url = 'https://sales.pa18.com/recruitment.queryHomePageDetail.shtml?empNo=' + str(agentId)
                html = requests.get(url=url)
                soup = BeautifulSoup(html.text, 'html.parser')
                person_p = soup.find('div', {'class': 'person'}).p.get_text()
                temp = str(person_p).split('\r\n')
                tel = temp[-2].strip().split('：')[-1]
                agency = temp[-1].strip().split('：')[-1]
                agent_info.append((name, agentId, email, mobile, tel, agency, intro))
                # print('parse over:', agentId)
            except Exception as e:
                continue
        return agent_info

    def save_to_csvfile(self, data, title=False):
        with open('../data/agent.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if title:
                writer.writerow(data)
            else:
                writer.writerows(data)

    def sub_collect_agent_info(self, session, provinceId, cityId, startPage, endPage):
        for page in range(startPage, endPage):
            try:
                _, agents = self.get_agent_info_by_page(session, provinceId, cityId, page)
                agent_info = self.parse_agent_info(agents)
                lock.acquire()
                self.save_to_csvfile(agent_info)
                lock.release()
            except Exception as e:
                print('failed at load page:', page)

    def collect_agent_info(self, provinceId, cityId):
        session = requests.Session()
        session.headers.update(headers)
        totalPages, _ = self.get_agent_info_by_page(session, provinceId, cityId, pageNo=1, flag=True)
        print('totalPages:', totalPages)

        threads_pool = []
        threads_count = 10
        step = totalPages // threads_count if totalPages % threads_count == 0 else totalPages // threads_count + 1
        begin = 1
        for i in range(threads_count):
            start = begin + i * step
            end = start + step
            if end > (totalPages + 1): end = totalPages + 1
            t = threading.Thread(target=self.sub_collect_agent_info, args=(session, provinceId, cityId, start, end))
            threads_pool.append(t)
        for t in threads_pool:
            t.start()
            time.sleep(3)
        for t in threads_pool:
            t.join()


def fetch_agent_info(start=0, end=0):
    while start < end:
        spider = AgentInfoSpider()
        provinceId, cityId, cityname = spider.province_city_info[start]
        spider.collect_agent_info(provinceId, cityId)
        start += 1


if __name__ == '__main__':
    spider = AgentInfoSpider()
    titles = ['姓名', '业务代码', '邮箱', '手机', '办公电话', '所属机构', '自我介绍']
    # spider.save_to_csvfile(titles, title=True)

    # spider.collect_agent_info(provinceId=11, cityId=26)
    s = 111
    fetch_agent_info(start=s, end=s + 1)
    # end = 373
