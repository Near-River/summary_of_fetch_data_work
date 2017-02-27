# -*- coding: utf-8 -*-

"""
采集每个企业的信息：
"""

__author__ = 'YangXiao'

import urllib.request
import http.cookiejar
import gzip
import re
import csv
import os
import time
from urllib.parse import urlencode
from util.loadList import load_company_info
from util.cookies import Cookies

Headers = {
    'Host': 'www.qichacha.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Connection': 'Keep-Alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'Referer': 'www.qichacha.com',
    'Cookie': Cookies[2]
}


class CompanyInfoSpider(object):
    def __init__(self):
        self.opener = None
        self.companies_info = load_company_info()

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

    def get_html(self, url, retries=3):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, timeout=10).read()  # 设置超时时间为10秒
            return self.ungzip(data)
        except urllib.request.URLError as e:
            if retries > 0: return self.get_html(retries - 1)
            print(url)
            return b''

    def savetities_to_csvfile(self, titles, filename):
        tempDir = os.path.abspath('../')
        file_name = os.path.join(tempDir, 'data', filename)
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(titles)

    def save_to_csvfile(self, info, filename):
        tempDir = os.path.abspath('../')
        file_name = os.path.join(tempDir, 'data', filename)
        with open(file_name, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(info)

    def load_touzi_info(self, url):
        html = self.get_html(url)
        html_doc = html.decode(encoding='utf-8', errors='ignore')
        # 匹配 是否为投资信息页面
        # <div class="touzi_info"></div>
        pattern1 = re.compile(
            r'<div class="touzi_info">(.*?)</div>',
            re.DOTALL
        )
        if len(pattern1.findall(html_doc)) == 0: return 'Cookie failure'
        # <ul class="list-group list-group-lg no-bg auto">
        pattern2 = re.compile(
            r'<ul class="list-group list-group-lg no-bg auto">(.*?)</ul>',
            re.DOTALL
        )
        if len(pattern2.findall(html_doc)) == 0: return []
        touzi_info = []
        # <a href="/firm_FJ_b35d715f277d8b327385b5cd9cadd36f" target="_blank"
        #    class="list-group-item clearfix">
        #     <span class="pull-left thumb-sm avatar m-r">
        #     <img src="http://co-image.qichacha.com/CompanyImage/default.jpg"> </span>
        #     <span class="clear">
        #         <span class="text-lg">福建电信科学技术研究院有限公司</span>
        #         <small class="text-gray clear text-ellipsis m-t-xs text-md">
        #             <label>法人：</label>
        #             赖克中
        #             <label>成立日期：</label> 2001-09-11
        #             <label>注册资本：</label> 1506.962 万元
        #         </small>
        #         <small class="text-gray clear text-ellipsis text-md"><label> 地址：</label>福州市六一南路241号</small>
        #     </span>
        # </a>
        pattern3 = re.compile(
            r'<a.*?>.*?<span class="text-lg">(.*?)</span>.*?</label>(.*?)<label>.*?</label>(.*?)<label>.*?</label>(.*?)</small>.*?</label>(.*?)</small>.*?</a>',
            re.DOTALL
        )
        result = pattern3.findall(html_doc)
        for elem in result:
            elem = list(map(lambda x: x.replace('\t', '').replace('\n', '').strip(), elem))
            touzi_info.append(elem)
        return touzi_info

    def collection_touzi_info(self):
        """ 收集企查查所有相关企业的对外投资信息 """
        self.opener = self.get_opener(Headers)
        start = 0
        count = 1
        size = len(self.companies_info)
        end = size
        titles = ['公司名称', '对外投资公司名称', '法人', '成立日期', '注册资本', '地址']  # 标题信息
        if start == 0: self.savetities_to_csvfile(titles=titles, filename='touzi.csv')
        touzi_info = []
        for i in range(start, end):
            company_info = self.companies_info[i]
            # http://www.qichacha.com/company_getinfos?unique=03395a15d0472c0561f14c44e7029b26&companyname=中邮科通信技术股份有限公司&tab=touzi
            company_name, link = company_info[0], company_info[1]
            unique = link[link.find('_') + 1:link.rfind('.')]
            d = {
                'unique': unique,
                'companyname': company_name,
                'tab': 'touzi'
            }
            url = 'http://www.qichacha.com/company_getinfos?' + urlencode(d)
            result = self.load_touzi_info(url)
            # 处理各种情况：一：cookie失效     二：没有对外投资信息      三：正常获取信息
            if result == 'Cookie failure':
                print('Cookie failure at: %d, Url: %s' % (i, url))
                break
            elif result:
                for elem in result:
                    elem.insert(0, company_name)
                    touzi_info.append(elem)
            if count % 5 == 0:
                time.sleep(3)
                print('Current position at:', i)
            count += 1
        self.save_to_csvfile(info=touzi_info, filename='touzi.csv')

    def load_finance_info(self, url):
        html = self.get_html(url)
        html_doc = html.decode(encoding='utf-8', errors='ignore')
        # 匹配 是否为财务信息页面
        # <div class="finance_info"></div>
        pattern1 = re.compile(
            r'<div class="finance_info">(.*?)</div>',
            re.DOTALL
        )
        if len(pattern1.findall(html_doc)) == 0: return 'Cookie failure'
        # <div class="noresult">...</div>
        pattern2 = re.compile(
            r'<div class="noresult">(.*?)</div>',
            re.DOTALL
        )
        if len(pattern2.findall(html_doc)) > 0: return []
        finance_info = []
        # <small class="clear text-ellipsis m-t-xs text-md">
        #     <label class="m-l-md">公司实力等级：</label>2000万-1亿<br>
        #     <label class="m-l-md">纳税区间：</label>10万-100万<br>
        #     <label class="m-l-md">销售净利润率：</label>0到10%<br>
        #     <label class="m-l-md">销售毛利率：</label>10%到50%
        # </small>
        pattern3 = re.compile(
            r'<small class="clear text-ellipsis m-t-xs text-md">.*?</label>(.*?)<br>.*?</label>(.*?)<br>.*?</label>(.*?)<br>.*?</label>(.*?)</small>',
            re.DOTALL
        )
        result = pattern3.findall(html_doc)
        for elem in result:
            elem = list(map(lambda x: x.replace('\t', '').replace('\n', '').strip(), elem))
            finance_info.append(elem)
        return finance_info

    def collection_finance_info(self):
        """ 收集企查查所有相关企业的财务信息 """
        self.opener = self.get_opener(Headers)
        start = 0
        count = 1
        size = len(self.companies_info)
        end = size
        titles = ['公司名称', '公司实力等级', '纳税区间', '销售净利润率', '销售毛利率']  # 标题信息
        if start == 0: self.savetities_to_csvfile(titles=titles, filename='finance.csv')
        finance_info = []
        for i in range(start, end):
            company_info = self.companies_info[i]
            # http://www.qichacha.com/company_getinfos?unique=03395a15d0472c0561f14c44e7029b26&companyname=中邮科通信技术股份有限公司&tab=finance
            company_name, link = company_info[0], company_info[1]
            unique = link[link.find('_') + 1:link.rfind('.')]
            d = {
                'unique': unique,
                'companyname': company_name,
                'tab': 'finance'
            }
            url = 'http://www.qichacha.com/company_getinfos?' + urlencode(d)
            result = self.load_finance_info(url)
            # 处理各种情况：一：cookie失效     二：没有对外投资信息      三：正常获取信息
            if result == 'Cookie failure':
                print('Cookie failure at: %d, Url: %s' % (i, url))
                break
            elif result:
                for elem in result:
                    elem.insert(0, company_name)
                    finance_info.append(elem)
            if count % 5 == 0:
                time.sleep(3)
                print('Current position at:', i)
            count += 1
        self.save_to_csvfile(info=finance_info, filename='finance.csv')

    def load_report_info(self, url):
        html = self.get_html(url)
        html_doc = html.decode(encoding='utf-8', errors='ignore')
        # 匹配 是否为年报信息页面
        # <div class="report_info"></div>
        pattern1 = re.compile(
            r'<div class="report_info">(.*?)</div>',
            re.DOTALL
        )
        if len(pattern1.findall(html_doc)) == 0: return 'Cookie failure'
        # <div class="noresult  no-search" id="noReport">...</div>
        pattern2 = re.compile(
            r'<div class="noresult  no-search" id="noReport">(.*?)</div>',
            re.DOTALL
        )
        if len(pattern2.findall(html_doc)) > 0: return None

        report_info = {}
        # <div class="tab-pane fade in active" id="2015年度报告"
        pattern3 = re.compile(
            r'<div class="tab-pane fade in.*?" id="(.*?)".*?>(.*?)</div>',
            re.DOTALL
        )
        result = pattern3.findall(html_doc)
        try:
            for res in result:
                """
                2 发起人及出资信息：
                    发起人、认缴出资额（万元）、认缴出资时间
                    认缴出资方式、实缴出资额（万元）、
                    出资时间、出资方式

                3 企业资产状况信息：
                    资产总额、所有者权益合计、营业总收入、
                    利润总额、营业总收入中主营业务收入、
                    净利润、纳税总额、负债总额

                4 对外投资信息：
                    投资设立企业或购买股权企业名称、注册号
                """
                year, text = res[0], res[1]
                # <table class="table table-bordered" style="margin-top:15px;
                pattern4 = re.compile(r'<table class="table table-bordered".*?>(.*?)</table>', re.DOTALL)
                kinds = pattern4.findall(text)
                # print(year, len(kinds))
                report_info[year] = {}
                for kind in kinds:
                    pattern5 = re.compile(r'<td.*?>(.*?)</td>.*?</tr>(.*?)</tbody>', re.DOTALL)
                    _result = pattern5.findall(kind)
                    if len(_result) > 0:
                        name = _result[0][0].strip()
                        if name == '企业基本信息':
                            # 1 企业基本信息：
                            #     注册号、企业经营状态、企业联系电话、电子邮箱、邮政编码、从业人数、住所、
                            #     有限责任公司本年度是否发生股东股权转让、企业是否有投资信息或购买其他公司股权

                            # <tr>
                            #     <td class="left-title" width="20%">注册号</td>
                            #     <td width="30%">330100400013364</td>
                            #     <td class="left-title" width="20%">企业经营状态</td>
                            #     <td width="30%">开业</td>
                            # </tr>
                            # <tr>
                            #     <td class="left-title" width="20%">企业联系电话</td>
                            #     <td width="25%">0571-85022088</td>
                            #     <td class="left-title" width="20%">电子邮箱</td>
                            #     <td><a href="mailto:tangxian.gongtx@alibaba-inc.com" style="color:#555;">tangxian.gongtx@alibaba-inc.com</a></td>
                            # </tr>
                            # <tr>
                            #     <td class="left-title" width="20%">邮政编码</td>
                            #     <td width="25%">310000</td>
                            #     <td class="left-title" width="20%">从业人数</td>
                            #     <td width="25%">企业选择不公示</td>
                            # </tr>
                            # <tr>
                            #     <td class="left-title" width="20%">住所</td>
                            #     <td colspan="3">杭州市西湖区西斗门路3号天堂软件园A幢10楼G座</td>
                            # </tr>
                            # <tr>
                            #     <td class="left-title" width="20%">有限责任公司本年度是否发生股东股权转让</td>
                            #     <td>否</td>
                            #     <td class="left-title" width="20%">企业是否有投资信息或购买其他公司股权</td>
                            #     <td colspan="3">有</td>
                            # </tr>
                            _pattern = re.compile(
                                r'<tr>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>.*?</tr>',
                                re.DOTALL
                            )
                            _pattern2 = re.compile(
                                r'<tr>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?<a href="mailto:(.*?)".*?</td>.*?</tr>',
                                re.DOTALL
                            )
                            _pattern3 = re.compile(
                                r'<tr>.*?<td class="left-title" width="20%">.*?</td>.*?<td colspan="3">(.*?)</td>.*?</tr>',
                                re.DOTALL
                            )
                            _res = _pattern.findall(_result[0][1])
                            _res2 = _pattern2.findall(_result[0][1])
                            _res3 = _pattern3.findall(_result[0][1])
                            report_info[year]['basic_info'] = [
                                _res[0][0], _res[0][1], _res[1][0], _res2[0], _res[2][0], _res[2][1],
                                _res3[0], _res[3][0], _res[3][1]
                            ]
                        elif name == '发起人及出资信息':
                            # 2 发起人及出资信息：
                            #     发起人、认缴出资额（万元）、认缴出资时间、认缴出资方式、实缴出资额（万元）、出资时间、出资方式

                            # <tr>
                            #     <td class="left-title">发起人</td>
                            #     <td class="left-title">认缴出资额（万元）</td>
                            #     <td class="left-title">认缴出资时间</td>
                            #     <td class="left-title">认缴出资方式</td>
                            #     <td class="left-title">实缴出资额（万元）</td>
                            #     <td class="left-title">出资时间</td>
                            #     <td class="left-title">出资方式</td>
                            # </tr>
                            # <tr>
                            #     <td>Alibaba Group Services Limited</td>
                            #     <td>101880.0906</td>
                            #     <td>2012年12月22日</td>
                            #     <td>货币</td>
                            #     <td>101880.0906</td>
                            #     <td>2010年12月21日</td>
                            #     <td>货币</td>
                            # </tr>

                            _pattern = re.compile(
                                r'<tr>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?</tr>',
                                re.DOTALL
                            )
                            _res = _pattern.findall(_result[0][1])[1]
                            report_info[year]['chuzi_info'] = list(_res)
                        elif name == '企业资产状况信息':
                            # 3 企业资产状况信息：
                            #     资产总额、所有者权益合计、营业总收入、利润总额、营业总收入中主营业务收入、
                            #     净利润、纳税总额、负债总额

                            # <tr>
                            #     <td class="left-title" width="20%">资产总额</td>
                            #     <td>企业选择不公示</td>
                            #     <td class="left-title" width="20%">所有者权益合计</td>
                            #     <td>企业选择不公示</td>
                            # </tr>
                            # <tr>
                            #     <td class="left-title">营业总收入</td>
                            #     <td>企业选择不公示</td>
                            #     <td class="left-title">利润总额</td>
                            #     <td>企业选择不公示</td>
                            # </tr>
                            # <tr>
                            #     <td class="left-title">营业总收入中主营业务收入</td>
                            #     <td>企业选择不公示</td>
                            #     <td class="left-title">净利润</td>
                            #     <td>企业选择不公示</td>
                            # </tr>
                            # <tr>
                            #     <td class="left-title">纳税总额</td>
                            #     <td>企业选择不公示</td>
                            #     <td class="left-title">负债总额</td>
                            #     <td>企业选择不公示</td>
                            # </tr>

                            _pattern = re.compile(
                                r'<tr>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>.*?</tr>',
                                re.DOTALL
                            )
                            _res = _pattern.findall(_result[0][1])
                            report_info[year]['zichan_info'] = [
                                _res[0][0], _res[0][1], _res[1][0], _res[1][1], _res[2][0], _res[2][1],
                                _res[3][0], _res[3][1]
                            ]
                        elif name == '对外投资信息':
                            # 4 对外投资信息：
                            #     投资设立企业或购买股权企业名称、注册号

                            # <tr>
                            #     <td class="left-title" width="50%">投资设立企业或购买股权企业名称</td>
                            #     <td class="left-title">注册号</td>
                            # </tr>
                            # <tr>
                            #     <td>浙江淘宝大学有限公司</td>
                            #     <td>330000000074309</td>
                            # </tr>
                            # <tr>
                            #     <td>浙江太极禅文化发展有限公司</td>
                            #     <td>330184000165855</td>
                            # </tr>
                            # <tr>
                            #     <td>上海星浩股权投資中心(有限合伙)</td>
                            #     <td>310000000101279</td>
                            # </tr>

                            _pattern = re.compile(
                                r'<tr>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?</tr>',
                                re.DOTALL
                            )
                            _res = _pattern.findall(_result[0][1])
                            lst = []
                            for l in _res[1:]: lst.append(list(l))
                            report_info[year]['touzi_info'] = lst
        except Exception as e:
            print('Parse Error:', url)
            return 'parse error'

        return report_info

    def collection_report_info(self):
        """ 收集企查查所有相关企业的年报信息 """
        self.opener = self.get_opener(Headers)
        start = 0
        count = 1
        size = len(self.companies_info)
        end = size
        """
        1 企业基本信息：
            注册号、企业经营状态、企业联系电话、
            电子邮箱、邮政编码、从业人数、住所、
            有限责任公司本年度是否发生股东股权转让、
            企业是否有投资信息或购买其他公司股权

        2 发起人及出资信息：
            发起人、认缴出资额（万元）、认缴出资时间
            认缴出资方式、实缴出资额（万元）、
            出资时间、出资方式

        3 企业资产状况信息：
            资产总额、所有者权益合计、营业总收入、
            利润总额、营业总收入中主营业务收入、
            净利润、纳税总额、负债总额

        4 对外投资信息：
            投资设立企业或购买股权企业名称、注册号
        """
        titles = [
            ['公司名称', '年份', '注册号', '企业经营状态', '企业联系电话', '电子邮箱', '邮政编码', '从业人数', '住所', '有限责任公司本年度是否发生股东股权转让',
             '企业是否有投资信息或购买其他公司股权'],
            ['公司名称', '年份', '发起人', '认缴出资额（万元）', '认缴出资时间', '认缴出资方式', '实缴出资额（万元）', '出资时间', '出资方式'],
            ['公司名称', '年份', '资产总额', '所有者权益合计', '营业总收入', '利润总额', '营业总收入中主营业务收入', '净利润', '纳税总额', '负债总额'],
            ['公司名称', '年份', '投资设立企业或购买股权企业名称', '注册号']
        ]
        if start == 0:
            self.savetities_to_csvfile(titles=titles[0], filename='report_basic_info.csv')
            self.savetities_to_csvfile(titles=titles[1], filename='report_chuzi_info.csv')
            self.savetities_to_csvfile(titles=titles[2], filename='report_zichan_info.csv')
            self.savetities_to_csvfile(titles=titles[3], filename='report_touzi_info.csv')

        report_basic_info = []
        report_chuzi_info = []
        report_zichan_info = []
        report_touzi_info = []
        for i in range(start, end):
            company_info = self.companies_info[i]
            # http://www.qichacha.com/company_getinfos?unique=03395a15d0472c0561f14c44e7029b26&companyname=中邮科通信技术股份有限公司&tab=report
            company_name, link = company_info[0], company_info[1]
            unique = link[link.find('_') + 1:link.rfind('.')]
            d = {
                'unique': unique,
                'companyname': company_name,
                'tab': 'report'
            }
            url = 'http://www.qichacha.com/company_getinfos?' + urlencode(d)
            result = self.load_report_info(url)
            # 处理各种情况：一：cookie失效     二：没有对外投资信息      三：正常获取信息
            if result == 'Cookie failure':
                print('Cookie failure at: %d, Url: %s' % (i, url))
                break
            elif result == 'parse error':
                print('Parse error at: %d, Url: %s' % (i, url))
                break
            elif result:
                # report_info[year]['touzi_info'] = _res[1:]
                for key in result:
                    for info in result[key]:
                        if info != 'touzi_info':
                            lst = result[key][info]
                            lst.insert(0, key)
                            lst.insert(0, company_name)
                        if info == 'basic_info':
                            report_basic_info.append(lst)
                        elif info == 'chuzi_info':
                            report_chuzi_info.append(lst)
                        elif info == 'zichan_info':
                            report_zichan_info.append(lst)
                        elif info == 'touzi_info':
                            lst = result[key][info]
                            for l in lst:
                                l.insert(0, key)
                                l.insert(0, company_name)
                                report_touzi_info.append(l)
            if count % 5 == 0:
                time.sleep(3)
                print('Current position at:', i)
            count += 1

        self.save_to_csvfile(info=report_basic_info, filename='report_basic_info.csv')
        self.save_to_csvfile(info=report_chuzi_info, filename='report_chuzi_info.csv')
        self.save_to_csvfile(info=report_zichan_info, filename='report_zichan_info.csv')
        self.save_to_csvfile(info=report_touzi_info, filename='report_touzi_info.csv')


if __name__ == '__main__':
    spider = CompanyInfoSpider()
    # spider.collection_touzi_info()
    # spider.collection_finance_info()
    # spider.collection_report_info()
