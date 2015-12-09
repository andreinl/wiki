# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'XBVhs30wecyg67sdc'
TITLE = 'Wiki'  # Title Optional

CONTENT_DIR = 'content'
USERS_DIR = '.'

MAIL_USERNAME = 'info@xxxx.com'
MAIL_PASSWORD = 'xxxxxxx'
MAIL_DEFAULT_SENDER = '"Sender" <noreply@xxxx.com>'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_DEBUG = True
# MAIL_SUPPRESS_SEND = False
# TESTING = False

ADMINS = []
admin1 = '"Admin One" <admin@test.com'
admin2 = os.getenv('ADMIN2', '')
admin3 = os.getenv('ADMIN3', '')
admin4 = os.getenv('ADMIN4', '')
if admin1:
    ADMINS.append(admin1)
if admin2:
    ADMINS.append(admin2)
if admin3:
    ADMINS.append(admin3)
if admin4:
    ADMINS.append(admin4)

APP_NAME = "Wiki"

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_AFTER_LOGIN_ENDPOINT = 'blue_wiki.home'
USER_AFTER_LOGOUT_ENDPOINT = 'blue_wiki.home'

USER_ENABLE_CHANGE_USERNAME = True
USER_ENABLE_REGISTRATION = True
USER_ENABLE_RETYPE_PASSWORD = False
