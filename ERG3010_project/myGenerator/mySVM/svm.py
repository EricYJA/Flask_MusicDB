from sklearn.svm import SVC
from sklearn.externals import joblib
from seg import Seg
import numpy as np
import os
import pickle
import gzip


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
