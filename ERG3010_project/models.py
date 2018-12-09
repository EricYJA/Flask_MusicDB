from ERG3010_project import db


class Singer(db.Model):
    __name__ = "singer"
    singer_id = db.Column(db.String(15), primary_key=True)
    gender = db.Column(db.String(6))
    region = db.Column(db.String(45))
    age = db.Column(db.String(11))
    singer_name = db.Column(db.String(45))


class Song(db.Model):
    __name__ = "song"
    song_id = db.Column(db.String(15), primary_key=True)
    song_name = db.Column(db.String(250))
    lyrics = db.Column(db.Text)
    play_times = db.Column(db.String(11))


class Sing(db.Model):
    __name__ = "sing"
    song_id = db.Column(db.String(15), primary_key=True)
    singer_id = db.Column(db.String(15), db.ForeignKey('singer.singer_id'))  # , db.ForeignKey('singer.singer_id')
