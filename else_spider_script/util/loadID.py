# -*- coding: utf-8 -*-


__author__ = 'YangXiao'

import xlrd

file_path = '../data/tianjin_all_ids.xlsx'


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
    return company_ids_lst


if __name__ == '__main__':
    load_all_ids()
