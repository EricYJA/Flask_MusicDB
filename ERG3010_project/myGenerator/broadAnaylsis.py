'''
歌手页面下
词频 词性的统计
抓取数据库中的歌词
'''

from collections import Counter, defaultdict
import jieba.posseg as psg
import os
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import json
import codecs


def cut_song_to_words(all_lyrics, saved_words_file):
    save_dir = os.path.dirname((saved_words_file))

    char_counter = Counter()  # 字频统计
    vocab = set()  # 词汇库
    word_counter = Counter()  # 词频统计
    genre_counter = defaultdict(Counter)  # 针对每个词性的Counter

    fid_save = open(saved_words_file, 'w', encoding = 'utf-8') #word2vec 要读的文件
    line_cnt = 0

    lyrics_segs = all_lyrics.split("+")  # 一首歌 一首歌分开

    for one_song in lyrics_segs:
        # 以下以一首歌为单位进行操作
        # 去除非汉字字符
        valid_char_list = [c for c in one_song if '\u4e00' <= c <= '\u9fff' or c == '，' or c == '。']
        for char in valid_char_list:
            char_counter[char] += 1
        regularized_song = ''.join(valid_char_list)
        word_genre_pairs = []
        for w in psg.cut(regularized_song):
            word_genre_pairs.append([w.word, w.flag])
        word_list = []
        for word, genre in word_genre_pairs:
            word_list.append(word)
            vocab.add(word)
            word_counter[word] += 1
            genre_counter[genre][word] += 1

        save_line = ' '.join(word_list)
        fid_save.write(save_line + '\n')   # 一首歌一行，进行 word2vec 词向量分析

        if line_cnt % 10 == 0:
            print('%d songs processed.' % line_cnt)
        line_cnt += 1

    fid_save.close()

    return char_counter, genre_counter


# 将分词结果转换为向量
def word2vec(words_file, singer_name):
    save_dir = os.path.dirname((words_file))
    vector_file = os.path.join(save_dir, '{}_word_vectors.model'.format(singer_name))

    if os.path.exists(vector_file):
        print('find word vector file, loading directly...')
        model = Word2Vec.load(vector_file)
    else:
        print('calculating word vectors...')
        model = Word2Vec(LineSentence(words_file), size=400, window=3, min_count=10,
                     workers=multiprocessing.cpu_count())
        # 将计算结果存储起来，下次就不用重新计算了
    model.save(vector_file)

    return model


def write2Json(char_counter, genre_counter, vector_model):
    def get_counter(counter):
        list_ = []
        num = []
        words = []
        for k, v in counter:
            list_.append([k, v])
            num.append(v)
            words.append(k)
        return list_, words, num

    # 基于词的分析
    # 形容词, 时间词, 场景词排名
    adj = genre_counter['a'].most_common(10)
    time = genre_counter['t'].most_common(10)
    scene = genre_counter['s'].most_common(10)
    dataA, wordsA, numA = get_counter(adj)
    dataT, wordsT, numT = get_counter(time)
    dataS, wordsS, numS = get_counter(scene)

    json_data_adj = json.dumps(dataA)
    json_data_time = json.dumps(dataT)
    json_data_scene = json.dumps(dataS)
    with codecs.open("ERG3010_project/static/broad_adj.json", "w", "utf-8") as f: # 改路径
        f.write(json_data_adj)
    with codecs.open("ERG3010_project/static/broad_time.json", "w", "utf-8") as f: # 改路径
        f.write(json_data_time)
    with codecs.open("ERG3010_project/static/broad_scene.json", "w", "utf-8") as f: # 改路径
        f.write(json_data_scene)


def broadAnalysis(singer_name, total_lyrics):
    # 同时 得到歌手的名字
    root_path = os.path.abspath('.')
    words_file = "ERG3010_project/myGenerator/words_file.txt" # 不用改

    # song_file: 就是输入的歌词
    # words_file：words file
    # json文件的路径放在你想放的路径里, 发送给前段的只有json文件
    char_counter, genre_counter = cut_song_to_words(total_lyrics, os.path.join(root_path, words_file))
    vector_model = word2vec(os.path.join(root_path, words_file), singer_name) #无需用户输入, 需要歌手名字
    write2Json(char_counter, genre_counter, vector_model) #无需用户输入


if __name__ == "__main__":
    broadAnalysis()

