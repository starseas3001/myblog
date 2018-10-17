# -*- coding: utf-8 -*-
import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
# from flask_migrate import Migrate

import pymysql

app = Flask(__name__)
app.debug = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:******@127.0.0.1:3306/myblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '******'
CSRFProtect(app)
# 邮箱配置
app.config.update(
    MAIL_SERVER='smtp.sina.com',
    MAIL_PORT=25,
    MAIL_USE_SSL=False,
    EMAIL_USE_TLS = False,
    MAIL_USERNAME='starseas3001',
    MAIL_PASSWORD = '******'
)
# 文件上传路径
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app.config['UP_DIR'] = os.path.join(BASE_DIR, "app/static/uploads/")

db = SQLAlchemy(app)
# migrate = Migrate(app, db)

MY_EMAIL = 'starseas3001@sina.com'

# flask日志
log_filename = os.path.join(BASE_DIR, 'logs/flask.log')
handler = logging.FileHandler(log_filename, encoding='UTF-8')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
from app.utils import utils as utils_blueprint

# 注册蓝图
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(utils_blueprint, url_prefix='/utils')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
