from flask.ext.wtf import Form
from wtforms import (BooleanField, TextField, TextAreaField)
from wtforms.validators import (InputRequired, ValidationError)
from app import app

from wiki import Processors
from wiki import Wiki

wiki = Wiki(app.config.get('CONTENT_DIR'))

"""
    Forms
    ~~~~~
"""


class URLForm(Form):
    url = TextField('', [InputRequired()])

    def validate_url(form, field):
        if wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return Processors().clean_url(url)


class SearchForm(Form):
    term = TextField('', [InputRequired()])
    ignore_case = BooleanField(description='Ignore Case', default=app.config.get('DEFAULT_SEARCH_IGNORE_CASE', True))


class EditorForm(Form):
    title = TextField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = TextField('')
