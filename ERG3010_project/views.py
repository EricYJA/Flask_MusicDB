# -*- coding: utf-8 -*-

from flask import redirect, url_for, render_template, request, make_response
from ERG3010_project.myGenerator.posterGenerator import gen_poster
from ERG3010_project.myGenerator.wordcloud import gen_lyrics_wordcloud
from ERG3010_project import app
from ERG3010_project.models import Singer, Song, Sing
from ERG3010_project.song_list_generator import html_generate
from ERG3010_project.lyrics_html_generator import lyrics_html_generate


def return_img_stream(img_local_path):
    import base64
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream


@app.route('/', methods=['GET'])
def index():
    # This is for the error handing
    error = request.args.get('error')
    if str(error) == "1":
        return render_template("index.html", error="Illegal Character")
    elif str(error) == "2":
        return render_template("index.html", error="Name does not exist")
    elif str(error) == "3":
        return render_template("index.html", error="Invalid song name")
    else:
        return render_template("index.html", error=" ")


@app.route('/singer', methods=['GET', 'POST'])
def singer():

    # this is for the error handling for invalid character
    name = request.args.get('singer_name')
    if ("'" in name) or ("--" in name) or (";" in name) or (")" in name) or ("(" in name):
        return redirect(url_for('index', error="1"))

    # this is for error handling for un-find name -> ORM query used
    singer_list = Singer.query.filter(Singer.singer_name == name).all()
    if len(singer_list) == 0:
        return redirect(url_for('index', error="2"))

    # this is for the word cloud generation / the dynamic generation of the song name
    sings_list = Sing.query.filter(Sing.singer_singer_id == singer_list[0].singer_id).all()
    total_lyrics = ""
    song_id_list = []
    song_name_list = []
    for i in range(len(sings_list)):
        # for the word cloud
        local_songs = Song.query.filter(Song.song_id == sings_list[i].song_song_id).all()
        total_lyrics = total_lyrics + "+" + str(local_songs[0].lyrics)

        # for the generation of front end
        song_id_list.append(str(local_songs[0].song_id))
        song_name_list.append(str(local_songs[0].song_name))

    # generate wordcloud
    total_lyrics.strip("+")
    gen_lyrics_wordcloud(total_lyrics, str(singer_list[0].singer_name))
    cloud_addr = "ERG3010_project/static/lyricsCloud" + str(singer_list[0].singer_name) + ".png"

    # generate song_list.html
    html_generate(song_name_list, song_id_list)

    return render_template("singer.html", singer_name=name)


@app.route('/song_list.html')
def song_list():
    return render_template("song_list.html")


@app.route('/song/<song_name>', methods=['GET', 'POST'])
def song(song_name):
    list_songs = Song.query.filter(Song.song_name == str(song_name)).all()
    if len(list_songs) == 0:
        return redirect(url_for('index', error="3"))

    # specify the song information
    s_id = list_songs[0].song_id
    s_lyrics = list_songs[0].lyrics

    # generate the html file
    print(s_lyrics)
    lyrics_html_generate(str(s_lyrics))

    list_sing = Sing.query.filter(Sing.song_song_id == s_id).all()
    list_singer = Singer.query.filter(Singer.singer_id == list_sing[0].singer_singer_id).all()

    # find the singer name and the lyrics made by the user
    singer_name = list_singer[0].singer_name
    in_lyrics = request.args.get('lyrics')

    if in_lyrics is not None:
        gen_poster(list_songs[0].song_id, song_name, in_lyrics)
        file_path = "../static/posters/" + str(song_name) + ".png"
        # img_stream = return_img_stream(file_path)
        return render_template("song.html", song=song_name, singer=singer_name, img_stream=file_path, song_id=s_id)
    return render_template("song.html", song=song_name, singer=singer_name, song_id=s_id)


@app.route('/song/lyrics.html')
def lyrics():
    return render_template("lyrics.html")
