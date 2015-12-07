from flask import Flask, render_template, flash, redirect, url_for, request, abort

from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
from flask.ext.script import Manager


"""
    Application Setup
    ~~~~~~~~~
"""

app = Flask(__name__)

app.config.from_object('config')

manager = Manager(app)

loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = 'user_login'

from app.user.views import blue_user
app.register_blueprint(blue_user)

from app.wiki.views import blue_wiki
app.register_blueprint(blue_wiki)
