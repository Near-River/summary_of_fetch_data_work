# -*- coding: utf-8 -*-

"""
成都信用网：企业工商信息采集
"""

__author__ = 'Nate_River'

import urllib.request
import http.cookiejar
import os.path
import time
import json
from urllib.parse import urlencode
from model.BuildModel import ModelFactory

Headers = {
    'Host': 'www.cdcredit.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Connection': 'Keep-Alive',
    'Referer': 'http://www.cdcredit.gov.cn/www/index.html'
}


class LinkSpider(object):
    def __init__(self):
        self.opener = self.get_opener(Headers)

    def get_opener(self, headers):
        cj = http.cookiejar.CookieJar()
        processor = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(processor)
        header_lst = []
        for key, value in headers.items(): header_lst.append((key, value))
        opener.addheaders = header_lst
        return opener

    def get_html(self, url, data=None, retries=3):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, data=data, timeout=10).read()  # 设置超时时间为10秒
            return data
        except urllib.request.URLError as e:
            if retries > 0: return self.get_html(retries - 1)
            return b''

    def crack_verification_code(self, model, trials):
        # 加载验证码
        file_name = 'verifCodePic' + str(trials) + '.jpg'
        file_path = os.path.join(os.path.abspath('../'), 'temp', file_name)
        # 破解验证码
        answer, trial_count = 0, 0
        while True:
            trial_count += 1
            request_url = 'http://www.cdcredit.gov.cn/verifCodeServlet?_=' + str(int(time.time() * 1000))
            while True:
                try:
                    # 下载验证码图片，并保存图片
                    urllib.request.urlretrieve(url=request_url, filename=file_path)
                    break
                except Exception as e:
                    continue
            # 识别验证码图片
            num1, operator, num2 = model.identify_verifCodePic(img_path=file_path)
            if operator == 'identify_operator_failed' or num1 == 'identify_num_failed' or num2 == 'identify_num_failed':
                continue
            elif num1 == 'unknown' or num2 == 'unknown':
                continue
            else:
                a, b = int(num1), int(num2)
                if operator == 'plus':
                    # print('%d %s %d' % (a, '＋', b))
                    answer = a + b
                elif operator == 'minus':
                    # print('%d %s %d' % (a, '－', b))
                    answer = a - b
                elif operator == 'multi':
                    # print('%d %s %d' % (a, '×', b))
                    answer = a * b
                # print('Trial Count:', trial_count)
                break
        return answer

    def collection_links(self):
        Headers = {
            'Host': 'www.cdcredit.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip,deflate',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Connection': 'Keep-Alive',
            'Content-Length': '22',
            'Referer': 'http://www.cdcredit.gov.cn/www/index.html'
        }
        self.opener = self.get_opener(Headers)
        postData = {
            'text': '成都铁路局',
            'unit': '0',
            'unitType': '0',
            'page': '1',
            'pageSize': '10',
            'appType': 'APP001'
        }
        search_url = 'http://www.cdcredit.gov.cn/search/getSearchList.do'
        html_txt = self.get_html(url=search_url, data=urlencode(postData).encode()).decode()
        ret = json.loads(html_txt)
        arr = ret['rows']
        for elem in arr:
            print(elem)
        return

        model = ModelFactory()  # 构建模式识别器对象
        trials = 0
        while True:
            trials += 1
            # 获取验证码答案
            answer = self.crack_verification_code(model=model, trials=trials)
            check_url = 'http://www.cdcredit.gov.cn/search/getIndexVerifyCode.do'
            # 定义一个要提交的数据数组(字典)
            postData = {
                'code': str(answer),
                'appType': 'APP001'
            }
            html_txt = self.get_html(url=check_url, data=urlencode(postData).encode()).decode()
            ret = json.loads(html_txt)
            print(ret, answer)
            if ret['isCheck'] == 1 and ret['code'] == 200: break


if __name__ == '__main__':
    spider = LinkSpider()
    spider.collection_links()

    # 验证结果是否正确(json)
    # http://www.cdcredit.gov.cn/search/getIndexVerifyCode.do
    # 获取查询信息(json)
    # http://www.cdcredit.gov.cn/search/getSearchList.do
