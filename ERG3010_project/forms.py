from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LyricsForm(FlaskForm):
    body = TextAreaField("Lyrics you want to generate", validators=[DataRequired(), Length(1, 75)])
    submit = SubmitField("Generate Lyrics")
