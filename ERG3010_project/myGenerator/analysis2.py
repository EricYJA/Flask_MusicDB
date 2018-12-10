import json
import codecs
from random import randint
 
import jieba
import re
from collections import Counter


def network(in_lyrics, singer_name):
    stopwords = []
    with open("ERG3010_project/myGenerator/stopwords.txt", 'r', encoding = 'utf-8-sig') as f:
        for line in f.readlines():
            stopwords.append(line.strip('\n'))

    word_list = []
    lyric_lines = []

    lyrics = in_lyrics
    lyrics = lyrics.split("+")
    for ly in lyrics:
        ly = ly.split('\n')
        for line in ly:
            if ':' not in line:
                ly = re.sub("[+.\n]", '', line)
                seg = jieba.cut(line)
                lyric_lines.append([])
            for word in seg:
                if len(word) > 0 and '\u4e00' <= word <= '\u9fff' and word not in stopwords:
                    word_list.append(word)
                    lyric_lines[-1].append(word) # 一首歌一个list

    words = dict(Counter(word_list).most_common(50))

    relationships = {}
    # print(lyric_lines)
    # explore relationships
    for lyric in lyric_lines:
        for wd1 in lyric:
            for wd2 in lyric:
                if words.get(wd1) is not None and words.get(wd2) is not None:
                    if wd1 == wd2:
                        continue
                    if relationships.get(wd1) is None:
                        relationships[wd1] = {wd2: 1}
                    elif relationships[wd1].get(wd2) is None:
                        relationships[wd1][wd2] = 1
                    else:
                        relationships[wd1][wd2] = relationships[wd1][wd2] + 1
    # print(relationships)
    relationship = []
    id_ = 0
    for key, value in relationships.items():
        for key_sub, value_sub in value.items():
            dic = {"id": str(id_), "source": key, "target": key_sub, "size": value_sub}
            relationship.append(dic)
            id_ += 1
    word = []

    x = randint(1,100)
    y = randint(1,100)
    for key, value in words.items():
        dic = {"id": key, "label": key, "size": value, "x": x, "y": y}
        word.append(dic)
    read = {"nodes": word, "edges": relationship}

    # output
    json_data = json.dumps(read)
    with codecs.open("ERG3010_project/static/file.json", "w", "utf-8") as f:
        f.write(json_data)