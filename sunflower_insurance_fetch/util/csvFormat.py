# -*- coding: utf-8 -*-

import os
import csv
import xlwt
from util.initDirs import load_cities_info


def total_info():
    cities_info = load_cities_info()
    total = 0
    for city in cities_info:
        src_city_dir = city[0]
        csv_file_name = os.path.join(src_city_dir, 'agent.csv')
        try:
            with open(csv_file_name, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                data = [row for row in reader]
                total += (len(data) - 1)
        except FileNotFoundError as e:
            pass
    print('Total records:', total)


def change_csv_format():
    cities_info = load_cities_info()
    for city in cities_info:
        src_city_dir = city[0]
        target_city_dir = city[0].replace('data', 'agent_data')

        csv_file_name = os.path.join(src_city_dir, 'agent.csv')
        xls_file_name = os.path.join(target_city_dir, 'agent.xls')
        print(csv_file_name)
        try:
            with open(csv_file_name, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                data = [row for row in reader]
                titles = data[0]

                # 将csv文件中的内容写入xls文件中
                workbook = xlwt.Workbook()
                sheet = workbook.add_sheet("代理人信息")
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
        except FileNotFoundError as e:
            pass


def change_csv_format2():
    tempDir = os.path.abspath('../')
    csv_file_name = os.path.join(tempDir, 'data', 'agent.csv')
    xls_file_name = os.path.join(tempDir, 'agent_data', 'agent.xls')
    with open(csv_file_name, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        data = [row for row in reader]
        titles = data[0]
        # 将csv文件中的内容写入xls文件中
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("代理人信息")
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
    total_info()
    # change_csv_format()
    # change_csv_format2()
