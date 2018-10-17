# -*- coding: utf-8 -*-
import os
import uuid
import json
from functools import wraps
from datetime import datetime

from flask import render_template, redirect, url_for, flash, session, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from app import app
from . import admin
from .forms import LoginForm
from app.models import Admin, Article, GuestBook, Comment, VerfiyCode, AccessLog
from app import db

from app.utils.app_utils import login_ctrl, rename_file


# 后台登录
@admin.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash("密码错误", 'err')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']

        return redirect(url_for('admin.article', page=1))

    return render_template('admin/login.html', form=form)


# 后台退出
@admin.route('/logout')
@login_ctrl
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


# 文章管理列表页
@admin.route('/article')
@login_ctrl
def article():
    # 分页
    page = request.args.get('page', 1)
    all_articles = Article.query.order_by(
        Article.add_time.desc()
    )
    article_nums = all_articles.count()
    all_articles = all_articles.paginate(page=int(page), per_page=10)

    return render_template(
        'admin/article.html', all_articles=all_articles, article_nums=article_nums
    )


# 添加/编辑文章
@admin.route('/addarticle/<int:id>/')
@login_ctrl
def add_article(id=None):
    if id == 0:
        return render_template('admin/add_article.html', id=id)
    else:
        article = Article.query.filter_by(id=id).first()
        title = article.title
        summary = article.summary
        content = article.content
        image = article.image
        return render_template(
            'admin/add_article.html', title=title, summary=summary, content=content, image=image, id=id
        )


# 删除文章
@admin.route('/article/delete/', methods=['GET', 'POST'])
@login_ctrl
def del_article():
    id = request.values.get('id')
    article = Article.query.filter_by(id=id).first_or_404()
    db.session.delete(article)
    db.session.commit()

    return jsonify({'status': 1})


# 提交文章
@admin.route('/submitarticle/<int:id>/', methods=['GET', 'POST'])
@login_ctrl
def submit_article(id=None):
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    summary = request.form.get('summary', '')
    image = ''
    file = request.files.get('titlepic', '')
    if file:
        image_name = secure_filename(file.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        # 重命名
        image = rename_file(image_name)
        file.save(app.config['UP_DIR'] + image)

    if id == 0:
        article = Article(title=title, summary=summary, content=content, image=image)
        db.session.add(article)
        db.session.commit()
    else:
        article = Article.query.filter_by(id=id).first()
        article.summary = summary
        article.title = title
        article.content = content
        if image:
            article.image = image
        db.session.add(article)
        db.session.commit()
    return redirect(url_for('admin.article', page=1))


# 留言管理列表页
@admin.route('/leavemsg')
@login_ctrl
def leave_msg():
    page = request.args.get('page', 1)
    all_comments = GuestBook.query.order_by(GuestBook.add_time.desc())
    comment_nums = all_comments.count()
    all_comments = all_comments.paginate(page=int(page), per_page=10)
    return render_template(
        'admin/leave_msg.html', comment_nums=comment_nums, all_comments=all_comments
    )


# 删除留言
@admin.route('/leavemsg/delete/', methods=['GET', 'POST'])
@login_ctrl
def del_leavemsg():
    id = request.values.get('id')
    comment = GuestBook.query.filter_by(id=id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"status": 1})


# 评论管理列表页
@admin.route('/commentmanage')
@login_ctrl
def comment_manage():
    page = request.args.get('page', 1)
    all_comments = Comment.query.order_by(Comment.article_id.desc()).order_by(Comment.add_time.desc())
    comment_nums = all_comments.count()
    all_comments = all_comments.paginate(page=int(page), per_page=10)
    return render_template(
        'admin/comment.html', comment_nums=comment_nums, all_comments=all_comments
    )


# 删除评论
@admin.route('/comment/delete/', methods=['GET', 'POST'])
@login_ctrl
def del_comment():
    id = request.values.get('id')
    comment = Comment.query.filter_by(id=id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"status": 1})


# 找回密码页面
@admin.route('/findpwd/', methods=['GET', 'POST'])
def find_pwd():

    return render_template('admin/find_pwd.html')

# 修改密码、提交
@admin.route('/submitpwd/', methods=['GET', 'POST'])
def submit_pwd():
    email = request.values['email']
    verify_code = request.values['verify_code']
    password = request.values['password']
    admin = Admin.query.filter_by(email=email).first()
    if admin is None:
        # 邮箱不存在
        return jsonify({'status': 2})
    has_code = VerfiyCode.query.filter_by(email=email, code=verify_code).first()
    if has_code:
        admin.pwd = generate_password_hash(password)
        db.session.add(admin)
        db.session.commit()
        # 修改成功
        return jsonify({'status': 1})
    else:
        # 验证码错误
        return jsonify({'status': 0})


# 访问日志
@admin.route('/accesslog/')
@login_ctrl
def access_log():
    page = request.args.get('page', 1)
    all_logs = AccessLog.query.order_by(AccessLog.add_time.desc())
    log_nums = all_logs.count()
    all_logs = all_logs.paginate(page=int(page), per_page=10)
    return render_template(
        'admin/access_log.html', log_nums=log_nums, all_logs=all_logs
    )


# 删除访问日志
@admin.route('/accesslog/delete/', methods=['GET', 'POST'])
@login_ctrl
def del_accesslog():
    id = request.values.get('id')
    log = AccessLog.query.filter_by(id=id).first_or_404()
    db.session.delete(log)
    db.session.commit()
    return jsonify({"status": 1})
