from functools import wraps
from flask import session, g
from cms.admin import admin_bp
from cms.admin.models import User
from flask import render_template, request, redirect, url_for, flash


def protected(route_function):
    @wraps(route_function)
    def wrapped_route_function(**kwargs):
        if g.User is None:
            return redirect(url_for('admin.login'))
        return route_function(**kwargs)
    return wrapped_route_function()


@admin_bp.before_app_request
def load_user():
    user_id = session.get(user_id)
    if user_id is not None:
        g.user = User.query.get(user_id)
    else:
        g.user = None

@admin_bp.route('/login', methods =["GET", "POST"] )
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.query.filter_by(username).first()
        if user is None:
            error = "Username is required."
        elif not user.check_password(password):
            error = 'Password is required.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect('admin.content', type='page')

        flash(error)

    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect('admin.login')
