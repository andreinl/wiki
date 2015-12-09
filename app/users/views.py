from flask import redirect, render_template, render_template_string
from flask import request, url_for
from flask import flash
from flask_user import current_user, login_required, roles_required

# from app.app_and_db import app, db
from app import db
from app.users.models import User
from app.users.models import Role
from app.users.models import UserRoles
from app.users.forms import UserProfileForm
from app.users.forms import RoleForm
from flask import Blueprint

system_user = Blueprint('system_user', __name__,
                        template_folder='templates', url_prefix='/user')

#
# User Profile form
#
@system_user.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():

        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # # Redirect to home page
        # return redirect(url_for('page.home_page'))
        flash('Profile updated', 'success')

    # Process GET or invalid POST
    return render_template('users/user_profile_page.html', form=form)


# The Admin page is accessible to users with the 'admin' role
@system_user.route('/manage')
@roles_required('admin')    # Limits access to users with the 'admin' role
def manage():
    users = User.query.all()
    return render_template('users/users.html', users=users)


@system_user.route('/manage/user/<user_id>', methods=['GET', 'POST'])
@roles_required('admin')    # Limits access to users with the 'admin' role
def manage_user(user_id=False):

    if user_id:
        user = User.query.filter_by(id=user_id).first()

        # Initialize form
        form = UserProfileForm(request.form, user)
        form.role.choices = [(0, '')] + [(r.id, r.name) for r in Role.query.order_by('name')]

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(user)

        if form.role.data:
            user.roles = []
            for role_id in form.role.data:
                if role_id:
                    role = Role.query.filter_by(id=role_id).first()
                    user.roles.append(role)

        # Save user_profile
        db.session.commit()

        flash('Profile updated', 'success')
        return redirect(url_for('system_user.manage'))
    elif user_id:
        form.role.data = [role.id for role in user.roles]

    # Process GET or invalid POST
    return render_template('users/manage_user_profile.html', form=form)


@system_user.route('/manage/roles')
@roles_required('admin')    # Limits access to users with the 'admin' role
def manage_roles():
    roles = Role.query.all()
    return render_template('users/roles.html', roles=roles)


@system_user.route('/manage/role', methods=['GET', 'POST'])
@system_user.route('/manage/role/<role_id>', methods=['GET', 'POST'])
@roles_required('admin')    # Limits access to users with the 'admin' role
def manage_role(role_id=False):
    if role_id:
        role = Role.query.filter_by(id=role_id).first()
        form = RoleForm(request.form, role)

        # Process valid POST
        if request.method == 'POST' and form.validate():
            form.populate_obj(role)

            # Save role
            db.session.commit()

            flash('Role updated', 'success')
            return redirect(url_for('system_user.manage_roles'))
    else:
        form = RoleForm()
        if form.validate_on_submit():
            role = Role(name=form.name.data, label=form.label.data)
            db.session.add(role)
            db.session.commit()
            flash('Role {} is created!'.format(form.name.data))
            return redirect(url_for('system_user.manage_roles'))

    return render_template('users/manage_role.html', form=form)


@system_user.route('/manage/delete/<user_id>', methods=['GET', 'POST'])
@roles_required('admin')    # Limits access to users with the 'admin' role
def delete_user(user_id):
    return render_template('pages/admin_page.html')
