# -*- coding: utf-8 -*-


__author__ = 'YangXiao'

import os
import csv
import xlrd

file_path = '甘肃'


def load_map():
    global file_path
    all_map = {}
    temp_dir = os.path.abspath(file_path)
    files_path = os.listdir(temp_dir)
    for file in files_path:
        _path = os.path.join(temp_dir, file)
        data = xlrd.open_workbook(_path)
        table = data.sheet_by_index(0)
        rows, cols = table.nrows, table.ncols
        print(file, '\tcols:', cols)
        for c in range(cols):
            for r in range(rows):
                val = str(table.cell(r, c).value)[:-2]
                key = val[:5] + '*****' + val[-2:]
                key2 = val[:5] + '*****' + val[-4:]
                all_map[key] = val
                all_map[key2] = val
    return all_map


def change_file(srcName, targetName):
    all_map = load_map()
    print('finished load map.')
    csv_file_name = srcName
    new_csv_file_name = targetName
    new_data = []
    with open(csv_file_name, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        data = [row for row in reader]
    print('loaded csv file.')
    new_data.append(data[0])
    changed_count = 0
    for i in range(1, len(data)):
        info = data[i]
        if info[1] in all_map:
            info[1] = all_map[info[1]]
            new_data.append(info)
            changed_count += 1
    print('changed count:', changed_count)
    with open(new_csv_file_name, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(new_data)


if __name__ == '__main__':
    # load_map()
    change_file('enterprise_info.csv', 'new_enterprise_info.csv')
