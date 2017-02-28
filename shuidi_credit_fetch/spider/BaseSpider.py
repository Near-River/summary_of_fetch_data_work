# -*- coding: utf-8 -*-


__author__ = 'YangXiao'

import urllib.request
import http.cookiejar
import gzip
from urllib.request import ProxyHandler
import random, time


class BaseSpider(object):
    def __init__(self):
        self.opener = None

    def set_opener(self, headers, proxy):
        proxy = {'http': proxy}
        proxy_support = ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        header_lst = []
        for key, value in headers.items():
            elem = (key, value)
            header_lst.append(elem)
        opener.addheaders = header_lst
        return opener

    def get_opener(self, headers):
        cj = http.cookiejar.CookieJar()
        processor = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(processor)
        # with open('../data/valid_proxy_ips.txt', 'r') as f:
        #     random.seed(time.time())
        #     lines = f.readlines()
        #     size = len(lines)
        #     rand = random.randint(0, size - 1)
        #     ip = lines[rand].strip()
        # proxy = {'http': ip}
        # print('Use Ip:', ip)
        # proxy_support = ProxyHandler(proxy)
        # opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        header_lst = []
        for key, value in headers.items():
            elem = (key, value)
            header_lst.append(elem)
        opener.addheaders = header_lst
        return opener

    def change_opener(self, headers):
        self.opener = self.get_opener(headers)

    def ungzip(self, data):
        try:
            data = gzip.decompress(data)
        except Exception as e:
            pass
        return data

    def get_html(self, url, retries=3):  # 失败后的重连机制
        try:
            data = self.opener.open(fullurl=url, timeout=10).read()  # 设置超时时间为10秒
            return self.ungzip(data)
        except (urllib.request.URLError, urllib.request.HTTPError) as e:
            if retries > 0: return self.get_html(retries - 1)
            return b''
