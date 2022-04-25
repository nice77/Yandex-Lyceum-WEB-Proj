from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime as dt
import os


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    hashed_password = db.Column(db.String)
    avatar = db.Column(db.String, default=open('app/def_avatar.txt').readline())
    avatar_dtype = db.Column(db.String, default='png')

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User> {self.name, self.email, self.hashed_password}'


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String)
    dtype = db.Column(db.String)
    text = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.DateTime, default=dt.datetime.now(), nullable=False)

    def __repr__(self):
        return f'<Post> {self.id, self.user, self.dtype, self.data}'


class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.Integer, db.ForeignKey("users.id"))
    followee = db.Column(db.Integer, db.ForeignKey("users.id"))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
