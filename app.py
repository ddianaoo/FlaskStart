from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.email}>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


@app.route('/register', methods=["POST", 'GET'])
def register():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], password=hash)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")


    return render_template('register.html', title='Registration')


@app.route('/')
def index():
    users = []
    try:
        users = Users.query.all()
    except:
        print("Ошибка чтения из БД")
    return render_template('index.html', title='Main Page', users=users)





if __name__ == "__main__":
    app.run(debug=True)