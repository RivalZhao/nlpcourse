import random
import re
import pandas as pd
import jieba
from collections import Counter

insurance = """
insurance = 称谓 产品 副词 问题
称谓 = 称谓 | 您好 | 您 | 我 | 我的 | 他 | 他的 | null
产品 = 副词 保险名
副词 = 什么 | 为什么 | 是 | 多少 | null
保险名 = 健康保险 | 人寿保险 | 意外险 | 财险
问题 = 多少钱 | 不好 | 如何 | 怎么样
"""

movie = """
movie = 电影 评价 例子
电影 = 电影名 数字
电影名 = 战狼 | 速度与激情 | 碟中谍 | 敢死队
数字 = 1 | 2 | 3
评价 = 评价主体 分值
评价主体 = 内容 | 场面 | 情节 | 逻辑
分值 = 五星 | 四星半 | 四星 | 超棒
例子 = 关联词 人物 形容
关联词 = 但 | 但是 | 其中 | 而且
人物 = 冷锋 | 达康书记 | 范迪塞尔 | 杰森斯坦森 | 史泰龙 | 汤姆克鲁斯
形容 = 形容词 程度
形容词 = 演技 | 表现 | 功力
程度 = 爆发 | 最棒 | 非常 | 到位
"""


def create_grammar(grammar_str, equ_split, l_split):
    grammar = {}
    for line in grammar_str.split(l_split):
        if not line.strip():
            continue
        exp, stmt = line.split(equ_split)
        grammar[exp.strip()] = [s.strip().split() for s in stmt.split('|')]
    return grammar

'''
grammar_insurance = create_grammar(insurance, '=', '\n')
grammar_movie = create_grammar(insurance, '=', '\n')
print(grammar_insurance)
'''

def generate(gram, target):
    if target not in gram:
        return target
    else:
        expaned = [generate(gram, t) for t in random.choice(gram[target])]
        return ''.join([e for e in expaned if e != 'null'])


def generate_n(grammar_str1, target1, equ_split, l_split, gener_num):
    grammar1 = create_grammar(grammar_str1, equ_split, l_split)
    sentence1 = []
    for i in range(gener_num):
        sentence1.append(generate(grammar1, target1))
        print(sentence1[i])
    return sentence1

#print(generate_n(insurance, "insurance", movie, "movie", "=", "\n", 2))


def clean(string):
    str = ""
    try:
        str = re.findall('\w+', string)
    except TypeError:
        return ""
    else:
        return str


def cut(string): return list(jieba.cut(string))


'''
generate insurance modle
#12889
'''
insurance_text_lib = []
read_index = 0
with open("./train/train.txt", 'r', encoding='utf-8') as read_file:
    while True:
        read_index += 1
        #if read_index > 1000:
        #    break
        if read_index % 1000 == 0:
            print("read insurance line:" + str(read_index))
        lines = read_file.readline()
        if not lines:
            break
        line_split = [l.strip() for l in lines.split("++$++")]
        #print(line_split)
        if not len(line_split) > 2:
            print("exception")
            print(read_index)
            continue
        insurance_text_lib.append(line_split[2])

#for i in range(10):
#    print(insurance_text_lib[i])

insurance_clean = [''.join(clean(ins)) for ins in insurance_text_lib]
#print(insurance_clean)

insurance_token = []
insurance_token_2 = []
for i, line in enumerate(insurance_clean):
    templist = []
    if i % 1000 == 0:
        print("cut insurance line:" + str(i))
    #print(line)
    templist += cut(line)
    #print(templist)  #['content']
    insurance_token += templist
    insurance_token_2 += [templist]
    #print(insurance_token_2GRAM)   #[['content'], ['法律', '要求', '残疾', '保险', '吗']]


insurance_words_count = Counter(insurance_token)
#print(insurance_words_count.most_common(10))  #[('保险', 37), ('的', 23), ('什么', 21), ('是否', 19), ('吗', 18), ('人寿保险', 16), ('我', 15), ('汽车保险', 14), ('可以', 13), ('医疗保险', 13)]
def ins_prob_1(word):
    if word in insurance_words_count:
        return insurance_words_count[word] / len(insurance_token)
    else:
        return 1/len(insurance_token)

