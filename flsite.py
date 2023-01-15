from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, current_app, g
import os
import sqlite3
import click
from FDataBase import FDataBase

# configuration
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'juicy-pussy-money-money-pussy-juicy'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


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


menu = [{"name": 'Home', "url": "/"},
        {"name": 'Articles', "url": "/articles"},
        {"name": 'Contacts', "url": "/contact"},
        {"name": 'Details', "url": "/about"},
        {"name": 'Log in', "url": "/login"},
        {"name": 'Log out', "url": "/logout"}]


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPosts())


@app.route("/add-post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        res = dbase.addPost(request.form['title'], request.form['text'], request.form['url'])
        if not res:
            flash('Error occurred during creation post', category='error')
        else:
            flash(f'Yout post was added successfuly !!', category='success')

    return render_template('addpost.html', title='Add post', menu=dbase.getMenu())


@app.route("/post/<url>")
def showPost(url):
    db = get_db()
    dbase = FDataBase(db)
    title, text = dbase.getPost(url)
    if not title:
        abort(404)
    return render_template('single_post.html', menu=dbase.getMenu(), title=title, text=text)


@app.route("/about")
def about():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('about.html', title='Details', menu=dbase.getMenu())


@app.route("/profile/<username>")
def profile(username):
    db = get_db()
    dbase = FDataBase(db)
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(403)
    return render_template('base.html', title=f"User - {username}", menu=dbase.getMenu())


@app.route("/contact", methods=["POST", "GET"])
def contact():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form["username"]) > 2:
            flash(f'{request.form["username"]}, Your message was sent!!', category='success')
        else:
            flash('Error, please try again. Your username must consist more than 2 letters!', category='error')

    return render_template('contact.html', title=menu[2]['name'], menu=dbase.getMenu())


@app.route('/login', methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)

    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))

    if request.method == "POST":
        if request.form["username"] == 'diana' and request.form['password'] == '123':
            session['userLogged'] = request.form["username"]
            #flash(f'Successfuly Logged in as {request.form["username"]}!!', category='success')
            return redirect(url_for('profile', username=session['userLogged']))
        else:
            flash('Error, please try again!', category='error')

    return render_template('login.html', title='Log in', menu=dbase.getMenu())


@app.route('/logout', methods=["POST", "GET"])
def logout():
    session.pop('userLogged', None)
    return redirect(url_for('index'))


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username='ebal-tvoyu-mamky'))


@app.errorhandler(404)
def PageDoesntExist(error):
    return render_template('page404.html', title='Page Not Found! Please Check Your Url !', menu=menu), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('page403.html', title='This page is Forbidden for you!', menu=menu), 403


if __name__ == "__main__":
    app.run(debug=True)