# Readme

## Preface

I needed a wiki that just uses plain markdown files as backend and is written in Flask. Fortunately I find https://github.com/alexex/wiki. Unfortunately all the code was inside the same file, so I transformed it in a regular Flask project that uses Blueprints. It also makes this project more useful, because Blueprint can be reused in other projects. Users authentication is present, it uses superior Flask-User module.

## Features

* Markdown Syntax Editing
* Tags
* Regex Search
* Random URLs
* Web Editor
* Pages can also be edited manually, possible uses are:
	* use the cli
	* use your favorite editor
	* sync with dropbox
	* and many more
* easily themable
* user registration and authentication
* only users with *writer* role can create/edit/delete pages

## Setup
Just clone this repository, cd into it, run `pip install -r requirements.txt`
and edit a `config.py` in the root directory.

Initialize user management database:

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade

## Start
Afterwards just run the app which will run the development server in debug
mode. 

    python run.py runserver -d -r
    
Or with gunicorn:
	
	gunicorn run:app

You can install `setproctitle` with pip to get meaningful process names.

## Theming
The templates are based on jinja2. I used
[bootstrap](http://twitter.github.com/bootstrap/) for the design.
If you want to change the overall design, you should edit `templates/base.html`
and/or `static/bootstrap.css`. If you do not like specific parts of the site,
it should be fairly easy to find the equivalent template and edit it.

## Users
The first user that registers became *admin*. This will work only if you use my customized Flask-User module. To be able to write an article you need to create *writer* role and add role to created user. To manage users go to 

    http://localhost:5000/user/manage
    

