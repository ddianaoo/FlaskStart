from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'juicy-pussy-money-money-pussy-juicy'

menu = [{"name": 'Home', "url": "/"},
        {"name": 'Articles', "url": "articles"},
        {"name": 'Contacts', "url": "contact"},
        {"name": 'Details', "url": "about"}]


@app.route("/")
def index():
    return render_template('index.html', menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', title='About This Site', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    return f"User - {username}"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form["username"]) > 2:
            flash(f'{request.form["username"]}, Your message was sent!!', category='success')
        else:
            flash('Error, please try again. Your username must consist more than 2 letters!', category='error')

    return render_template('contact.html', title=menu[2]['name'], menu=menu)


# @app.route("/profile/<username>/<int:number>")
# def profile(username, number):
#     return f"User - {username}; Number - {number}"
#
#
# @app.route("/profile/<int:id>/<path:details>")
# def profile_details(id, details):
#     return f"ID - {id}; Details - {details}"


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username='ebal-tvoyu-mamky'))


if __name__ == "__main__":
    app.run(debug=True)