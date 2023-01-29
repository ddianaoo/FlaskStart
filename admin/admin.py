from flask import Blueprint, render_template, url_for, request, flash, redirect, session, g, abort

from flask_login import logout_user

from FDataBase import FDataBase

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

menu = [
    {'url': '.index', 'title': 'Main Page'},
    {'url': '.posts', 'title': 'Posts'},
    {'url': '.users', 'title': 'Users'},
    {'url': '.logout', 'title': 'Log out'}
]


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)



db = None
@admin.before_request
def before_request():
    global db
    db = g.get('link_db')

@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


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


@admin.route('/posts')
def posts():
    if not isLogged():
        return redirect(url_for('.login'))

    if db:
        try:
            dbase = FDataBase(db)
            lst = dbase.getPosts()
        except:
            lst = []
    return render_template('admin/posts.html', menu=menu, title='List of posts', posts=lst)


@admin.route("/posts/<url>")
def get_post(url):
    if not isLogged():
        return redirect(url_for('.login'))
    if db:
        try:
            dbase = FDataBase(db)
            title, text = dbase.getPost(url)
            if not title:
                abort(404)
            return render_template('admin/single_post.html', menu=menu, title=title, text=text)
        except:
            abort(404)


@admin.route('/users')
def users():
    if not isLogged():
        return redirect(url_for('.login'))

    if db:
        try:
            dbase = FDataBase(db)
            lst = dbase.getUsers()
        except:
            lst = []
    return render_template('admin/users.html', menu=menu, title='List of users', users=lst)