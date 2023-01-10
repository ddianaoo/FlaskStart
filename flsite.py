from flask import Flask, render_template, url_for

app = Flask(__name__)

menu = [{"name": 'Set up', "url": "install-flask"},
        {"name": 'First application', "url": "first-app"},
        {"name": 'Contacts', "url": "contact"}]


@app.route("/")
def index():
    return render_template('index.html', menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', title='About This Site', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    return f"User - {username}"


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