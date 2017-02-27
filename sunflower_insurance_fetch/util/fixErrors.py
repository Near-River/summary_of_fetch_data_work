# -*- coding: utf-8 -*-

import os
from util.initDirs import load_cities_info
from spider.infoSpider import InfoSpider, Headers


def fix_errors():
    spider = InfoSpider()
    spider.opener = spider.get_opener(Headers)

    cities_info = load_cities_info()
    cities_map = {}
    for elem in cities_info:
        cities_map[elem[0]] = elem[1]

    tempDir = os.path.abspath('../')
    file_path = os.path.join(tempDir, 'data', 'errors_record.txt')
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        errors = f.readlines()
        errs_info = []
        for err in errors:
            s, e = err.find('('), err.find(')')
            city_dir = err[s + 1:e]
            page = err.split(' ')[-2]
            # print(city_dir, page)
            errs_info.append((city_dir, page))

        # 处理出错页面
        for (city_dir, page) in errs_info:
            url = cities_map[city_dir]
            page_url = url + '?page=' + str(page)
            # 获取该页下所有保险代理人的链接
            links = spider.load_agent_links(page_url)
            # 根据链接获取所有代理人的信息
            all_agent_info = spider.load_agent_info(links)
            # 保存代理人信息到目录 city_dir 下
            spider.save_to_csvfile(city_dir, all_agent_info)


def fix_errors2():
    spider = InfoSpider()
    spider.opener = spider.get_opener(Headers)

    tempDir = os.path.abspath('../')
    file_path = os.path.join(tempDir, 'data', 'error_links.txt')
    target_dir = os.path.join(tempDir, 'data')
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        links = list(set(f.readlines()))
        all_agent_info = spider.load_agent_info(links)
        spider.savetities_to_csvfile(target_dir)
        spider.save_to_csvfile(target_dir, all_agent_info)


if __name__ == '__main__':
    # fix_errors()
    fix_errors2()
