# -*- coding: utf-8 -*-

import xlrd
import xlsxwriter
import time


def filter_ids(linksNumberRecord, areaNo):
    if len(linksNumberRecord) > 0:
        from util.loadID import load_all_ids
        all_ids = load_all_ids()
        col_all_ids = all_ids[areaNo]
        print('load all_ids finished.')
        xlsx_file_path = '../data_temp/filter_all_ids.xlsx'
        workbook = xlsxwriter.Workbook(xlsx_file_path)
        worksheet = workbook.add_worksheet(name='sheet1')
        r_count = 0
        for _no in linksNumberRecord:
            begin = _no * 5000
            end = begin + 5000
            for r in range(begin, end):
                worksheet.write(r_count, 0, col_all_ids[r])
                r_count += 1
        workbook.close()


def change(srcName, targetName, sheetName):
    data = xlrd.open_workbook(srcName)
    table = data.sheet_by_index(0)
    rows, cols = table.nrows, table.ncols

    xlsx_file_name = targetName
    workbook = xlsxwriter.Workbook(xlsx_file_name)
    worksheet = workbook.add_worksheet(name=sheetName)
    for i in range(21):
        c = chr(65 + i)
        worksheet.set_column(c + ':' + c, width=20)
    print('Finished open the file:', srcName)
    for c in range(cols):
        print('enter', c)
        t1 = time.time()
        for r in range(500000, rows):
            worksheet.write(r - 500000, c, table.cell(r, c).value)
        t2 = time.time()
        print(c, 'cost', t2 - t1)
    workbook.close()


if __name__ == '__main__':
    change('raw_all_ids.xlsx', 'all_ids.xlsx', 'sheet_1')
