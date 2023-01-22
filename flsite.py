from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, current_app, g, make_response
import os
import sqlite3
import datetime
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin


# configuration
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'juicy-pussy-money-money-pussy-juicy'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

app.permanent_session_lifetime = datetime.timedelta(days=10)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in if you want to visit this page'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


menu = [{"name": 'Home', "url": "/"},
        {"name": 'Articles', "url": "/articles"},
        {"name": 'Contacts', "url": "/contact"},
        {"name": 'Details', "url": "/about"},
        {"name": 'Log in', "url": "/login"},
        {"name": 'Log out', "url": "/logout"}]


@app.route("/")
def index():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1

    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPosts(), visits=session['visits'])


@app.route("/add-post", methods=["POST", "GET"])
def addPost():
    if request.method == 'POST':
        res = dbase.addPost(request.form['title'], request.form['text'], request.form['url'])
        if not res:
            flash('Error occurred during creation post', category='error')
        else:
            flash(f'Yout post was added successfuly !!', category='success')

    return render_template('addpost.html', title='Add post', menu=dbase.getMenu())


@app.route("/post/<url>")
@login_required
def showPost(url):
    title, text = dbase.getPost(url)
    if not title:
        abort(404)
    return render_template('single_post.html', menu=dbase.getMenu(), title=title, text=text)


@app.route("/about")
def about():
    return render_template('about.html', title='Details', menu=dbase.getMenu())


@app.route("/profile/<username>")
@login_required
def profile(username):
    requester_id = current_user.get_id()
    requester = dbase.getUser(user_id=requester_id)

    if username != requester['username']:
        abort(403)
    return render_template('base.html', title=f"User - {username}", menu=dbase.getMenu())


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form["username"]) > 2:
            flash(f'{request.form["username"]}, Your message was sent!!', category='success')
        else:
            flash('Error, please try again. Your username must consist more than 2 letters!', category='error')

    return render_template('contact.html', title=menu[2]['name'], menu=dbase.getMenu())


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['username']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['password']) > 3 and request.form['password'] == request.form['password2']:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['username'], request.form['email'], hash)
            if res:
                flash(f'Successfuly registered as {request.form["username"]}!!', category='success')
                return redirect(url_for('login'))
            else:
                flash('Error, email already in use!', category='error')
        flash('Error, The entered data is incorrect! Maybe your username, email or password too short. Or passwords aren`t the same!', category='error')
    return render_template('register.html', title='Registration', menu=dbase.getMenu())


# @app.route('/login', methods=["POST", "GET"])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#
#     if request.method == "POST":
#         user = dbase.getUser(email=request.form['email'])
#
#         if not user:
#             flash('Error, please try again!', category='error')
#             return render_template('login.html', title='Log in', menu=dbase.getMenu())
#
#         if request.form["username"] == user['username'] and user['email'] == request.form['email'] and check_password_hash(user['password'], request.form['password']):
#             session['userLogged'] = request.form["username"]
#             flash(f'Successfuly Logged in as {request.form["username"]}!!', category='success')
#             return redirect(url_for('profile', username=session['userLogged']))
#         else:
#             flash('Error, please try again!', category='error')
#
#     return render_template('login.html', title='Log in', menu=dbase.getMenu())
#
#
# @app.route('/logout')
# def logout():
#     session.pop('userLogged', None)
#     return redirect(url_for('index'))


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        requester_id = current_user.get_id()
        requester = dbase.getUser(user_id=requester_id)
        return redirect(url_for('profile', username=requester['username']))

    if request.method == "POST":
        user = dbase.getUser(email=request.form['email'])

        if user and request.form["username"] == user['username'] and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            flash(f'Successfuly Logged in as {request.form["username"]} !!', category='success')
            #return redirect(url_for('profile', username=request.form["username"]))
            return redirect(request.args.get("next") or url_for('profile', username=request.form["username"]))

        flash('The entered data is incorrect', category='error')
    return render_template('login.html', title='Log in', menu=dbase.getMenu())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are out of your account', 'success')
    return redirect(url_for('index'))


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username='ebal-tvoyu-mamky'))


@app.errorhandler(404)
def PageDoesntExist(error):
    return render_template('page404.html', title='Page Not Found! Please Check Your Url !', menu=dbase.getMenu()), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('base.html', title='This page is Forbidden for you!', menu=dbase.getMenu()), 403

@app.errorhandler(401)
def forbidden(error):
    return render_template('base.html', title='You are Unauthorized!', menu=dbase.getMenu()), 401


if __name__ == "__main__":
    app.run(debug=True)