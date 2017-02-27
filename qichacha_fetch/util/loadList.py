# -*- coding: utf-8 -*-

"""
加载诚信商圈试点商户名单信息
"""

__author__ = 'YangXiao'

import xlrd
import csv

# file_path = '../data/qichacha.xlsx'
file_path = '../data/qichacha_names.txt'
file_path2 = '../data/links.csv'


def load_names(size=0):
    business_names_lst = []
    with open(file_path, encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            business_names_lst.append(line.replace('\n', ''))
    return business_names_lst


def load_list(size=0):
    business_names_lst = []
    data = xlrd.open_workbook(file_path)
    table = data.sheet_by_index(0)
    # rows = table.nrows

    for i in range(1, size):
        business_names_lst.append((i, table.cell(i, 1).value))
        # print(table.cell(i, 1).value)
    return business_names_lst


def load_company_info():
    with open(file_path2, 'r', newline='', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=',')
        company_info = [(row[1], row[2]) for row in reader]
    return company_info


if __name__ == '__main__':
    load_names()
    # lst = load_list()

    # lst = load_company_info()
    # for l in lst: print(l)
