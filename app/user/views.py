from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
from app import loginmanager
from app import app
from forms import LoginForm

from user import UserManager

from flask import Blueprint

blue_user = Blueprint('blue_user', __name__, template_folder='templates', url_prefix='/user')

users = UserManager(app.config.get('USERS_DIR'))


@loginmanager.user_loader
def load_user(name):
    return users.get_user(name)


@blue_user.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('index'))
    return render_template('login.html', form=form)


@blue_user.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('index'))


@blue_user.route('/user/')
def user_index():
    pass


@blue_user.route('/user/create/')
def user_create():
    pass


@blue_user.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@blue_user.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass
