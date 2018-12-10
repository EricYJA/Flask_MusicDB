from bs4 import BeautifulSoup
from selenium import webdriver
from ERG3010_project.models import Pics
import re


def get_all_album(html):
    all_li = BeautifulSoup(html,'lxml').find(id='m-song-module').find_all('li')
    albList = []
    for al in all_li:
        album_name = al.find('p',class_='dec')['title']
        album_id = str(re.findall('href="(.*?)"', str(al))).split('=')[1].split('\'')[0]
        album_date = al.find('span',class_='s-fc3').text
        album_img = deal_url(al.find('img')['src'])

        this_album = Pics()
        this_album.a_id = album_id
        this_album.a_name = album_name
        this_album.a_date = album_date
        this_album.a_url = album_img

        albList.append(this_album)
    
    return albList


def deal_url(str):
    end_pos = str.index('?')
    str = str[:end_pos]
    return str


def get(singer_id,singer_name): 
    browser = webdriver.Chrome('ERG3010_project/chromedriver')
    name_ = singer_name
    id_ = singer_id
    album_url = 'https://music.163.com/artist/album?id={}'.format(id_)
    print(name_, " ", id_)
    browser.get(album_url)
    browser.switch_to.frame('g_iframe')
    html = browser.page_source
    print("1")

    try:
        return get_all_album(html)
    except:
        print("no album\n")
        return [None]


def timeline_generator(singer_id,singer_name):
    total_abums = get(singer_id,singer_name)

    if total_abums[0] is None:
        return total_abums
    else:
        return total_abums
