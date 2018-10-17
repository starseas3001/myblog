# -*- coding: utf-8 -*-
import os
import json
import uuid
import random
from datetime import datetime
from functools import wraps

from flask import render_template, redirect, url_for, flash, session, request, jsonify
from flask_mail import Mail, Message

from app import db, app, MY_EMAIL, BASE_DIR
from . import utils
from app.models import VerfiyCode, Admin

# 检查登录状态
def login_ctrl(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)

    return decorated_function


# 文件重命名
def rename_file(filename):

    name_list = os.path.splitext(filename)
    filename = datetime.now().strftime('%Y%m%d%H%M%S')+str(uuid.uuid4().hex)+name_list[-1]

    return filename


# 自定定义过虑器:切片
@app.template_filter('sliceup')
def sliceup(value, args):
    """
    对请求路径进行切片
    :param value: reqeust path
    :param args: slice num
    :return: path
    """
    return  value[:args]


# 自定定义过虑器:时间格式化
@app.template_filter('date')
def date(value):
    strtime = value.strftime('%Y-%m-%d')

    return strtime

# 随机选取图片
def get_image():
    path = os.path.join(BASE_DIR, 'app/static/user_images')
    image_list = os.listdir(path)
    random_num = random.randint(0, len(image_list))
    image = image_list[random_num-1]

    return image

# 随机产生六位数验证码
def generate_code():
    str_num = '1234567890'
    code = ''
    for i in range(6):
        num = random.randint(0, 9)
        random_num = str_num[num]
        code += random_num

    return code

# 发送邮箱验证码
@utils.route('/sendCode/', methods=['GET', 'POST'])
def send_code():
    email = request.values['email']
    has_email = Admin.query.filter_by(email=email).first()
    if has_email:
        code = generate_code()
        mail = Mail(app)
        msg = Message(
            subject="个人博客邮箱验证码", sender=MY_EMAIL,
            recipients=[email]
        )
        msg.html = '【Panson的博客】您本次找回密码的邮箱验证码为{0}'.format(code)
        mail.send(msg)
        verify_code = VerfiyCode(email=email, code=code)
        db.session.add(verify_code)
        db.session.commit()

        return jsonify({'status':1})

    return jsonify({'status':0})

