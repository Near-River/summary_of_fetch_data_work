# -*- coding: utf-8 -*-

import csv
import os


def load_cities_info():
    with open('../data/links.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i = 0
        tempDir = os.path.abspath('../')
        cities_info = []
        for row in reader:
            if i != 0:
                province_name, city_name, url = str(row[0]), str(row[1]), str(row[2])
                city_dir = os.path.join(tempDir, 'data', province_name, city_name)
                cities_info.append((city_dir, url))
            i = 1
    return cities_info


def init_dirs():
    """
    初始化目录结构
    :return:
    """
    with open('../data/links.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i = 0
        tempDir = os.path.abspath('../')
        provinces = set()
        cities_dirs = []
        for row in reader:
            if i != 0:
                province_name = str(row[0])
                if province_name not in provinces:
                    provinces.add(province_name)
                    province_dir = os.path.join(tempDir, 'data', province_name)
                    os.mkdir(province_dir)
                temp = os.path.join(tempDir, 'data', province_name, str(row[1]))
                cities_dirs.append(temp)
            i = 1

        for city_dir in cities_dirs:
            os.mkdir(city_dir)


'''
if __name__ == '__main__':
    init_dirs()
'''
