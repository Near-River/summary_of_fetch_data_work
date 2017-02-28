# -*- coding: utf-8 -*-

"""
应用的主调用接口：
"""

__author__ = 'YangXiao'


def load_links_numbers(loops):
    try:
        from spider import linksSpiderTest
    except ImportError as e:
        print('Import Module spider failed.')
    else:
        # 加载一个城市下所有区的有效注册号个数，保存在路径文件 ../data/records.txt 下
        _linkSpiderTest = linksSpiderTest.LinksSpider()
        _linkSpiderTest.load_links_number(loops)


def load_all_links(threads_count):
    try:
        from spider import linksSpider
    except ImportError as e:
        print('Import Module spider failed.')
    else:
        # 根据每个区对应的有效注册号个数，抓取相应的企业链接信息
        linksSpider.multi_threads_running(threads_count)


def load_all_company_info(threads_count):
    try:
        from spider import CompanyInfoSpider
    except ImportError as e:
        print('Import Module spider failed.')
    else:
        # 根据每个区对应的有效注册号个数，抓取相应的企业链接信息
        CompanyInfoSpider.multi_threads_running(threads_count)


def convert_file_format(xlsFile, sheetName):
    try:
        from util import csv2xls
    except ImportError as e:
        print('Import Module util failed.')
    else:
        # 将 company.csv 文件转换为 xls 文件，保存到文件夹 real_data 下
        csv2xls.change_csv_format('company.csv', xlsFile, sheetName)


if __name__ == '__main__':
    # load_links_numbers(loops=20)
    load_all_links(threads_count=25)
    # load_all_company_info(threads_count=100)
    # convert_file_format(xlsFile='北京市企业信息.xls', sheetName='北京市企业信息')
