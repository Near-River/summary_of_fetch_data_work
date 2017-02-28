# -*- coding: utf-8 -*-


__author__ = 'YangXiao'

import csv
import xlrd

file_path = '../data_temp/all_ids.xlsx'
file_path2 = '../data/real_links.csv'
file_path3 = '../data_temp/filter_all_ids.xlsx'


def load_all_filter_ids():
    global file_path3
    data = xlrd.open_workbook(file_path3)
    table = data.sheet_by_index(0)
    rows = table.nrows

    company_ids_lst = []
    for r in range(rows):
        val = str(table.cell(r, 0).value)
        company_ids_lst.append(val)
    return company_ids_lst


def load_all_ids():
    global file_path
    data = xlrd.open_workbook(file_path)
    table = data.sheet_by_index(0)
    rows, cols = table.nrows, table.ncols

    company_ids_lst = [[] for _ in range(cols)]
    for c in range(cols):
        for r in range(rows):
            val = str(table.cell(r, c).value)[:-2]
            company_ids_lst[c].append(val)
    # for i in range(cols): print(company_ids_lst[i][:3])
    print('Finished Load All Ids')
    return company_ids_lst


def load_company_info():
    with open(file_path2, 'r', newline='', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=',')
        company_info = [(row[0], row[1]) for row in reader]
    return company_info


if __name__ == '__main__':
    load_all_ids()
