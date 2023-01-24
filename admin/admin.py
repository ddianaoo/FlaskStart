from flask import Blueprint, render_template, url_for, request, flash, redirect, session

from flask_login import logout_user


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

menu = [
    {'url': '.index', 'title': 'Admin Main Page'},
    {'url': '.logout', 'title': 'Log out'}
]


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title='Admin Tools')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form['username'] == 'admin' and request.form['password'] == '1234':
            login_admin()
            flash('You logged in successfully', category='success')
            return redirect(url_for('.index'))
        else:
            flash('The entered data is incorrect', category='error')

    return render_template('admin/login.html', title='Log in')


@admin.route('/logout')
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    flash('You are out of your account', category='success')
    return redirect(url_for('.login'))