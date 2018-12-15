'''
歌手页面下
词频 词性的统计
抓取数据库中的歌词
'''

from collections import Counter, defaultdict
import thulac
import os
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import json
import codecs

def cut_song_to_words(song_file, saved_words_file):
    save_dir = os.path.dirname((saved_words_file))

    char_counter = Counter()  # 字频统计
    vocab = set()  # 词汇库
    word_counter = Counter()  # 词频统计
    genre_counter = defaultdict(Counter)  # 针对每个词性的Counter

    fid_save = open(saved_words_file, 'w', encoding = 'utf-8') #word2vec 要读的文件
    lex_analyzer = thulac.thulac()  # 分词器
    line_cnt = 0
    with open(song_file, 'r', encoding = 'utf-8') as f:
        all_lyrics = f.read()
        lyrics_segs = all_lyrics.split("+")  # 一首歌 一首歌分开

        for one_song in lyrics_segs:
            # 以下以一首歌为单位进行操作
            # 去除非汉字字符
            valid_char_list = [c for c in one_song if '\u4e00' <= c <= '\u9fff' or c == '，' or c == '。']
            for char in valid_char_list:
                char_counter[char] += 1
            regularized_song = ''.join(valid_char_list)
            word_genre_pairs = lex_analyzer.cut(regularized_song)
            
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
def word2vec(words_file):
    save_dir = os.path.dirname((words_file))
    vector_file = os.path.join(save_dir, 'word_vectors.model')
    
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
    with codecs.open("broad_adj.json", "w", "utf-8") as f:
        f.write(json_data_adj)
    with codecs.open("broad_time.json", "w", "utf-8") as f:
        f.write(json_data_time)
    with codecs.open("broad_scene.json", "w", "utf-8") as f:
        f.write(json_data_scene)    

def broadAnalysis():
    # song_path: 原始歌词 来自mysql
    # 同时 得到歌手的名字
    song_file = "D:\\Academic_work\\01_ERG3010\\ERGproj\\broadTextMining\\lijianlyrics2.txt"
    words_file = "D:\\Academic_work\\01_ERG3010\\ERGproj\\broadTextMining\\words_file.txt"
    # 如果这个歌手的所有歌词没有训练过，或者有大量新的歌词加进来，重新统计
    # 如果没有更改，或者已经训练过则读取原有的json文件
    # 有重大改动删除相关json文件
    if not (os.path.exists(os.path.join(current_path, "broad_adj.json")) and 
            os.path.exists(os.path.join(current_path, "broad_time.json")) and
            os.path.exists(os.path.join(current_path, "broad_scene.json"))):
        char_counter, genre_counter = cut_song_to_words(song_file, words_file) #输入一个歌手所有歌曲歌词
        vector_model = word2vec(words_file) #无需用户输入
        write2Json(char_counter, genre_counter, vector_model) #无需用户输入

broadAnalysis()
