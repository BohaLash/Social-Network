from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, SelectField, IntegerField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from social_network.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    login = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=32)])
    gender = RadioField('Gender', choices=[(0, 'Male'), (1, 'Female')])
    city = StringField('City', validators=[
        DataRequired(), Length(min=2, max=64)])
    born = IntegerField("Year of Birth")
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Username is taken already. Please choose a different one.')


class EditForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=2, max=32)])
    gender = RadioField('Gender', choices=[(0, 'Male'), (1, 'Female')])
    city = StringField('City', validators=[
        DataRequired(), Length(min=2, max=64)])
    born = IntegerField("Year of Birth")
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def __init__(self):
        super(EditForm, self).__init__()
        self.name.data = current_user.name
        self.gender.data = str(int(current_user.gender))
        self.city.data = current_user.city
        self.born.data = current_user.born


# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', validators=[
#                                      DataRequired(), EqualTo('password')])
#     submit = SubmitField('Reset Password')
