from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, FileField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    login = EmailField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Enter')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat password')
    name = StringField('Name')
    nickname = StringField("Nickname")
    submit = SubmitField('Register!')


class PostMaker(FlaskForm):
    photo = FileField('Photo')
    text = StringField('Description')
    submit = SubmitField('Create a post!')


class AvtarChanger(FlaskForm):
    photo = FileField('Photo')
    submit = SubmitField('Change the avatar!')


class CommentAdder(FlaskForm):
    text = StringField('Your Comment')
    submit = SubmitField('Add a comment!')