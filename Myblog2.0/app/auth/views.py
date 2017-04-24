# coding:utf-8
from flask import render_template, redirect, url_for,flash,request
from flask.ext.login import login_user,login_required,logout_user,current_user
from app import db
from .forms import RegisterForm,LoginForm
from app.models import User
from . import auth



@auth.route('/login',methods=['GET','POST'])
def login():
    title = u'登录'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is not None and user.password==form.password.data:
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash(u'账号或密码错误！')
    return  render_template('login.html',form=form,title=title)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'注销成功。')
    return redirect(url_for('main.index'))



@auth.route('/register',methods=['GET','POST'])
@login_required
def register():
    title = u'注册'
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash(u'注册成功！')
            user = User(username = u'{}'.format(form.username.data),
                        password = form.password.data)
            db.session.add(user)
            db.session.commit()
        #form.username.name = ''
        return redirect(url_for('auth.login'))
    return render_template('register.html',form=form,title=title)






