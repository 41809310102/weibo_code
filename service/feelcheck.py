import pandas
import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np
import jieba
from jieba import analyse
import csv
# 生成词云数据
from wordcloud import WordCloud


def write(data, name):
    # 打开文件
    file_name = 'G:/代做毕业设计/film-recommend/static/{}.csv'.format(name)
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "console", "local"])

    try:
        pd.DataFrame(data).to_csv(file_name)
    except:
        print("the data is over")


def read_files(data_file):
    data = pd.read_csv(data_file)  # 读取csv文件数据
    data.head(2)
    data1 = data[['id', 'console', 'source']]
    data1.head(10)
    data1['emotion'] = data1['console'].apply(lambda x: SnowNLP(x).sentiments)
    print(data1.head(10))
    data1.describe()
    return data1


def getattion_chart(data1):
    # 计算积极评论与消极评论各自的数目
    pos = 0
    neg = 0
    for i in data1['emotion']:
        if i >= 0.5:
            pos += 1
        else:
            neg += 1
    # 积极评论占比
    res = {
        'pos': pos,
        'neg': neg
    }
    print(res)
    return res


def getap10_chart(data):
    # 关键词top10
    text = ''
    for s in data['console']:
        text += s
    key_words = jieba.analyse.extract_tags(sentence=text, topK=10, withWeight=True, allowPOS=())
    print(key_words)
    res = []
    for k in range(0, 10):
        res.append(key_words[k][0])
    return res
    # 参数说明 ：
    # sentence
    # 需要提取的字符串，必须是str类型，不能是list
    # topK
    # 提取前多少个关键字
    # withWeight
    # 是否返回每个关键词的权重
    # allowPOS是允许的提取的词性，默认为allowPOS =‘ns’, ‘n’, ‘vn’, ‘v’，提取地名、名词、动名词、动词


def getcloud_chart(data):
    w = WordCloud(background_color="white",
                  font_path="G:/代做毕业设计/film-recommend/service/SimplifiedChinese/SourceHanSerifSC-SemiBold.otf")  # font_path="msyh.ttc"，设置字体，否则显示不出来
    text = ''
    for s in data:
        text += s + "\n"
    w.generate(text)
    w.to_file("G:/代做毕业设计/film-recommend/static/img/doubanTop10cloud.png")


if __name__ == '__main__':
    getap10_chart(read_files())
