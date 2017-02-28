# -*- coding: utf-8 -*-

__author__ = 'Nate_River'

import requests
import os
from urllib.parse import quote


def load_ips(api_params, platform):
    """
    :param api_params:
        -- 大象代理：
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

        -- 站大爷代理：
        api	    API_ID
        count   提取数量
        fitter  是否过滤今天已提取过的IP（1：是   2：否）
        px      排序方式（1：按时间由近及远  2：随机抽取）

        -- 快代理：
        orderid 	订单号
        num 	    提取数量
        area        ip所在地区，支持按 国家/省/市 筛选
        b_pcff      返回的代理支持 火狐浏览器(Firefox)  取值固定为1
        protocol    按代理协议筛选 	1: HTTP, 2: HTTPS(同时也支持HTTP)
        method      按支持 GET/POST 筛选 	1: 支持HTTP GET, 2: 支持 HTTP POST(同时也支持GET)
        quality     代理ip的稳定性    0: 不筛选(默认)  1: VIP稳定  2: SVIP企业版非常稳定
        sort        返回的代理列表的排序方式 	0: 默认排序 1: VIPSVIP企业版按响应速度(从快到慢)
        dedup 	    过滤今天提取过的IP 	取值固定为1
        sp1         返回的代理中只包含极速代理（响应速度<1秒）   取值固定为1
        sp2         返回的代理中只包含快速代理（响应速度1~3秒）   取值固定为1
        sp3         返回的代理中只包含慢速代理（响应速度>3秒）   取值固定为1
        sep 	    提取结果列表中每个结果的分隔符 	1: \r\n分隔(默认)
                                                    2: \n分隔
                                                    3: 空格分隔
                                                    4: |分隔
    :param platform:
    :return:
    """
    api_url = ''
    if platform == 'daxiang_daili':
        api_url = 'http://tvp.daxiangdaili.com/ip/?'
        if 'tid' in api_params.keys():
            api_url += ('tid=' + api_params['tid'])
        if 'num' in api_params.keys():
            api_url += ('&num=' + str(api_params['num']))
        else:
            api_url += '&num=100'
        if 'operator' in api_params.keys():
            lst = list(map(str, api_params['operator']))
            operator = ','.join(lst)
            api_url += ('&operator=' + operator)
        if 'area' in api_params.keys():
            api_url += ('&area=' + api_params['area'])
        if 'ports' in api_params.keys():
            lst = list(map(str, api_params['ports']))
            ports = ','.join(lst)
            api_url += ('&ports=' + ports)
        if 'foreign' in api_params.keys():
            api_url += ('&foreign=' + api_params['foreign'])
        else:
            api_url += '&foreign=none'
        if 'exclude_ports' in api_params.keys():
            lst = list(map(str, api_params['exclude_ports']))
            exclude_ports = ','.join(lst)
            api_url += ('&exclude_ports=' + exclude_ports)
        if 'filter' in api_params.keys():
            api_url += ('&filter=' + api_params['filter'])
        if 'protocol' in api_params.keys():
            api_url += ('&protocol=' + api_params['protocol'])
        if 'category' in api_params.keys():  # 普匿(0) / 高匿(2)
            api_url += ('&category=' + api_params['category'])
        if 'delay' in api_params.keys():
            api_url += ('&delay=' + str(api_params['delay']))
        if 'sortby' in api_params.keys():  # time or speed
            api_url += ('&sortby=' + api_params['sortby'])
        if 'format' in api_params.keys():  # xml or json
            api_url += ('&format=' + api_params['format'])
        if 'longlife' in api_params.keys():
            api_url += ('&longlife=' + str(api_params['longlife']))
    elif platform == 'zhandaye_daili':
        api_url = 'http://vip.zdaye.com/?'
        if 'api' in api_params.keys():
            api_url += ('api=' + api_params['api'])
        if 'count' in api_params.keys():
            api_url += ('&count=' + str(api_params['count']))
        else:
            api_url += '&count=100'
        if 'fitter' in api_params.keys():
            api_url += ('&fitter=' + api_params['fitter'])
        if 'px' in api_params.keys():
            api_url += ('&px=' + api_params['px'])
    elif platform == 'kuai_daili':
        api_url = 'http://dev.kuaidaili.com/api/getproxy/?'
        if 'orderid' in api_params.keys():
            api_url += ('orderid=' + api_params['orderid'])
        if 'num' in api_params.keys():
            api_url += ('&num=' + str(api_params['num']))
        else:
            api_url += '&num=100'
        if 'area' in api_params.keys():
            area = ','.join(api_params['area'])
            api_url += ('&area=' + quote(area))
        if 'b_pcff' in api_params.keys():
            api_url += ('&b_pcff=' + api_params['b_pcff'])
        if 'protocol' in api_params.keys():
            api_url += ('&protocol=' + api_params['protocol'])
        if 'method' in api_params.keys():
            api_url += ('&method=' + api_params['method'])
        if 'quality' in api_params.keys():
            api_url += ('&quality=' + api_params['quality'])
        if 'sort' in api_params.keys():
            api_url += ('&sort=' + api_params['sort'])
        if 'dedup' in api_params.keys():
            api_url += ('&dedup=' + api_params['dedup'])
        if 'sp1' in api_params.keys():
            api_url += ('&sp1=' + api_params['sp1'])
        if 'sp2' in api_params.keys():
            api_url += ('&sp2=' + api_params['sp2'])
        if 'sp3' in api_params.keys():
            api_url += ('&sp3=' + api_params['sp3'])
        if 'sep' in api_params.keys():
            api_url += ('&sep=' + api_params['sep'])
    print('api_url:', api_url)
    ret = requests.get(api_url).text
    ips = ret.split()
    filepath = os.path.join(os.path.abspath('data'), 'ips.txt')
    with open(filepath, 'w') as f:
        for ip in ips: f.write(ip.strip() + '\n')
