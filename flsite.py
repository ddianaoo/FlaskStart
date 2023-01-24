from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, current_app, g, make_response
import os
import sqlite3
import datetime
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm, ContactForm, AddPostForm
from admin.admin import admin


# configuration
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'juicy-pussy-money-money-pussy-juicy'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

app.permanent_session_lifetime = datetime.timedelta(days=10)

app.register_blueprint(admin, url_prefix='/admin')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in if you want to visit this page'
login_manager.login_message_category = 'error'


@login_manager.user_loader
def load_user(user_id):
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
@login_required
def addPost():
    form = AddPostForm()
    if form.validate_on_submit():
        res = dbase.addPost(form.title.data, form.text.data, form.url.data)
        if not res:
            flash('Error occurred during creation post', category='error')
        else:
            flash(f'Yout post was added successfuly !!', category='success')
            return redirect(url_for('index'))

    return render_template('addpost.html', title='Add post', menu=dbase.getMenu(), form=form)


@app.route("/contact", methods=["POST", "GET"])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        res = dbase.addMessage(form.email.data, form.message.data)
        print(res)
        if res and form.email.data == current_user.getEmail():
            print('I passed all validation')
            flash(f'{form.username.data}, your message was sent!!', category='success')
            return redirect(url_for('index'))
        else:
            flash('Error, confirm that your email is correct and try again', category='error')

    return render_template('contact.html', title='Contacts', menu=dbase.getMenu(), form=form)


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
    if username != current_user.getName():
        abort(403)
    return render_template('profile.html', title=f"User - {username}", menu=dbase.getMenu())


@app.route("/userphoto")
@login_required
def userphoto():
    img = current_user.getPhoto(app)
    if not img:
        return ''
    h = make_response(img)
    h.headers['Content-Type'] = 'image/jpg'
    return h


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserPhoto(img, current_user.get_id())
                if not res:
                    flash('Error during uploading your photo', 'error')
                    return redirect(url_for('profile', username=current_user.getName()))
                flash('Your new photo added', 'success')
            except FileNotFoundError as e:
                flash('Error during reading file', 'error')
        else:
            flash('Error during uploading your photo', 'error')

    return redirect(url_for('profile', username=current_user.getName()))


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.password.data)
        res = dbase.addUser(form.username.data, form.email.data, hash)
        if res:
            flash(f'Successfuly registered as {form.username.data}!!', category='success')
            return redirect(url_for('login'))
        else:
            flash('Error, email already in use!', category='error')

    return render_template('register.html', title='Registration', menu=dbase.getMenu(), form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.getName()))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUser(email=form.email.data)

        if user and form.username.data == user['username'] and check_password_hash(user['password'], form.password.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            flash(f'Successfuly Logged in as {form.username.data} !!', category='success')
            #return redirect(url_for('profile', username=request.form["username"]))
            return redirect(request.args.get("next") or url_for('profile', username=form.username.data))

        flash('The entered data is incorrect', category='error')

    return render_template('login.html', title='Log in', menu=dbase.getMenu(), form=form)


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