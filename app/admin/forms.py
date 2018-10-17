# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models import Admin


class LoginForm(FlaskForm):
    """后台登录表单"""
    account = StringField(
        label='账号', validators=[DataRequired('请输入账号')],
        description='账号',
        render_kw={
            'class': 'input100',
            'placeholder': '请输入用户名',
            #'required': 'require'
        }
    )

    pwd = PasswordField(
        label='密码', validators=[DataRequired('请输入密码')],
        description='密码',
        render_kw={
            'class': 'input100',
            'placeholder': '请输入密码',
            'required': 'required',
        }
    )

    submit = SubmitField(
        label='登录',
        render_kw={
            'class': 'login100-form-btn',
        }
    )

    def validate_account(self, field):
        """查询用户名"""
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在！")