#print(ins_prob_1("家庭"))
insurance_token_2_GRAM = []
for token_2 in insurance_token_2:
    insurance_token_2_GRAM += [''.join(token_2[i:i+2]) for i in range(len(token_2[:-1]))]
#print(insurance_token_2_GRAM[:10]) #['法律要求', '要求残疾', '残疾保险', '保险吗', '债权人可以', '可以在', '在死', '死后', '后人寿保险', '人寿保险吗']
insurance_words_count_2 = Counter(insurance_token_2_GRAM)

def ins_prob_2(word1, word2):
    if word1 + word2 in insurance_words_count_2:
        return insurance_words_count_2[word1+word2] / len(insurance_token_2_GRAM)
    else:
        return 1 / len(insurance_token_2_GRAM)
'''
generate insurance modle end
'''

'''
generate movie modle
'''
movie_text_csv = pd.read_csv("./train/movie_comments.csv", encoding='utf-8', low_memory=False)
movie_text_lib = movie_text_csv['comment'].tolist()
#print(movie_text_lib[0])

movie_clean = [''.join(clean(mov)) for mov in movie_text_lib]

movie_token = []
movie_token_2 = []
for i, line in enumerate(movie_clean):
    templist = []
    if i % 1000 == 0:
        print("cut movie line:"+ line + str(i))
    templist += cut(line)
    movie_token += templist
    movie_token_2 += [templist]


movie_words_count = Counter(movie_token)
#print(insurance_words_count.most_common(10))  #[('保险', 37), ('的', 23), ('什么', 21), ('是否', 19), ('吗', 18), ('人寿保险', 16), ('我', 15), ('汽车保险', 14), ('可以', 13), ('医疗保险', 13)]
def mov_prob_1(word):
    if word in movie_words_count:
        return movie_words_count[word] / len(movie_token)
    else:
        return 1/len(movie_token)


movie_token_2_GRAM = []
for token_2 in movie_token_2:
    movie_token_2_GRAM += [''.join(token_2[i:i+2]) for i in range(len(token_2[:-1]))]
#print(insurance_token_2_GRAM[:10]) #['法律要求', '要求残疾', '残疾保险', '保险吗', '债权人可以', '可以在', '在死', '死后', '后人寿保险', '人寿保险吗']
movie_words_count_2 = Counter(movie_token_2_GRAM)


def mov_prob_2(word1, word2):
    if word1 + word2 in movie_words_count_2:
        return movie_words_count_2[word1+word2] / len(movie_token_2_GRAM)
    else:
        return 1 / len(movie_token_2_GRAM)
'''
generate movie modle end
'''


def get_ins_probablity(sentence):
    words = cut(sentence)
    sentence_pro = 1
    for i, word in enumerate(words[:-1]):
        next_ = words[i + 1]
        probability = ins_prob_2(word, next_)/ins_prob_1(word)
        sentence_pro *= probability
    return sentence_pro


def generate_insurance_best():
    insurance_sentences = generate_n(insurance, "insurance", "=", "\n", 10)
    sentence_with_pro = []
    for sentence in insurance_sentences:
        (x, y) = (get_ins_probablity(sentence), sentence)
        tuple_sen = (x, y)
        sentence_with_pro.append(tuple_sen)
    sentence_with_pro = sorted(sentence_with_pro, key=lambda x: x[0], reverse=True)
    return sentence_with_pro[0]


def get_mov_probablity(sentence):
    words = cut(sentence)
    sentence_pro = 1
    for i, word in enumerate(words[:-1]):
        next_ = words[i + 1]
        probability = mov_prob_2(word, next_)/mov_prob_1(word)
        sentence_pro *= probability
    return sentence_pro


def generate_movie_best():
    movie_sentences = generate_n(movie, "movie", "=", "\n", 10)
    sentence_with_pro = []
    for sentence in movie_sentences:
        (x, y) = (get_mov_probablity(sentence), sentence)
        tuple_sen = (x, y)
        sentence_with_pro.append(tuple_sen)
    sentence_with_pro = sorted(sentence_with_pro, key=lambda x: x[0], reverse=True)
    return sentence_with_pro[0]

print("the best sentence is:")
print(generate_insurance_best())
print(generate_movie_best())
