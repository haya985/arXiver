__author__ = 'dave'

import os
from flask import Flask,url_for,request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
from config import ARTICLES_PER_PAGE
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from flask.ext.restful import Api
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask(__name__, static_url_path='')
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app,os.path.join(basedir,'tmp'))

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

if not app.debug:
    import logging
    # from logging.handlers import SMTPHandler
    # credentials = None
    # if MAIL_USERNAME or MAIL_PASSWORD:
    #     credentials = (MAIL_USERNAME,MAIL_PASSWORD)
    # mail_handler = SMTPHandler((MAIL_SERVER,MAIL_PORT),
    #     'no-reply@'+MAIL_SERVER,ADMINS,'microblog failure', credentials)
    # mail_handler.setLevel(logging.ERROR)
    # app.logger.addHandler(mail_handler)

    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/' + __name__ + '.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.info(__name__ + ' startup')
from arxiver import views, models  #, apis

