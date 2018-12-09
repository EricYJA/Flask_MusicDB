import jieba
import re
from collections import Counter
from QcloudApi.qcloudapi import QcloudApi
from pyecharts import Gauge
from pyecharts import Liquid, Polar, Radar

def lyricGenerate():
    lyrics_list = []
    with open("D:\\Academic_work\\01_ERG3010\\Project\\lyricsAnalysis3\\lijianlyrics2.txt", 'r', encoding = 'utf-8') as f:
        for line in f:
            line = f.readline()
            if ':' not in line and len(line) > 0:
                line = re.sub("[+.\n]", '', line)
                lyrics_list.append(line)

    lyric = " ".join(lyrics_list)
    return lyric

# 对一首歌的分析
# 从数据库抓取
def Analysis(lyric):
    module = 'wenzhi'
    action = 'TextSentiment'
    config = {
        'Region': 'sz',
        'secretId': 'AKIDBHCx49tBzc5eTIA6kFoddWUXQDbpq7JQ',
        'secretKey': 'gCXHsHFD1eDjJgT7b3TkI4fu1wnjDYbU',
        'method': 'post',
    }
    params = {
        'content': lyric,  # 需要分析的歌词
        'type': 4,
    }
    try:
        service = QcloudApi(module, config)
        result = service.call(action, params)
    except Exception as e:
        import traceback
        print('traceback.format_exc():\n%s' % traceback.format_exc())

    # 图1
    result = eval(str(result,encoding = "utf-8"))
    negative_value = round(result['negative'], 4)
    positive_value = round(result['positive'], 4)
    gauge = Gauge("Sentiment",
                   background_color = None, 
                   title_color = "#274C77",
                   title_text_size = 20)
    gauge.add("Probability of Negative Property", "Negative", value = negative_value*100,
               legend_text_color = "#274C77",
               legend_text_size = 15,
               lable_color = ["E7ECEF", "#274C77", "FB6107"])
    
    # gauge.show_config()
    gauge.render('gauge.html')

    # 图2
    liquid2 =Liquid(title = "Probability of Positive Property",
                    title_pos = 'center')
    liquid2.add("Probability of Positive Property", [positive_value, 0.5, 0.4, 0.3], 
                is_liquid_outline_show=False,
                shape = "pin",
                liquid_color = ["E7ECEF", "#274C77", "FB6107"])
    # liquid2.show_config()
    liquid2.render('pin.html')

lyric = lyricGenerate()
Analysis(lyric)