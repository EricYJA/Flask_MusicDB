# input: 一个歌手的所有歌
# 格式： list， 一首歌一个string

from random import shuffle
import pandas as pd
from seg import Seg
from svm import SVM
from feature_extraction import FeatureExtraction
from sentimentAnalysis import Sentiment
import matplotlib.pyplot as plt
import os
import seaborn as sns
import time
import random
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def Analysis(lyric, mod = True): 
    if mod == False:
        pos = []
        neg = []
        with open("D:\\Academic_work\\01_ERG3010\\Project\\corpus\\doubandata.txt", 'r', encoding = 'utf-8-sig') as f:
            for line in f:
                line = f.readline()
                line = line.split("##")
                try:
                    star = int(line[1])
                except:
                    pass
                if star == 1 or star == 2:
                    neg.append(line[2].strip('\n'))
                elif star == 4 or star == 5:
                    pos.append(line[2].strip('\n'))

        ''' segment '''
        seg_pos = Seg().seg_from_datalist(pos)
        seg_neg = Seg().seg_from_datalist(neg)

        ''' training & test  '''
        word_list = []
        lable_list = []
        data = []
        train_data = []
        shuffle(seg_pos)
        shuffle(seg_neg)
        for k in seg_pos[:500]:
            train_data.append(('pos', k))
            word_list.append(k)
            lable_list.append('pos')
        for k in seg_neg[:500]:
            train_data.append(('neg', k))
            word_list.append(k)
            lable_list.append('neg') 

        ''' train, test'''
        fe = FeatureExtraction(word_list, lable_list)
        best_words = fe.best_words(3000, False)
        best_words = "D:\Academic_work\01_ERG3010\Project\lyricsAnalysis2\svmmodel-bestwords.dat"
        model = Sentiment(best_words)
        model.train_model(train_data)
        model.save_model(root_path + "\\lyricsAnalysis2\\svmmodel")
    else:
        model = Sentiment()
        model.load_model(root_path + "\\lyricsAnalysis2\\svmmodel")

    result = model.predict_datalist(lyric) # lyric 是一个list, 放每一首歌曲
    data = []
    count = 1
    for prob in result:
        time = "{}/{}".format((count // 12), count // 30)
        data.append([count, prob, "Pos"])
        data.append([count, 1-prob, "Neg"])
        count += 1

    ''' text visualization '''
    tr = ThemeRiver("Sentiment",
                    title_color = "#274C77",
                    title_text_size = 20)
    tr.add(['Pos','Neg'], data, 
            is_label_show=True,
            is_datazoom_show=True,
            legend_text_color = "#274C77",
            legend_text_size = 15)
    tr.render("ThemeRiver.html")