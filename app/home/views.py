# -*- coding: utf-8 -*-
from datetime import datetime

from flask import render_template, request, jsonify, redirect, url_for

from app import db
from app.home import home
from app.models import Comment, GuestBook
from app.utils.app_utils import get_image
from app.models import Article, AccessLog


# 首页
@home.route('/')
def index():
    page = request.args.get('page', 1)
    all_articles = Article.query.order_by(Article.add_time.desc())
    all_articles = all_articles.paginate(page=int(page), per_page=5)
    ip = request.remote_addr
    log = AccessLog(ip=ip)
    db.session.add(log)
    db.session.commit()

    return render_template('home/index.html', all_articles=all_articles)


# 文章详情
@home.route('/detail')
def detail():
    id = request.args.get('article', '')
    if id:
        article = Article.query.filter_by(id=int(id)).first()
        article.click_nums += 1
        db.session.add(article)
        db.session.commit()
        prev_article = Article.query.filter_by(id=int(id)+1).first()
        next_article = Article.query.filter_by(id=int(id)-1).first()

        all_comments = Comment.query.filter_by(article_id=article.id).order_by(Comment.add_time.desc())
        comment_nums = all_comments.count()


        return render_template(
            'home/detail.html', article=article, prev_article=prev_article,
            next_article=next_article, all_comments=all_comments,
            comment_nums=comment_nums
        )
    return redirect(url_for('home.index'))


# 留言页面
@home.route('/leavemsg')
def leave_msg():
    page = request.args.get('page', 1)
    all_comments = GuestBook.query.order_by(GuestBook.add_time.desc())
    comment_nums = all_comments.count()
    # 分页
    all_comments = all_comments.paginate(page=int(page), per_page=10)
    return render_template(
        'home/gustbook.html', all_comments=all_comments,comment_nums=comment_nums
    )


# 添加评论/留言
@home.route('/addcomment', methods=['GET', 'POST'])
def add_comment():
    article_id = request.values.get('article_id','')
    nick_name = request.values['author']
    email = request.values['email']
    content = request.values['comment']
    head_image = get_image()
    strtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 添加评论
    if article_id:
        article = Article.query.filter_by(id=int(article_id)).first()
        comment = Comment(
            nick_name=nick_name, email=email, content=content, head_image=head_image,
            article_id = article.id
        )

        if article:
            db.session.add(comment)
            db.session.commit()

            return jsonify({'code': 1, 'head_image': head_image, 'strtime':strtime})
        return jsonify({'code': 2, 'msg':'评论失败'})
    # 添加留言
    guest_book = GuestBook(
        nick_name=nick_name, email=email, content=content, head_image=head_image,
    )
    db.session.add(guest_book)
    db.session.commit()
    return jsonify({'code':1, 'head_image':head_image, 'strtime':strtime})

