from os import walk, path
import re

import jieba
import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image

work_path = 'ERG3010_project/static/lyricsCloud'
image_name = 'ERG3010_project/myGenerator/mask.png'
font_name = 'ERG3010_project/myGenerator/STFANGSO.TTF'


def generate_wordcloud(data, singer_name):
    font_path = font_name # 字体

    color_mask = np.array(Image.open(image_name))  # the shape of the world cloud

    max_words = 2000
    max_font_size = 75

    cloud = WordCloud(font_path=font_path, max_words=max_words, width=3000, height=2000, mask=color_mask,
                      max_font_size=max_font_size, background_color='white',
                      contour_width=3, contour_color='steelblue', random_state=42)

    wordcloud = cloud.generate(text=data)       # data should be string

    image_colors = ImageColorGenerator(color_mask)

    wordcloud.recolor(color_func=image_colors)
    wordcloud.to_file(path.join(work_path, '{0}.png'.format(singer_name)))     # save to file

def seg(data_file):
    f = open("ERG3010_project/myGenerator/stopwords.txt", 'r', encoding = 'utf-8-sig')
    stopwords = f.readlines()
    data = []
    lyrics = data_file.split("+")
    for lyr in lyrics:
        lyr = lyr.split("\n")
        for line in lyr:
            if ":" not in line:
                line = re.sub("[.\n]", ' ', line)
                # line = " ".join(line)
                data.append(line)
    data = " ".join(data)

    words_data = []
    local_words = jieba.cut(data, cut_all=False)       # cut the data
    for word in local_words:
        if len(word) > 1 and word != '\r\n' and word not in stopwords:
            words_data.append(word)

    return ' '.join(words_data)


def gen_lyrics_wordcloud(data, singer_name):
    in_data = seg(data)
    generate_wordcloud(in_data, singer_name)
