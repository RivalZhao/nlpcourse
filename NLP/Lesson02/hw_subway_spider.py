import requests
from bs4 import BeautifulSoup
import re
#import lxml

###############################
# 由于百度百科爬取情况太多，放弃。。。
###############################


req = requests.Session()
req.headers['User-Agent']= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
redata = req.get(url='https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485?fr=aladdin')
redata.encoding = 'utf-8'


def get_line_link1(redata):
    begin_index = redata.text.find('<h3 class="title-text"><span class="title-prefix">北京地铁</span>运行时间</h3>')
    end_index = redata.text.find('<a name="客运流量" class="lemma-anchor " ></a>')
    line_content = redata.text[begin_index: end_index]
    line_pattern = re.compile(r"<a target=_blank href=\"(.+?)\".*?>(北京地铁.+?)</a>")
    line_link = {}
    for link, name in line_pattern.findall(line_content):
        #if name in line_link: continue
        line_link[name] = "https://baike.baidu.com" + link
    return line_link


def get_line_link2(redata):
    pageSoup = BeautifulSoup(redata.text, 'lxml')
    table_link = None
    for all_link in pageSoup.find_all('a'):
        # print(all_link.get('name'))
        if all_link.get('name') == "运行时间":
            for table_link in all_link.parent.next_siblings:
                if table_link.name == 'table':
                    break
    line_link_dict = {}
    for line_link in table_link.find_all('a'):
        if line_link.get('target') == '_blank':
            # print(line_link.get('href'))
            # print(line_link.get_text())
            line_link_dict[line_link.get_text()] = "https://baike.baidu.com" + line_link.get('href')
            # print(line_link_dict)
    return line_link_dict


def get_station(line_url='https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%8116%E5%8F%B7%E7%BA%BF'):
    station = []
    redata = req.get(line_url)
    redata.encoding = 'utf-8'
    pageSoup = BeautifulSoup(redata.text, 'lxml')
    table_html_list = []
    line_name = []
    line_name_list = []
    return_dict = {}
    for all_html in pageSoup.find_all(['caption', 'td', 'th', 'h3']):
    #for all_html in pageSoup.find_all('h3'):
        station_pattern = re.compile(r"(.+?线.*?)首末[班]*车时[刻间][表]*")
        #station_pattern = re.compile(r".*?首末车时间")
        if station_pattern.match(all_html.get_text()):
            #print(all_html.get_text())  # 北京地铁8号线（北段）首末车时刻表
            if all_html.parent.name == 'table':
                table_html_list.append(all_html.parent)
                #print(all_html.parent)
            else:
                table_html_list.append(all_html.parent.parent)
                #print(all_html.parent.parent)
            line_name = station_pattern.findall(all_html.get_text())
            if line_name[0].find("北京地铁") >= 0:
                line_name_list.append(line_name[0])
            else:
                line_name_list.append("北京地铁"+line_name[0])
    for index, table in enumerate(table_html_list):
        for station_html in table.find_all(['th', 'td']):
            station_text = station_html.get_text()
            if len(station_text) > 15 or station_text.find("暂缓开通") >= 0 or station_text.find("-") >= 0 or station_text.find("—") >= 0 or station_text == "":
                continue
            if station_text.find("末车时间") >= 0 or station_text.find("全程") >= 0 or station_text.find("末班车") >= 0:
                station = []
                continue
            error_pattern = re.compile(r"\d")
            if error_pattern.match(station_text):
                continue

            station.append(station_text)
        return_dict[line_name_list[index]] = station[0:-1]
    return return_dict

#print(get_station())

line_link = get_line_link2(redata)
station_dict = {}
for line_name, line_url in line_link.items():
    # dictmerged = dict(station_dict)
    # station_dict = dictmerged.update(get_station(line_url))
    print(get_station(line_url))
#print(station_dict)


# for link in pageSoup.find_all(name='a',attrs={"href":re.compile(r'^/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%'),"target":re.compile(r'blank')}):
#
# for i in range(len(linklist)):
#     r = s.get('https://baike.baidu.com'+linklist[i]).text
