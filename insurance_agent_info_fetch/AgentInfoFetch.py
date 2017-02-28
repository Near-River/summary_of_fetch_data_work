# -*- coding: utf-8 -*-

__auther__ = 'Nate_River'

"""
保险代理人数据采集脚本 V4.0: 使用代理IP进行防止IP封锁机制，全自动化机制
版本一：
    —— 功能说明：
        在ip_pool.txt文件中配置代理ip信息
        若配置文件ip_pool.txt中的代理ip均失效，程序会自动从提取有效代理IP
"""

import sys, os

sys.path.append(os.path.abspath('.'))
import time, threading, csv
import requests
from bs4 import BeautifulSoup
from util import ProxyIpHelper

ProxyAgents = 'kuai_daili'  # daxiang_daili       kuai_daili     zhandaye_daili
lock = threading.Lock()
URL = "http://iir.circ.gov.cn/web/baoxyx!searchInfoBaoxyx.html"
Headers = {
    'Host': "iir.circ.gov.cn",
    'User - Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept - Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept - Encoding': "gzip, deflate",
    'Referer': "http://www.circ.gov.cn/",
    'Connection': "keep-alive",
    'Cache - Control': "max-age=0"
}
IP_Pool = []  # 全局IP池
Retrial_Count = 0


def load_ip_pool():
    global IP_Pool
    IP_Pool.clear()
    print('Preparing For Load Proxy IP...')
    if ProxyAgents == 'daxiang_daili':
        IP_Pool = ProxyIpHelper.daxiang_daili()
    elif ProxyAgents == 'kuai_daili':
        IP_Pool = ProxyIpHelper.kuai_daili()
    elif ProxyAgents ==  'zhandaye_daili':
        IP_Pool = ProxyIpHelper.zhandaye_daili()


while len(IP_Pool) == 0: load_ip_pool()


class Fetch(object):
    def __init__(self):
        self.session = requests.session()
        self.session.proxies.update({
            'http': IP_Pool[0]
        })

    def writeData(self, data, file='agent_info.csv'):
        with open(file, 'a', encoding='utf-8', errors='ignore')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(data)

    def getData(self, id):
        global URL, Headers
        data = {
            'id_card': id,
            'certificate_code': "",
            'evelop_code': "",
            'name': "",
            'valCode': ""
        }
        html = self.session.post(url=URL, headers=Headers, data=data, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.body
        temp_table = body.find('table').next_sibling.next_sibling
        trs = temp_table.find('table').find_all('tr')
        data = []
        for i in trs:
            try:
                data.append(i.find('td').string + '\t')
            except:
                data.append('')
        return data

    def run(self, IDCard_numbers, start, end):
        global Del_Flag, Retrial_Count
        i = start
        while i < end:
            try:
                id_num = IDCard_numbers[i]
                data = self.getData(id_num)
                print(id_num, data)
                if data[1] != '序号\t':
                    lock.acquire()
                    data.insert(0, id_num + '\t')
                    self.writeData(data, file='agent_info.csv')
                    lock.release()
                i += 1
            except Exception as e:
                Retrial_Count += 1
                if Retrial_Count >= 300:
                    lock.acquire()
                    del IP_Pool[0]
                    print('The number of IP_Pool:', len(IP_Pool))
                    while len(IP_Pool) == 0:
                        load_ip_pool()
                        time.sleep(8)
                    self.session.proxies.update({
                        'http': IP_Pool[0]
                    })
                    Retrial_Count = 0
                    lock.release()
                else:
                    continue


def main(file_paths, threads_count, packStart=0, packEnd=-1):
    if packEnd == -1: packEnd = len(file_paths)
    packageCount = 0
    t_begin = time.time()
    for i in range(packStart, packEnd):
        filePath = file_paths[i]
        packageCount += 1
        t1 = time.time()
        # 开启多线程采集
        threads_pool = []
        IDCard_numbers = []
        print(filePath)
        with open(filePath, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                id = row[0].split('\t')[1]
                IDCard_numbers.append(id)
        idNums = len(IDCard_numbers)
        begin = 0
        step = idNums // threads_count if idNums % threads_count == 0 else idNums // threads_count + 1
        fetch = Fetch()
        for i in range(threads_count):
            start = begin + i * step
            end = start + step
            if end > idNums: end = idNums
            # print(start, end)
            t = threading.Thread(target=fetch.run, args=(IDCard_numbers, start, end))
            threads_pool.append(t)
        for t in threads_pool:
            t.start()
            time.sleep(1)
        for t in threads_pool:
            t.join()

        t2 = time.time()
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write('Finished Package %s.\n' % filePath)
        print('Finished Package %d within %f seconds.' % (packageCount, t2 - t1))

    t_end = time.time()
    print('Finished all tasks within %f seconds.' % (t_end - t_begin))


if __name__ == '__main__':
    tempDir = os.path.abspath('.')
    path = os.path.join(tempDir, 'NewIDCard', 'test')
    packageLst = os.listdir(path)
    print('package count:', len(packageLst))

    # 加载所有csv文件的路径
    file_paths = []
    for pack in packageLst:
        temp_path = os.path.join(path, pack)
        pack_name = os.path.join(temp_path, (os.listdir(temp_path))[0])
        file_paths.append(pack_name)

    main(file_paths, threads_count=10, packStart=0)
