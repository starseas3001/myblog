# -*- coding: utf-8 -*-
from app import app, db

from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from app.models import Admin, Article, Comment, VerfiyCode, GuestBook, AccessLog

migrate = Migrate(app, db)
manage = Manager(app)

if __name__ == '__main__':

    app.run()
