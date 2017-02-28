# -*- coding: utf-8 -*-

__author__ = 'Nate_River'

import urllib
from threading import Thread, Lock
from urllib.request import ProxyHandler

lock = Lock()


def check_ips_task(ip_pool, start, end, filter_ip_pool):
    for ip in ip_pool[start:end]:
        proxy = {'http': ip}
        proxy_support = ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        i = 0
        while i < 3:
            try:
                resp = opener.open('http://iir.circ.gov.cn/', timeout=5)
                if resp.status == 200:
                    lock.acquire()
                    filter_ip_pool.append(ip)
                    print('Effective IP:', ip)
                    # print(resp.read().decode('gbk'))
                    lock.release()
            except Exception as e:
                i += 1
            else:
                break
        if i == 3: print('Failure IP:', ip)


def check_ips(ip_pool):
    filter_ip_pool = []
    pool = []  # 线程池
    size = len(ip_pool)
    step = size // 4 if size % 4 == 0 else size // 4 + 1
    for i in range(4):
        s, e = i * step, (i + 1) * step
        if e >= size: e = size
        t = Thread(target=check_ips_task, args=(ip_pool, s, e, filter_ip_pool))
        pool.append(t)
    for t in pool: t.start()
    for t in pool: t.join()
    return filter_ip_pool
