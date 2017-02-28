# -*- coding: utf-8 -*-

"""
导游信息采集：
"""

__author__ = 'Nate_River'

import requests
from bs4 import BeautifulSoup
import csv
import os
from PIL import Image
import subprocess
import threading

Headers = {
    'Host': 'daoyou-chaxun.cnta.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
    'Connection': 'Keep-Alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

lock = threading.Lock()


class InfoSpider(object):
    def save_to_csvfile(self, data):
        with open('info.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data)

    def identify_vcode(self):
        # 转换图片格式
        imgDir = os.path.join(os.path.abspath('img'), 'vcode.bmp')
        image = Image.open(imgDir)
        image.save('img/vcode.jpg', format='jpeg')
        filePath = os.path.join(os.path.abspath('img'), 'vcode.jpg')
        subprocess.call(['tesseract', filePath, 'output', '-l', 'eng', '-psm', '7', 'nobatch'])
        with open('output.txt', encoding='utf-8') as f:
            return f.read().strip()

    def collection_info(self, start, end):
        session = requests.session()
        session.headers.update(Headers)

        while True:
            # 获取验证码图片
            vcode_url = 'http://daoyou-chaxun.cnta.gov.cn/single_info/validatecode.asp'
            img_stream = session.get(vcode_url).content
            with open('img/vcode.bmp', 'bw') as f:
                f.write(bytes(img_stream))

            # 识别验证码
            vcode = self.identify_vcode()
            print('vcode:', vcode)

            search_url = 'http://daoyou-chaxun.cnta.gov.cn/single_info/selectlogin_1.asp'
            postData = {
                'text_dyzh': 'D-4101-017259',
                'text_dykh': '',
                'text_dysfzh': '',
                'vcode': vcode,
            }
            html = session.post(url=search_url, data=postData)
            html.encoding = 'gb2312'
            if '验证码输入错误' in html.text:
                print('验证码识别错误')
                continue
            else:
                print(html.text)
            exit()


if __name__ == '__main__':
    spider = InfoSpider()
    spider.collection_info(start=0, end=1)
