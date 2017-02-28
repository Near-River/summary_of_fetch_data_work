# -*- coding: utf-8 -*-

"""
下载1000张验证码图片做模型学习
"""

__author__ = 'Nate_River'

import urllib.request
import os
import time


class DownloadSpider(object):
    def collection_data(self, pic_nums):
        i = 0
        while i < pic_nums:
            try:
                request_url = 'http://www.cdcredit.gov.cn/verifCodeServlet?_=' + str(int(time.time() * 1000))
                file_name = 'verifCodePic' + str(i + 1) + '.jpg'
                file_path = os.path.join(os.path.abspath('../'), 'imgs', file_name)
                urllib.request.urlretrieve(url=request_url, filename=file_path)
                i += 1
                print('Finished:', i)
            except Exception:
                print('Error happened.')
                break


if __name__ == '__main__':
    spider = DownloadSpider()
    # spider.collection_data(pic_nums=1000)
