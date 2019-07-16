# -*- coding:UTF-8 -*-
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import ttfFontProperty
import numpy as np
import pandas as pd
import networkx as nx
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from collections import deque
import re

'''
x = np.linspace(-1, 1, 50)
y = 2*x + 1

plt.figure(figsize=(5, 5), dpi=80)
plt.plot(x, y)
plt.show()
'''


def get_coord_information():
    subway_coord_csv = pd.read_csv("./data/北京地铁经纬度信息.csv", encoding='GBK', low_memory=False)
    subway_station_list = subway_coord_csv['站名'].tolist()
    subway_coord_list = subway_coord_csv['经纬度'].tolist()
    subway_line_list = subway_coord_csv['线路'].tolist()
    #print(subway_station_list)
    subway_coord_lib = {}
    for index, station in enumerate(subway_station_list):
        long, lat = [coord.strip() for coord in subway_coord_list[index].split(',')]
        subway_coord_lib[station] = (float(long), float(lat))
    print(subway_coord_lib)
    return subway_coord_lib


def draw_beijing_subway_graph(subway_coord_lib):
    subway_graph = nx.Graph()
    subway_graph.add_nodes_from(list(subway_coord_lib.keys()))
    nx.draw(subway_graph, subway_coord_lib, with_labels=True, node_size=20)
    #zhfont1 = matplotlib.font_manager.FontProperties(fname='E:/CloudStationBackup/PyCharm/NLP-ClassFile/nlpcourse/NLP/Lesson02/data/simsun.ttc')
    #plt.xlabel(u'中文字体', fontproperties=zhfont1)
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['font.family'] = 'sans-serif'
    #plt.figure(figsize=(5, 5), dpi=8)
    plt.show()

def get_line_information():
    line_dict = {}
    req = requests.Session()
    req.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400'
    redata = requests.get(url='https://www.bjsubway.com/station/xltcx/', verify=False)
    redata.encoding = 'gbk'
    pageSoup = BeautifulSoup(redata.text, 'lxml')
    line_name = ''
    line_dict = defaultdict(list)
    for line_info in pageSoup.find_all('div'):
        if line_name == '':
            # print(line_info.get('class'))
            if line_info.get('class') == ['subway_num1']:
                line_name = line_info.get_text()
        else:
            if line_info.get('class') == ['station']:
                line_dict[line_name] = line_dict[line_name] + [line_info.get_text()]
            else:
                if line_info.get('class') == ['other']:
                    break
                line_name = line_info.get_text()
    # print(line_dict)
    return line_dict


def deal_special_line(line_dict):
    line_dict['14号线西段'] = line_dict['14号线'][:7]
    line_dict['14号线东段'] = ['善各庄', '来广营', '东湖渠', '望京', '阜通', '望京南', '将台', '东风北桥', '枣营', '朝阳公园', '金台路', '大望路', '九龙山', '平乐园', '北工大西门', '十里河', '方庄', '蒲黄榆', '景泰', '永定门外', '北京南站']
    line_dict['8号线北段'] = line_dict['8号线'][:19]
    line_dict['8号线南段'] = line_dict['8号线'][19:]
    line_dict.pop('14号线')
    line_dict.pop('8号线')
    return line_dict


# 打印没有坐标信息的站名
def check_nocoord_station(subway_coord_lib, line_dict):
    for line, stations in line_dict.items():
        for station in stations:
            print("line:" + str(line) + "  station:" + station)
            if station not in subway_coord_lib:
                print(station)


def transform_station_format(line_dict):
    station_dict = defaultdict(list)
    for line, station in line_dict.items():
        for seq, station_name in enumerate(station):
            if seq > 0:
                station_dict[station_name].append(station[seq-1])
            if seq < len(station)-1:
                station_dict[station_name].append(station[seq+1])
    return station_dict


def bfs_search(start, destination, connection_grpah):
    pathes = [[start]]
    visitied = set()
    while pathes:  # if we find existing pathes
        path = pathes.pop(0)
        froninter = path[-1]
        if froninter in visitied: continue
        successors = connection_grpah[froninter]
        for city in successors:
            if city in path: continue  # eliminate loop
            new_path = path + [city]
            pathes.append(new_path)
            if city == destination: return new_path
        visitied.add(froninter)
    print('终点不可达')


def dfs_search(start, destination, connection_grpah):
    pathes = [[start]]
    visitied = set()
    while pathes:  # if we find existing pathes
        path = pathes.pop()
        froninter = path[-1]
        if froninter in visitied: continue
        successors = connection_grpah[froninter]
        for city in successors:
            if city in path: continue  # eliminate loop
            new_path = path + [city]
            pathes.append(new_path)
            if city == destination: return new_path
        visitied.add(froninter)
    print('终点不可达')


def leaststation_search(start, destination, connection_grpah):
    pathes = [[start]]
    visitied = set()
    while pathes:  # if we find existing pathes
        path = pathes.pop()
        froninter = path[-1]
        if froninter in visitied: continue
        successors = connection_grpah[froninter]
        for city in successors:
            if city in path: continue  # eliminate loop
            new_path = path + [city]
            pathes.append(new_path)
            if city == destination: return new_path
        visitied.add(froninter)
        pathes = sorted(pathes, key=len, reverse=True)  # 我们可以加一个排序函数 对我们的搜索策略进行控制
    print('终点不可达')


subway_coord_lib = get_coord_information()  # 获取坐标信息
# draw_beijing_subway_graph(subway_coord_lib)  #画图 存在不能放大的问题
line_dict = get_line_information()  # 获取线路信息
line_dict = deal_special_line(line_dict)  # 处理两条分段线路
# print(line_dict)
# check_nocoord_station(subway_coord_lib, line_dict)
station_dict = transform_station_format(line_dict)
# print(station_dict)
print(bfs_search("农大南路", "双井", station_dict))
print(dfs_search("农大南路", "双井", station_dict))
print(leaststation_search("农大南路", "双井", station_dict))

