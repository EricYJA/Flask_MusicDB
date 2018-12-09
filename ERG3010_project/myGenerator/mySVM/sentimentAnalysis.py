from svm import SVM
from seg import Seg
import os


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

