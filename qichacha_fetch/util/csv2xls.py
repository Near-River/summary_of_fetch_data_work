# -*- coding: utf-8 -*-

import os
import csv
import xlwt


def change_csv_format(srcName, targetName, sheetName):
    tempDir = os.path.abspath('../')
    csv_file_name = os.path.join(tempDir, 'data', srcName)
    xls_file_name = os.path.join(tempDir, 'real_data', targetName)
    with open(csv_file_name, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        data = [row for row in reader]
        titles = data[0]
        # 将csv文件中的内容写入xls文件中
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(sheetName)
        style = xlwt.easyxf('font: bold 1')
        for i in range(9): sheet.col(i).width = 256 * 20
        # 写入标题
        for i in range(len(titles)):
            sheet.write(0, i, titles[i], style)
        # 写入代理人信息
        for i in range(1, len(data)):
            _data = data[i]
            for j in range(len(_data)):
                sheet.write(i, j, _data[j])
        workbook.save(xls_file_name)


if __name__ == '__main__':
    # 装换 touzi.csv 文件
    # change_csv_format('touzi.csv', 'touzi.xls', '企查查对外投资信息')
    # change_csv_format('finance.csv', 'finance.xls', '企查查财务信息')
    # change_csv_format('report_basic_info.csv', 'report_basic_info.xls', '企查查年报信息_企业基本信息')
    # change_csv_format('report_chuzi_info.csv', 'report_chuzi_info.xls', '企查查年报信息_发起人及出资信息')
    # change_csv_format('report_touzi_info.csv', 'report_touzi_info.xls', '企查查年报信息_企业资产状况信息')
    pass