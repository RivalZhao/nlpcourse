#coding=utf-8
import os
from tqdm import tqdm
import os.path


# 获取目标文件夹的路径
filedir = 'E:/BaiduNetdiskDownload/wiki/temp/'
# 获取当前文件夹中的文件名称列表
dirnames = os.listdir(filedir)

f = open('E:/BaiduNetdiskDownload/wiki/temp_merge/result_merge', 'w', encoding='utf-8')
for dirname in dirnames:
    filenames = os.listdir(filedir + dirname)
    # 先遍历文件名
    for filename in tqdm(filenames):
        filepath = filedir + dirname + '/' + filename
        # 遍历单个文件，读取行数
        for line in open(filepath, encoding='utf-8'):
            f.writelines(line)
        f.write('\n')
# 关闭文件
f.close()

