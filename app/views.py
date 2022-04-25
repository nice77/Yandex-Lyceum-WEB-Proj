from flask import render_template, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, login_manager, db
from .models import User, Post, Follows, Comment
from .forms import *
from werkzeug.security import generate_password_hash
from base64 import b64encode


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    reg = RegisterForm()
    if reg.validate_on_submit():
        data = reg.data
        to_add = User(name=data['name'], nickname=data['nickname'],
                      email=data['email'], hashed_password=generate_password_hash(data['password'], 'sha256'))
        db.session.add(to_add)
        db.session.commit()
        return redirect('/')
    return render_template('register.html', title='Authorization', form=reg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.login.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            return render_template('login.html', message='Invalid data', form=form)
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', title='Authorization', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title=current_user.name, db=Follows, posts=Post)


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    post = PostMaker()
    if post.validate_on_submit():
        data = post.data
        nme = data['photo'].filename.split('.')[-1]
        to_add = Post(user=current_user.id,
                      data=data['photo'].read(),
                      dtype=nme,
                      text=data['text'])
        to_add.data = b64encode(bytes(to_add.data)).decode('utf-8')
        db.session.add(to_add)
        db.session.commit()
        return redirect('/')
    return render_template('new_post.html', title='Create a post', form=post)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/find_users/<name>')
def finder(name):
    return render_template('find_users.html', title='Searching for matches', db=User, name=name)


@app.route('/other_user/<int:user_id>')
def other_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('other_user.html', db=Follows, title=user.nickname, user=user, posts=Post, user_id=user_id)


@app.route('/subscribe/<int:user_id>')
def subscribe(user_id):
    to_add = Follows(account=user_id, followee=current_user.id)
    db.session.add(to_add)
    db.session.commit()
    return redirect(f'/other_user/{user_id}')


@app.route('/unsubscribe/<int:user_id>')
def unsubscribe(user_id):
    to_find = Follows.query.filter_by(followee=current_user.id, account=user_id).first()
    db.session.delete(to_find)
    db.session.commit()
    return redirect(f'/other_user/{user_id}')


@app.route('/change_avatar', methods=['GET', 'POST'])
def changer():
    changer = AvtarChanger()
    if changer.validate_on_submit():
        data = changer.data
        nme = data['photo'].filename.split('.')[-1]
        current_user.avatar = b64encode(bytes(data['photo'].read())).decode('utf-8')
        current_user.avatar_dtype = nme
        db.session.commit()
        return redirect('/profile')
    return render_template('change.html', form=changer)


@app.route('/add_comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def commentator(post_id):
    comment = CommentAdder()
    if comment.validate_on_submit():
        data = comment.data
        to_add = Comment(text=data['text'], post_id=post_id, user_id=current_user.id)
        db.session.add(to_add)
        db.session.commit()
        return redirect(f'/add_comment/{post_id}')
    post = Post.query.filter_by(id=post_id).first()
    return render_template('write_comment.html', form=comment, title='Write a comment', post=post, db=User,
                           comments=Comment, post_id=post_id)


@app.route('/')
def base():
    if current_user.is_authenticated:
        follows = Follows.query.filter_by(followee=current_user.id).all()
        posts = db.session.query(Post).filter(Post.user.in_(list(map(lambda x: x.account, follows)))).all()
        return render_template('main_page.html', posts=posts, db=User)
    return render_template('non_registered_main.html', title='Main')