
'''
歌手页面下
歌曲页面下
对歌词，评论进行分析
抓取数据库中的评论和歌词
'''


import os
import jieba
import re
from scipy.misc import imread
from sklearn.svm import SVC
from sklearn.externals import joblib
import numpy as np
import pickle
import gzip
import pandas as pd
import random
import json
import codecs

root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Seg(object):
    # 保存 stopwords 的路径
    stop_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\SentimentAnalysisok\\stopwords.txt'

    def __init__(self):
        self.seg_result = []

    def stopwordslist(self):
        stopwords = [line.strip() for line in open(self.stop_path, 'r', encoding='utf-8').readlines()]
        return stopwords

    def get_keyword_from_datalist(self, datalist):
        keyword = {}

        stopwords = self.stopwordslist()
        for sentence in datalist:
            seged_sentence = self.seg_sentence(sentence)
            words = list(set(seged_sentence) - set(stopwords))
            for word in words:
                keyword[word] = keyword.get(word, 0) + 1

        keyword = sorted(keyword.items(), key=lambda x: x[1], reverse=True)
        return keyword

    def seg_from_datalist(self, datalist):
        stopwords = self.stopwordslist()

        res = []

        for sentence in datalist:
            seged_sentence = self.seg_sentence(sentence)
            res.append(list(set(seged_sentence) - set(stopwords)))
        return res

    def seg_from_doc(self, doc):
        stopwords = self.stopwordslist()

        res = []
        s = doc.split('\n')

        for sentence in s:
            seged_sentence = self.seg_sentence(sentence)
            res.append(list(set(seged_sentence) - set(stopwords)))
        return res

    @staticmethod
    def seg_sentence(sentence):
        sentence_seged = jieba.cut(sentence.strip())
        return sentence_seged

class Sentiment(object):
    def __init__(self, best_words = None):
        self.svm = SVM(50, best_words)
        self.seg = Seg()
    def train_model(self, data):
        self.svm.train_model(data)

    def save_model(self, filename):
        self.svm.save_model(filename)

    def load_model(self, filename):
        self.svm.load_model(filename)

    def predict_doc_svm(self, sentence):
        print("------ SVM Classifier predicting over ------")
        prob = self.svm.predict_sentence(sentence)
        print("------ SVM Classifier predicting over ------")
        return prob

    def predict_datalist_svm(self, datalist):
        print("------ SVM Classifier is predicting ------")
        result = self.svm.predict_datalist(datalist)
        print("------ SVM Classifier predicting over ------")
        return result

    def predict_sentence_doc(self, sentence):
        return self.predict_doc_svm(sentence)

    def predict_datalist(self, datalist):
        return self.predict_datalist_svm(datalist)


class SVM(object):
    def __init__(self, c, best_words):
        self.seg = Seg()
        self.clf = SVC(probability=True, C=c)
        self.train_data = []
        self.train_label = []
        self.best_words = best_words

    def words2vector(self, all_data):
        vectors = []
        for data in all_data:
            vector = []
            for feature in self.best_words:
                vector.append(data.count(feature))
            vectors.append(vector)
            # print(vector)
        vectors = np.array(vectors)
        return vectors

    def train_model(self, data):
        print("------ SVM Classifier is training ------")
        for d in data:
            label = d[0]
            doc = d[1]
            self.train_data.append(doc)
            self.train_label.append(label)

        self.train_data = np.array(self.train_data)
        self.train_label = np.array(self.train_label)

        train_vectors = self.words2vector(self.train_data)
        self.clf.fit(train_vectors, self.train_label)

        print("------ SVM Classifier training over ------")

    def save_model(self, filename):
        print("------ SVM Classifier is saving model ------")
        joblib.dump(self.clf, filename+'-model.m')
        f = gzip.open(filename + '-bestwords.dat', 'wb')
        d = {}
        d['best words'] = self.best_words
        f.write(pickle.dumps(d))
        f.close()
        print("------ SVM Classifier saving model over ------")

    def load_model(self, filename):
        print("------ SVM Classifier is loading model ------")
        self.clf = joblib.load(filename+'-model.m')

        f = gzip.open(filename+'-bestwords.dat', 'rb')
        d = pickle.loads(f.read())
        f.close()
        self.best_words = d['best words']
        print("------ SVM Classifier loading model over ------")

    def predict_wordlist(self, sentence):
        vector = self.words2vector([sentence])
        prediction = self.clf.predict(vector)
        prob = self.clf.predict_proba(vector)[0][1]
        return prediction[0], prob

    def predict_sentence(self, sentence):
        seged_sentence = self.seg.seg_from_doc(sentence)
        prediction, prob = self.predict_wordlist(seged_sentence)
        return prediction, prob

    def predict_datalist(self, datalist):
        seged_datalist = self.seg.seg_from_datalist(datalist)
        result = []
        for data in seged_datalist:
            prediction, prob = self.predict_wordlist(data)
            result.append(prob)
        return result

