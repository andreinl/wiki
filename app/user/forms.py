from flask.ext.wtf import Form
from wtforms import (BooleanField, TextField, TextAreaField, PasswordField)
from wtforms.validators import (InputRequired, ValidationError)

from app import app
from user import UserManager

users = UserManager(app.config.get('USERS_DIR'))


class LoginForm(Form):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = users.get_user(field.data)
        if not user:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')
