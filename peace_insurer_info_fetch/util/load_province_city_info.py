# -*- coding: utf-8 -*-

import requests
import json
import csv


def load_province_city_info():
    html = requests.get(url='http://life.pingan.com/app_js/pingan/v20/life/city.js')
    txt = html.text
    jsonStr = txt[txt.index('['):-1]
    objs = json.loads(jsonStr)
    info = []
    for obj in objs: info.append((obj['ProID'], obj['CityID'], obj['CityName']))
    with open('../data/province_city_info.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(info)


def get_province_city_info():
    with open('../data/province_city_info.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        info = []
        for e in reader: info.append(e)
    return info


if __name__ == '__main__':
    # load_province_city_info()
    get_province_city_info()
