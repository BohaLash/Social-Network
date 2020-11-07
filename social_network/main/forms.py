from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from social_network.models import User


class NewPostForm(FlaskForm):
    text = TextAreaField("", default="", validators=[
        DataRequired(), Length(min=5, max=256)])
    submit = SubmitField('Publish')
