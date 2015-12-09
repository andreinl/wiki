# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask_user.forms import RegisterForm
from flask_wtf import Form
from wtforms import StringField, SelectMultipleField, SubmitField, validators


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    # first_name = StringField('First name', validators=[
    #     validators.DataRequired('First name is required')])
    # last_name = StringField('Last name', validators=[
    #     validators.DataRequired('Last name is required')])
    email = StringField('Email', validators=[
        validators.DataRequired('Email is required')])


# Define the User profile form
class UserProfileForm(Form):
    # first_name = StringField('First name', validators=[
    #     validators.DataRequired('First name is required')])
    # last_name = StringField('Last name', validators=[
    #     validators.DataRequired('Last name is required')])
    username = StringField('Login name')
    first_name = StringField('First name')
    last_name = StringField('Last name')

    # role = SelectMultipleField('Role')
    role = SelectMultipleField('Role', coerce=int)

    email = StringField('Email', validators=[
        validators.DataRequired('Email is required')])
    submit = SubmitField('Save')


class RoleForm(Form):
    name = StringField('Role name')
    label = StringField('Label')
    submit = SubmitField('Save')
