'''

Get data from NetEase Cloud website

'''

import json
import requests
import re
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random


# ------------------------------------------


class NetEase():

    cookies_filename = "netease_cookies.json"

    def __init__(self):
        self.headers = {
            'Host': 'music.163.com',
            'Connection': 'keep-alive',
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Referer': 'http://music.163.com/',
            "User-Agent": 'ERG3010_project/chromedriver'
            # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        self.cookies = dict(appver="1.2.1", os="osx")

    def show_progress(self, response):
        content = bytes()
        total_size = response.headers.get('content-length')
        if total_size is None:
            content = response.content
            return content
        else:
            total_size = int(total_size)
            bytes_so_far = 0

            for chunk in response.iter_content():
                content += chunk
                bytes_so_far += len(chunk)
                progress = round(bytes_so_far * 1.0 / total_size * 100)
                self.signal_load_progress.emit(progress)
            return content

    def http_request(self, method, action, query=None, urlencoded=None, callback=None, timeout=1):
        res = None
        if method == "GET":
            res = requests.get(action, headers=self.headers, cookies=self.cookies, timeout=timeout)
        content = self.show_progress(res)
        content_str = content.decode('utf-8')
        content_dict = json.loads(content_str)
        return content_dict

    def song_detail(self, sid):
        action = 'http://music.163.com/api/song/detail?ids=%5B' + str(sid) + '%5D'
        res_data = self.http_request('GET', action)
        return res_data['songs'][0]

    def get_lyric_by_musicid(self, mid):
        # 此API必须使用POST方式才能正确返回，否则提示“illegal request”
        url = 'http://music.163.com/api/song/lyric?id=' + str(mid) + '&lv=1&kv=1&tv=-1'
        return self.http_request('POST', url)

    def clean_lyric(self, lrc):
        r = []
        is_empty = False
        for line in lrc.strip().split('\n'):
            line = line.strip()
            if not is_empty:
                r.append(line)
                if line == '':
                    is_empty = True
            else:
                if line != '':
                    r.append(line)
                    is_empty = False
        return '\n'.join(r)


class Song(object):
    def __init__(self, uid):
        self.id = uid
        self.song_lrc = ''
        self.song_id = uid
        self.song_name = ''
        self.song_img = ''

    def get_lrc(self, random_line):
        uid = self.id
        netease = NetEase()
        song = netease.song_detail(uid)
        self.song_name = song['name'].strip()
        self.song_id = uid
        self.song_img = song["album"]["blurPicUrl"]


    def create_img(self, pic_style):
        if pic_style == 1:
            Img().save(self.song_name, self.song_lrc, self.song_img)


class Img():

    def __init__(self, save_dir=None):
        self.save_dir = "ERG3010_project/static/posters"

        self.font_family = 'ERG3010_project/myGenerator/STFANGSO.TTF'
        self.font_size = 30 # 字体大小
        self.line_space = 30 # 行间隔大小
        self.word_space = 5
        self.share_img_width = 640
        self.padding = 50
        self.song_name_space = 50
        self.banner_space = 60
        self.text_color = '#767676'

        self.netease_banner = u'@FROM BERILIA MUSIC'
        self.netease_banner_color = '#D3D7D9'
        self.netease_banner_size = 20
        self.netease_icon = 'ERG3010_project/myGenerator/icon.png'
        self.icon_width = 25

        self.style2_margin = 50
        self.style2_padding = 30
        self.style2_line_width = 2
        self.style2_quote_width = 30
        self.quote_icon = 'quote.png'

        if self.save_dir is not None:
            try:
                os.mkdir(self.save_dir)
            except:
                pass

    def save(self, name, lrc, img_url):
        lyric_font = ImageFont.truetype(self.font_family, self.font_size)
        banner_font = ImageFont.truetype(self.font_family, self.netease_banner_size)
        lyric_w, lyric_h = ImageDraw.Draw(Image.new(mode='RGB', size=(1, 1))).textsize(str(lrc), font=lyric_font, spacing=self.line_space)

        padding = self.padding
        w = self.share_img_width

        album_img = None
        if img_url.startswith('http'):
            raw_img = requests.get(img_url)
            album_img = Image.open(BytesIO(raw_img.content))
        else:
            album_img = Image.open(img_url)

        iw, ih = album_img.size
        album_h = ih *  w // iw

        h = album_h + padding + lyric_h + self.song_name_space + \
            self.font_size + self.banner_space + self.netease_banner_size + padding

        resized_album = album_img.resize((w, album_h), resample=3)
        icon = Image.open(self.netease_icon).resize((self.icon_width, self.icon_width), resample=3)

        out_img = Image.new(mode='RGB', size=(w, h), color=(255, 255, 255))
        draw = ImageDraw.Draw(out_img)

        # 添加封面
        out_img.paste(resized_album, (0, 0))

        # 添加文字
        draw.text((padding, album_h + padding), str(lrc), font=lyric_font, fill=self.text_color, spacing=self.line_space)

        # Python中字符串类型分为byte string 和 unicode string两种，'——'为中文标点byte string，需转换为unicode string
        y_song_name = album_h + padding + lyric_h + self.song_name_space
        # song_name = unicode('—— 「', "utf-8") + name + unicode('」', "utf-8")
        song_name = u'—— 「' + name + u'」'
        sw, sh = draw.textsize(song_name, font=lyric_font)
        draw.text((w - padding - sw, y_song_name), song_name, font=lyric_font, fill=self.text_color)

        # 添加网易标签
        y_netease_banner = h - padding - self.netease_banner_size
        out_img.paste(icon, (padding, y_netease_banner - 2))
        draw.text((padding + self.icon_width + 5, y_netease_banner), self.netease_banner, font=banner_font, fill=self.netease_banner_color)

        img_save_path = ''
        if self.save_dir is not None:
            img_save_path = self.save_dir
            print(img_save_path)
        print(out_img)
        out_img.save(img_save_path + "/" + name + '.png')



def unicode_str(s):
    try:
        t = s.unicode('utf-8')
        return t
    except:
        return s


def gen_poster(in_id, in_song_name, in_song_lyrics):

    '''   -sid: 186436
      -pic_style: 1/2/3

      -random_line: #
      -line_range: 1,3,5-9

      -img_file: image file loaded by users
      -text: text written by users
      -name: a name of text written by users
    '''

    # download
    sid = in_id  # song_id
    pic_style = 1
    random_line = 0  # number of lines of poster
    text = in_song_lyrics
    name = in_song_name

    text = '\n'.join([line.strip() for line in text.replace('\\n','\n').split('\n')])
    text = unicode_str(text)
    song = Song(sid)
    song.song_lrc = text
    song.get_lrc(random_line)

    song.create_img(pic_style)


if __name__ == '__main__':
    # 歌词必须有换行符 好像
    gen_poster(1334667455, "幻觉动物", "侥幸 幻觉浮出 仰着感触\n窝着领悟 我们都是 被熔铸的动物")