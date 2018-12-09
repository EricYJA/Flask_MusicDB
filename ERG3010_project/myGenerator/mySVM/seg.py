import os
import jieba
import pymysql
import re
import numpy as np
from scipy.misc import imread

root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Seg(object):
    stop_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\lyricsAnalysis2\\stopwords.txt'

    def __init__(self):
        self.seg_result = []

    def stopwordslist(self):
        stopwords = [line.strip() for line in open(self.stop_path, 'r', encoding='utf-8').readlines()]
        return stopwords

    def get_data_from_mysql(self, qty, offset):
        commentlist = []
        with self.db:
            cur = self.db.cursor()
            sql = "SELECT text FROM comments LIMIT %s OFFSET %s" % (qty, offset)
            cur.execute(sql)
            rows = cur.fetchall()
        reg = u"[\u4e00-\u9fa5]+"
        for row in rows:
            res = re.findall(reg, row[0])
            if not res:
                continue
            if res not in commentlist:
                commentlist.append(res[0])
        return commentlist

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

    def seg_from_mysql(self, qty):
        datalist = self.get_data_from_mysql(qty)
        self.seg_result = self.seg_from_datalist(datalist)
        return self.seg_result

    @staticmethod
    def seg_sentence(sentence):
        sentence_seged = jieba.cut(sentence.strip())
        return sentence_seged
