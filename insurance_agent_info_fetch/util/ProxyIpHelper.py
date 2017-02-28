# -*- coding: utf-8 -*-

__author__ = 'Nate_River'

import os
from util import IPLoader, IPChecker

file_path = os.path.abspath('.')
if not file_path.endswith('Insurance_Agent_Fetch'):
    file_path = os.path.join(file_path, 'Insurance_Agent_Fetch')
file_path = os.path.join(file_path, 'data', 'ips.txt')


def load_ip_pools(api_params, platform):
    IPLoader.load_ips(api_params, platform)
    ip_pool = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            ip_pool.append(line.strip())
    print('Loading Proxy IP Finished.')
    _ip_pool = IPChecker.check_ips(ip_pool) if platform != 'zhandaye_daili' else ip_pool
    print('Filter Proxy IP Finished')
    return _ip_pool


def daxiang_daili():
    """
    :param api_params:
        tid	是	订单号	123456768123121
        num	是	提取数量	1到50000任意数字
        operator	否	运营商	电信(1) / 联通(2) / 移动(3)
        area	否	地区	江苏 / 任意地区
        ports	否	端口号	1998,18186
        foreign	否	是否提取大陆以外IP	全部(all) / 仅非大陆(only) / 仅大陆(none)
        exclude_ports	否	排除端口号	8088,18186
        filter	否	过滤24小时内提取过的	默认不过滤，加上 on 参数就过滤
        protocol	否	支持的协议	默认为http和https, 可传入 https
        category	否	类别(匿名度)	默认为普匿 + 高匿, 可传入参数 普匿(0) / 高匿(2)
        delay	否	延迟，单位是秒 	判断条件为通过代理打开百度首页的时间。可传入任意数字，数字越小速度越快，传入 5 表示提取延迟5秒内的代理
        sortby	否	IP排序	默认最快优先， 传入 speed表示最快优先， time 表示最新优先
        format	否	返回格式	默认是文本，可以传入 xml json
        longlife	否	只提取稳定IP	转入数字，单位是分钟
    """
    ip_pool = load_ip_pools(api_params={
        'tid': '555358706930047',
        'num': 10,
        # 'ports': [80, 8080, 808],
        # 'filter': 'on',
        'delay': '1',
        'sortby': 'speed',
        'longlife': '20'
    }, platform='daxiang_daili')
    return ip_pool


def zhandaye_daili():
    """
    :param api_params:
        api	    API_ID
        count   提取数量
        fitter  是否过滤今天已提取过的IP（1：是   2：否）
        px      排序方式（1：按时间由近及远  2：随机抽取）
    """
    ip_pool = load_ip_pools(api_params={
        'api': '201702141117472321',
        'count': 10,
        'filter': '2',
        'px': '1'
    }, platform='zhandaye_daili')
    return ip_pool


def kuai_daili():
    """
    :param api_params:
        orderid 	订单号
        num 	    提取数量
        area        ip所在地区，支持按 国家/省/市 筛选
        b_pcff      返回的代理支持 火狐浏览器(Firefox)  取值固定为1
        protocol    按代理协议筛选 	1: HTTP, 2: HTTPS(同时也支持HTTP)
        method      按支持 GET/POST 筛选 	1: 支持HTTP GET, 2: 支持 HTTP POST(同时也支持GET)
        quality     代理ip的稳定性    0: 不筛选(默认)  1: VIP稳定  2: SVIP企业版非常稳定
        sort        返回的代理列表的排序方式 	0: 默认排序 1: VIP SVIP 企业版按响应速度(从快到慢)
        dedup 	    过滤今天提取过的IP 	取值固定为1
        sp1         返回的代理中只包含极速代理（响应速度<1秒）   取值固定为1
        sp2         返回的代理中只包含快速代理（响应速度1~3秒）   取值固定为1
        sp3         返回的代理中只包含慢速代理（响应速度>3秒）   取值固定为1
        sep 	    提取结果列表中每个结果的分隔符 	1: \r\n分隔(默认)
                                                    2: \n分隔
                                                    3: 空格分隔
                                                    4: |分隔
    """
    ip_pool = load_ip_pools(api_params={
        'orderid': '918723516570222',
        'num': 10,
        'area': ['中国'],
        'b_pcff': '1',
        'protocol': '1',
        'method': '2',
        'quality': '1',
        'sort': '1',
        # 'dedup': '1',
        'sp1': '1',  # 按需求和IP库存量来修改 sp(1, 2, 3)
        'sep': '1',
    }, platform='kuai_daili')
    return ip_pool


'''
if __name__ == '__main__':
    ip_pool = daxiang_daili()
    zhandaye_daili()
    filter_ip_pool(ip_pool)
'''