class FeatureExtraction(object):
    def __init__(self, doc_list, doc_labels):
        self.total_data, self.total_pos_data, self.total_neg_data = {}, {}, {}
        for i, doc in enumerate(doc_list):
            if doc_labels[i] == 'pos':
                for word in doc:
                    self.total_pos_data[word] = self.total_pos_data.get(word, 0) + 1
                    self.total_data[word] = self.total_data.get(word, 0) + 1
            else:
                for word in doc:
                    self.total_neg_data[word] = self.total_neg_data.get(word, 0) + 1
                    self.total_data[word] = self.total_data.get(word, 0) + 1

        total_freq = sum(self.total_data.values())
        total_pos_freq = sum(self.total_pos_data.values())
        total_neg_freq = sum(self.total_neg_data.values())

        self.words = {}
        for word, freq in self.total_data.items():
            pos_score = self.__calculate(self.total_pos_data.get(word, 0), freq, total_pos_freq, total_freq)
            neg_score = self.__calculate(self.total_neg_data.get(word, 0), freq, total_neg_freq, total_freq)
            self.words[word] = (pos_score + neg_score)

    @staticmethod
    def __calculate(n_ii, n_ix, n_xi, n_xx):
        n_ii = n_ii
        n_io = n_xi - n_ii
        n_oi = n_ix - n_ii
        n_oo = n_xx - n_ii - n_oi - n_io
        return n_xx * (float((n_ii * n_oo - n_io * n_oi) ** 2) /
                       ((n_ii + n_io) * (n_ii + n_oi) * (n_io + n_oo) * (n_oi + n_oo)))

    def best_words(self, num, need_score=False):
        words = sorted(self.words.items(), key=lambda word_pair: word_pair[1], reverse=True)
        if need_score:
            return [word for word in words[:num]]
        else:
            return [word[0] for word in words[:num]]

'''

Application

# input: lyric/评论 
# 格式： string (如果是多首歌，用+连接) (如果是评论，每条评论用加号连接)
# mod: True 使用原有模型
       False 重新训练

'''

def Analysis(lyric, mod = False): 
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
        random.shuffle(seg_pos)
        random.shuffle(seg_neg)
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
        # best_words = "D:\Academic_work\01_ERG3010\Project\lyricsAnalysis2\svmmodel-bestwords.dat"
        model = Sentiment(best_words)
        model.train_model(train_data)
        model.save_model(root_path + "\\SentimentAnalysisok\\svmmodel")  # 保存 model 的路径
    else:
        model = Sentiment()
        model.load_model(root_path + "\\SentimentAnalysisok\\svmmodel")  # 保存model 的路径

    lyrics_segs = lyric.split("+")  # 一首歌 一首歌分开
    lyrics_list = []
    for one_song in lyrics_segs:
        # 以下以一首歌为单位进行操作
        # 去除非汉字字符
        lines = one_song.split("\n")
        lines_list = []
        for line in lines:
            if ":" not in line:
                valid_char_list = [c for c in one_song if '\u4e00' <= c <= '\u9fff']
                lines_list.append("".join(valid_char_list))
        lyrics_list.append(" ".join(lines_list))
    
    result = model.predict_datalist(lyrics_list) 
    data = []
    count = 1
    for i in range(len(result)):
        data.append([count, result[i], "Pos"])
        data.append([count, 1-result[i], "Neg"])
        count += 1
    
    json_data = json.dumps(data)
    if len(data) > 2:
        with codecs.open("sentiment_data.json", "w", "utf-8") as f:
            f.write(json_data)
    else:
        with codecs.open("sentiment_data_1.json", "w", "utf-8") as f:
            f.write(json_data)

#------------------------------------------------------------------------#

with open("D:\\Academic_work\\01_ERG3010\\ERGproj\\SentimentAnalysisok\\lijianlyrics2.txt", "r", encoding = "utf-8") as f:
    lyric = f.read()

Analysis(lyric, mod = True)  # Analysis(lyric, mod)

