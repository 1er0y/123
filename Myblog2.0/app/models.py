from app import db
from flask.ext.login import UserMixin
from datetime import datetime
from markdown import markdown
from . import login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref = 'role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password = db.Column(db.String(64),unique=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'),default=3)

    posts = db.relationship('Post',backref ='author')

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.Text)
    body_html = db.Column(db.String)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow())

    comments = db.relationship('Comment',backref = 'post')
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    @staticmethod
    def on_body_change(target,value,oldvalue,inititor):
        if value is None or (value is ''):
            target.body_html=''
        else:
            target.body_html = markdown(value)

db.event.listen(Post.body,'set',Post.on_body_change)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String)
    created = db.Column(db.DateTime,index=True,default=datetime.utcnow())
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))