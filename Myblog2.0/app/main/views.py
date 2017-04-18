# coding:utf-8
from manage import db
from datetime import datetime
#import flask_login
from flask import render_template,abort,redirect,url_for
from flask.ext.login import login_required
from flask.ext.principal import Permission
from ..models import User,Post
from .forms import PostForm
from . import main
from flask_login import current_user

@main.route('/')
def index():
    #form = PostForm
    posts = Post.query.all()
    # if flask_login.current_user.can(Permission.WRITE_ARTICLES) and \
    #         form.validate_on_submit():
    #     post = Post(body=form.body.data,
    #                 auther = flask_login.current_user.__get_current_object())
    #     db.session.add(post)
    #     return redirect(url_for('.index'))
    # post = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',title = u'欢迎',posts = posts)

@main.route('/nowtime')
def now_time():
    title = u'现在时间'
    return render_template('nowtime.html',
                           current_time = datetime.utcnow(),
                           title = title)

@main.route('/secret')
@login_required
def secret():
    if (current_user.is_authenticated):
        print "false"
    else:
        print "true"
    return render_template('secter.html')

@main.route('/edit',methods = ['GET','POST'])
@main.route('/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit(id=0):
    form = PostForm()
    if id is not None:
         #post = Post(author =current_user())
         print id
    # else:
    #     post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        post = Post()
        post.body = form.body.data
        post.title = form.title.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    title = u'添加文章'
    if id >0:
         title=u'编辑'

    return render_template('post/edit.html',
                           form = form,
                           title=title)

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)

@main.errorhandler(404)
def page_not_found(errors):
    return render_template('404.html'),404

@main.errorhandler(500)
def inter_server_error(errors):
    return render_template('500.html'),500