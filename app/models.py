# -*- coding: utf-8 -*-
from datetime import datetime

from app import db




class Admin(db.Model):
    """管理员"""
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 账号
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(30)) # 邮箱
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


class Article(db.Model):
    """文章"""
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)    # id
    title = db.Column(db.String(100), unique=True, index=True)  # 标题
    summary = db.Column(db.Text, nullable=True) # 摘要
    content = db.Column(db.Text)   # 内容
    image = db.Column(db.String(255), nullable=True)  # 图片
    click_nums = db.Column(db.BigInteger, default=0)  # 点击量
    comments = db.relationship('Comment', backref='article')    # 评论外键关联

    add_time = db.Column(db.DateTime, default=datetime.now, index=True) # 添加时间

    def __repr__(self):

        return '<Article %r>' % self.title


class Comment(db.Model):
    """文章评论"""
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(30))
    email = db.Column(db.String(20))
    content = db.Column(db.Text)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id')) # 所属文章
    head_image = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, default=datetime.now, index=True) # 添加时间

    def __repr__(self):
        return '<Comment %r>' % self.nick_name


class GuestBook(db.Model):
    """留言页留言"""
    ___tablename__ = 'guestbook'
    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(30))
    email = db.Column(db.String(20))
    content = db.Column(db.Text)
    head_image = db.Column(db.String(255))  # 头像
    add_time = db.Column(db.DateTime, default=datetime.now, index=True)  # 添加时间

    def __repr__(self):
        return '<GuestBook %r>' % self.nick_name


class VerfiyCode(db.Model):
    """邮箱验证码"""
    __tablename__ = 'verifycode'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20))
    code = db.Column(db.String(20))
    add_time = db.Column(db.DateTime, default=datetime.now, index=True)  # 添加时间

    def __repr__(self):
        return '<VerfiyCode %r>' % self.email


class AccessLog(db.Model):
    """访问日志"""
    __tablename__ = 'accesslog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))  # 访问ip
    add_time = db.Column(db.DateTime, default=datetime.now, index=True)  # 添加时间

    def __repr__(self):
        return '<AccessLog %r>' % self.ip



# if __name__ == '__main__':
#
#     from werkzeug.security import generate_password_hash
#     admin = Admin(
#         name='xxxxxx',
#         pwd=generate_password_hash('xxxxxx')
#     )
#     db.session.add(admin)
#     db.session.commit()







