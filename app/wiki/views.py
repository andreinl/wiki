from flask import render_template, flash, redirect, url_for, request
from flask_user import current_user, login_required, roles_required
from app import app
# from flask.ext.login import current_user
# from functools import wraps
# from app import loginmanager

from wiki import Wiki
from wiki import Processors
from forms import URLForm, EditorForm, SearchForm

from flask import Blueprint
blue_wiki = Blueprint('blue_wiki', __name__, template_folder='templates', url_prefix='/wiki')

wiki = Wiki(app.config.get('CONTENT_DIR'))

# def protect(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if app.config.get('PRIVATE') and not current_user.is_authenticated():
#             return loginmanager.unauthorized()
#         return f(*args, **kwargs)
#     return wrapper

"""
    Routes
    ~~~~~~
"""
import pdb

@app.route('/')
def home_i():
    pdb.set_trace()
    return redirect(url_for('blue_wiki.home'))


@blue_wiki.route('/')
def home():
    page = wiki.get('home')
    if page:
        return display('home')
    return render_template('wiki/home.html')


@blue_wiki.route('/index/')
def index():
    pages = wiki.index()
    return render_template('wiki/index.html', pages=pages)


@blue_wiki.route('/<path:url>/')
def display(url):
    page = wiki.get_or_404(url)
    return render_template('wiki/page.html', page=page)


@blue_wiki.route('/create/', methods=['GET', 'POST'])
@roles_required('writer')    # Limits access to users with the 'writer' role
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for('blue_wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('wiki/create.html', form=form)


@blue_wiki.route('/edit/<path:url>/', methods=['GET', 'POST'])
@roles_required('writer')    # Limits access to users with the 'writer' role
def edit(url):
    page = wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('blue_wiki.display', url=url))
    return render_template('wiki/editor.html', form=form, page=page)


@blue_wiki.route('/preview/', methods=['POST'])
@roles_required('writer')    # Limits access to users with the 'writer' role
def preview():
    a = request.form
    data = {}
    processed = Processors(a['body'])
    data['html'], data['body'], data['meta'] = processed.out()
    return data['html']


@blue_wiki.route('/move/<path:url>/', methods=['GET', 'POST'])
@roles_required('writer')    # Limits access to users with the 'writer' role
def move(url):
    page = wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        wiki.move(url, newurl)
        return redirect(url_for('.display', url=newurl))
    return render_template('wiki/move.html', form=form, page=page)


@blue_wiki.route('/delete/<path:url>/')
@roles_required('writer')    # Limits access to users with the 'writer' role
def delete(url):
    page = wiki.get_or_404(url)
    wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('blue_wiki.home'))


@blue_wiki.route('/tags/')
def tags():
    tags = wiki.get_tags()
    return render_template('wiki/tags.html', tags=tags)


@blue_wiki.route('/tag/<string:name>/')
def tag(name):
    tagged = wiki.index_by_tag(name)
    return render_template('wiki/tag.html', pages=tagged, tag=name)


@blue_wiki.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = wiki.search(form.term.data, form.ignore_case.data)
        return render_template('wiki/search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('wiki/search.html', form=form, search=None)


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('wiki/404.html'), 404
