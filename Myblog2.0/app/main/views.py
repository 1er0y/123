# coding:utf-8
from manage import db
from datetime import datetime
# import flask_login
from flask import render_template, abort, redirect, url_for, request
from flask.ext.login import login_required
from flask.ext.principal import Permission
from ..models import User, Post, Comment,Board
from .forms import PostForm, CommentForm,BoardForm
from . import main
from flask_login import current_user


@main.route('/')
def index():
    return render_template('index.html', title=u'欢迎来到我的博客')

@main.route('/wechat')
def wechat():
    return render_template('wechat.html')

@main.route('/board', methods=['GET','POST'])
def boards():
    page_index = request.args.get('page', 1, type=int)
    form = BoardForm()
    query = Board.query.order_by(Board.creater.desc())
    pagination = query.paginate(page_index, per_page=5, error_out=False)
    boards = pagination.items
    title = u'留言板'
    if form.validate_on_submit():
        board = Board(body = u'{}'.format(form.body.data))
        db.session.add(board)
        db.session.commit()
        return redirect(url_for('main.boards'))
    return render_template('board.html',form=form,title =title,boards=boards,pagination=pagination)


@main.route('/blog')
def blog():
    page_index = request.args.get('page', 1, type=int)
    query = Post.query.order_by(Post.timestamp.desc())
    pagination = query.paginate(page_index, per_page=5, error_out=False)
    posts = pagination.items
    return render_template('blog.html', title=u'个人博客', posts=posts, pagination=pagination)

@main.route('/aboutme')
def aboutme():
    title = u'关于我'
    return render_template('aboutme.html',
                           title=title)


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comments = Comment(body=form.body.data,
                           post_id=post.id)
        db.session.add(comments)
        db.session.commit()
    return render_template('post/detail.html',
                           form=form,
                           title=post.title,
                           post=post)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()

    if id==0:
        post = Post(author_id=current_user)
    else:
        post = Post.query.filter_by(id=id).first()
    # print post
       # form.body.data = post.body
    if form.validate_on_submit():
        post = Post()
        post.body = form.body.data
        post.title = form.title.data
        post.author_id = current_user.id
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    title = u'添加文章'
    if id > 0:
        title = u'编辑'

    return render_template('post/edit.html',
                       form=form,
                       title=title,
                       post=post)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.errorhandler(404)
def page_not_found(errors):
    return render_template('404.html'), 404


@main.errorhandler(500)
def inter_server_error(errors):
    return render_template('500.html'), 500

@main.route('/nowtime')
def now_time():
    title = u'现在时间'
    return render_template('nowtime.html',
                           current_time=datetime.utcnow(),
                           title=title)


@main.route('/secret')
@login_required
def secret():
    if (current_user.is_authenticated):
        print "false"
    else:
        print "true"
    return render_template('secter.html')
