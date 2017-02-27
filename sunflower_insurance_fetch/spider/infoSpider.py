# -*- coding: utf-8 -*-

"""
采集每个城市下所有保险代理人的信息：
最终将采集获得的信息保存到 data 文件夹下的 xx.csv 文件中(xx为对应的城市名称)
"""

__author__ = 'YangXiao'

from util.initDirs import load_cities_info
import urllib.request
import http.cookiejar
import gzip
import re
import csv
import os

URL = 'http://bxr.im'
Headers = {
    'Host': "bxr.im",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive"
}


class InfoSpider(object):
    def __init__(self):
        self.opener = None
        self.cities_info = load_cities_info()

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
            # print('Uncompressed, no decompression.')
            pass
        return data

    def get_html(self, url, retries=3):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, timeout=10).read()  # 设置超时时间为10秒
            return self.ungzip(data)
        except urllib.request.URLError as e:
            if retries > 0: return self.get_html(retries - 1)
            print(url)
            print(e.reason)

    def savetities_to_csvfile(self, city_dir):
        file_name = os.path.join(city_dir, 'agent.csv')
        titles = ['姓名', '公司', '电话', '保险销售执业证号', '保险代理资格证号', '投保方案数',
                  '解答经验', '好评数', '简介']  # 标题信息
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(titles)

    def save_to_csvfile(self, city_dir, all_agent_info):
        file_name = os.path.join(city_dir, 'agent.csv')
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            data = []
            for elem in all_agent_info:
                # agent_name  agent_company   agent_intro
                # insurance_sales_license_number  insurance_agent_qualification_number
                # insurance_scheme_number     answering_experience
                # praise_number   call_number
                data.append((elem['agent_name'], elem['agent_company'], elem['call_number'],
                             elem['insurance_sales_license_number'], elem['insurance_agent_qualification_number'],
                             elem['insurance_scheme_number'], elem['answering_experience'], elem['praise_number'],
                             elem['agent_intro']))
            writer.writerows(data)


    def get_pages_number(self, url):
        # <a href="/sf34-cs398/gs.html?page=213" class="flow-center-item gray999 pageList-link">尾页 »</a>
        html = self.get_html(url)
        html_doc = html.decode(encoding='utf-8', errors='ignore')
        # print(html_doc)
        pattern = re.compile(
            r'<a .*?href=".*?gs.html\?page=(.*?)".*?</a>',
            flags=re.DOTALL
        )
        pages = pattern.findall(html_doc)
        return int(pages[-1]) if len(pages) > 0 else 1

    def load_agent_links(self, url):
        html = self.get_html(url)
        html_doc = html.decode(encoding='utf-8', errors='ignore')
        # <div class="agent-pic">
        # 	<a target="_blank" href="http://bxr.im/645689">
        # 		<img src="..." alt="">
        # 	</a>
        # </div>
        link_pattern = re.compile(
            r'<div class="agent-pic">.*?href="(.*?)".*?</div>',
            flags=re.DOTALL
        )
        links = link_pattern.findall(html_doc)
        return links

    def load_agent_info(self, urls):
        all_agent_info = []
        for url in urls:
            try:
                html = self.get_html(url)
                html_doc = html.decode(encoding='utf-8', errors='ignore')
                agent_info = {}
                # 匹配 姓名、公司和简介
                # <span class="agent-name">牛志军</span>
                # <p class="agent-company">北京&nbsp;&nbsp;平安人寿</p>
                # <div class="agent-intro">
                #   <p>
                #     2001年6月1日加盟平安保险公司，拥有人力资源和社会保障部的全国2级理财规划师资格（国家承认），在很多...
                #     <a class="more text-gray" href="/niuzhijun/jieshao.html">更多&gt;&gt;</a>
                #   </p>
                # </div>
                pattern1 = re.compile(
                    r'<span class="agent-name">(.*?)</span>.*?<p class="agent-company">(.*?)</p>.*?<div class="agent-intro">.*?href="(.*?)".*?</div>',
                    re.DOTALL
                )
                info1 = pattern1.findall(html_doc)[0]
                agent_info['agent_name'] = info1[0]
                company = info1[1].replace('&nbsp;', ' ')
                agent_info['agent_company'] = company
                introduce_url = URL + info1[2]
                intro_html = self.get_html(introduce_url).decode(encoding='utf-8', errors='ignore')
                intro_pattern = re.compile(
                    r'<div class="info-box">.*?<p>(.*?)</p>',
                    re.DOTALL
                )
                introduce = intro_pattern.findall(intro_html)[0]
                introduce = introduce.strip('\r\n').strip()
                agent_info['agent_intro'] = introduce

                # 匹配 保险销售执业证号和保险销售执业证号
                # <div class="left fn-left">
                #     <i class="ui-icon icon-y"></i>保险销售执业证号：02000111010880002010000562
                # </div>
                # <div class="right fn-right">
                #     <i class="ui-icon icon-y"></i>保险销售执业证号：02000111010880002010000562
                # </div>
                pattern2 = re.compile(
                    r'<div class="left fn-left">.*?</i>(.*?)</div>.*?<div class="right fn-right">.*?</i>(.*?)</div>',
                    re.DOTALL
                )
                card_numbers = pattern2.findall(html_doc)[0]
                num_pattern = re.compile(r'([0-9]+?)', re.DOTALL)
                agent_info['insurance_sales_license_number'] = ''.join(num_pattern.findall(card_numbers[0]))
                agent_info['insurance_agent_qualification_number'] = ''.join(num_pattern.findall(card_numbers[1]))

                # 匹配 投保方案、解答经验、好评数
                # <span class="agent-data-num text-orange">5</span>
                # <span class="agent-data-num text-green">817</span>
                # <span class="agent-data-num text-blue">8</span>
                pattern3 = re.compile(
                    r'<span class="agent-data-num text-orange">(.*?)</span>.*?<span class="agent-data-num text-green">(.*?)</span>.*?<span class="agent-data-num text-blue">(.*?)</span>',
                    re.DOTALL
                )
                numbers = pattern3.findall(html_doc)[0]
                agent_info['insurance_scheme_number'] = numbers[0]
                agent_info['answering_experience'] = numbers[1]
                agent_info['praise_number'] = numbers[2]

                # 匹配手机号
                pattern4 = re.compile(
                    r'<a .*?data-call-number="(.*?)".*?</a>',
                    re.DOTALL
                )
                agent_info['call_number'] = pattern4.findall(html_doc)[0]
                all_agent_info.append(agent_info)
            except Exception as e:
                # print('HTTPError:', url)
                with open('../data/error_links.txt', 'a') as f:
                    f.write('HTTPError: ' + str(url))
                    f.write('\n')
                continue

        return all_agent_info

    def crawl_agent_info(self, city_dir, url):
        """
        抓取单个城市下所有保险代理人的信息
        :return:
        """

        def crawl_info():
            page_url = url + '?page=' + str(page)
            # 获取该页下所有保险代理人的链接
            links = self.load_agent_links(page_url)
            # 根据链接获取所有代理人的信息
            all_agent_info = self.load_agent_info(links)
            # 保存代理人信息到目录 city_dir 下
            self.save_to_csvfile(city_dir, all_agent_info)

        # 获取总页数
        pages = self.get_pages_number(url)
        if pages > 0:
            self.savetities_to_csvfile(city_dir)
            for page in range(1, pages + 1):
                i = 0
                try:
                    crawl_info()
                except Exception as e:
                    i += 1
                    if i <= 3:
                        crawl_info()
                    else:
                        # print('Exception occupied at page %d (%s):' % (page, city_dir))
                        with open('../data/errors_record.txt', 'a') as f:
                            f.write('Exception occupied at ' + str(page) + ' (' + str(city_dir) + ')')
                            f.write('\n')

    def collection_info(self):
        """
        采集每个城市下所有保险代理人的信息
        :return:
        """
        start = 0
        end = len(self.cities_info)
        self.opener = self.get_opener(Headers)
        for i in range(start, end):
            (city_dir, url) = self.cities_info[i]
            # print(city_dir, url)
            self.crawl_agent_info(city_dir, url)
            print('city %s end.' % city_dir)


'''
if __name__ == '__main__':
    spider = InfoSpider()
    spider.collection_info()
'''
