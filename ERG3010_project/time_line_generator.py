import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import json


def get_html(url):
    proxy_addr = {'http': '61.135.217.7:80'}
    # 用的代理 ip，如果被封的，在http://www.xicidaili.com/换一个
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    try:
        html = requests.get(url, headers=headers, proxies=proxy_addr).text
        return html
    except BaseException:
        print('request error')
        pass


def get_all_album(html):
    all_li = BeautifulSoup(html,'lxml').find(id='m-song-module').find_all('li')
    albumnames = []
    albumids = []
    albumdates = []
    albumimgs = []
    for al in all_li:
        album_name = al.find('p',class_='dec')['title']
        album_id = str(re.findall('href="(.*?)"', str(al))).split('=')[1].split('\'')[0]
        album_date = al.find('span',class_='s-fc3').text
        album_img = deal_url(al.find('img')['src'])

        albumnames.append(album_name)
        albumids.append(album_id)
        albumdates.append(album_date)
        albumimgs.append(album_img)
    
    return albumids, albumnames, albumdates, albumimgs


def deal_url(str):
    end_pos = str.index('?')
    str = str[:end_pos]
    return str

def get(singer_id,singer_name): 
    browser = webdriver.Chrome()  
    name_ = singer_name
    id_ = singer_id
    album_url = 'https://music.163.com/artist/album?id={}'.format(id_)
    print(name_, " ", id_)
    browser.get(album_url)
    browser.switch_to.frame('g_iframe')
    html = browser.page_source
    try:         
		albumids, albumnames, albumdates, albumimgs = get_all_album(html)
    except:
        print("no album\n")
	return albumids, albumnames, albumdates, albumimgs

def timeline_generator(singer_id,singer_name):
	album_id, album_name,album_public,album_img = get(singer_id,singer_name)
	timeline_content = ""
	for i in range(len(album_id)):
		timeline_content = timeline_content + """
		<div class="album-image">
			<div id="%s" title="%s" style="background-image: url(%s);"></div>
			<h3 class="public-time">%s</h3>
		</div>
		"""
	return timeline_content
