# coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Required,Length

class LoginForm(Form):
    name = StringField(label=u'报上名来',validators=[Required(),                                         Length(1,64)])
    password = PasswordField(label=u'密码',validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(label=u'登录')

class RegisterForm(Form):
    username = StringField(label=u'用户名',validators=[Required()])
    password = PasswordField(label=u'密码',validators=[Required()])
    submit = SubmitField(label=u'马上注册')