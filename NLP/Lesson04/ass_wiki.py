from pathlib import Path
from tqdm import tqdm
import jieba
import pickle
import re
import logging
import gensim
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib

# print(os.system(r'python ../../PreClass/tttre.py'))
# .\opencc -c t2s.json -i E:\BaiduNetdiskDownload\wiki\temp\result_AA.txt -o E:\BaiduNetdiskDownload\wiki\temp_simplified\AA
# .\opencc -c t2s.json -i E:\BaiduNetdiskDownload\wiki\temp_merge\result_merge -o E:\BaiduNetdiskDownload\wiki\temp_simplified\result_simplified

# 将语料进行切词，并保存结果
def cutword_save():
    pattern = "[“”，。「」（）《》、\'·\"\-  ]"
    words = [] # 所有的词
    line_num = 0 # 行数
    file_num = 0 # 缓存的文件数
    openfile = open('E:/BaiduNetdiskDownload/wiki/temp_simplified/result_simplified', encoding='utf-8')
    # 读取每一行
    for line in tqdm(openfile.readlines()):
        # 去除不需要的行
        line = line.strip()
        if line == '' or line.startswith('<doc') or line.startswith('</doc'):
            continue
        line = re.sub(pattern, '', line)
        if len(line) < 2:
            continue
        # 去除不需要的行
        words_line = [] # 用于存储每一行切分后的词
        for word in jieba.cut(line):
            if len(word) > 0:
                words_line.append(word)
        words.append(words_line)# 将每一行切出的词，存入总的词list中
        line_num += 1
        if line_num % 100000 == 0:
            print('finish line:' + str(line_num))
        if line_num % 1000000 == 0:
            file_num += 1
            with open('E:/BaiduNetdiskDownload/wiki/temp_simplified/cut_simplified_' + str(file_num) + 'bw', 'wb') as tempf:
                pickle.dump(words, tempf)
            words = []
            print('------------------save line ' + str(line_num) + ' ------------------')
    with open('E:/BaiduNetdiskDownload/wiki/temp_simplified/cut_simplified_end', 'wb') as f:
        pickle.dump(words, f)


def open_cutword():
    with open('E:/BaiduNetdiskDownload/wiki/temp_simplified/cut_simplified_1bw', 'rb') as tempf:
        cutword1 = pickle.load(tempf)
    print(len(cutword1))
    for i in range(20):
        print(cutword1[i])


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# 训练词向量
def creatWord2Vec():
    wiki_words = []
    with open('E:/BaiduNetdiskDownload/wiki/temp_simplified/cut_simplified_1bw', 'rb') as wikif:
        wiki_words += pickle.load(wikif)
    with open('E:/BaiduNetdiskDownload/wiki/temp_simplified/cut_simplified_2bw', 'rb') as wikif:
        wiki_words += pickle.load(wikif)
    with open('E:/BaiduNetdiskDownload/wiki/temp_simplified/cut_simplified_3bw', 'rb') as wikif:
        wiki_words += pickle.load(wikif)
    with open('E:/BaiduNetdiskDownload/wiki/temp_simplified/cut_simplified_4bw', 'rb') as wikif:
        wiki_words += pickle.load(wikif)
    with open('E:/BaiduNetdiskDownload/wiki/temp_simplified/cut_simplified_5bw', 'rb') as wikif:
        wiki_words += pickle.load(wikif)
    with open('E:/BaiduNetdiskDownload/wiki/temp_simplified/cut_simplified_end', 'rb') as wikif:
        wiki_words += pickle.load(wikif)
    Word2VecModel = Word2Vec(wiki_words, size=100, window=5, min_count=500, workers=16)
    Word2VecModel.save('./model/wiki_news_all_500')
    #Word2VecModel.wv.save_word2vec_format('./model/word2vec_format.txt')
    # aa = [['数学'], ['数学', '是']]
    # bb = [['数学'], ['数学', '是']]
    # cc = aa + bb
    # print(cc)


def testWord2Vec():
    model = gensim.models.Word2Vec.load('./model/wiki_news_500')
    #print(model.similarity('西红柿', '番茄'))
    print(model.most_similar(['美丽']))
    #tsne_plot(model)


def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['font.family'] = 'sans-serif'

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


#cutword_save()
#open_cutword()
creatWord2Vec()
#testWord2Vec()