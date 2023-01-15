from flask import Flask, render_template, make_response, redirect, url_for

app = Flask(__name__)

menu = [
    {"title": "Home", "url": "index"}
    # {"title": "Add post", "url": "addPost"}
]


@app.route("/")
def index():
    return "<h1>Home</h1>", 200, {'Content-Type': 'text/plain'}


@app.route('/transfer')
def transfer():
    return redirect(url_for('index'), 301)


@app.errorhandler(404)
def PageDoesntExist(error):
    return ('Page Not Found', 404)


@app.before_first_request
def before_first_request():
    print("before_first_request() called")
    
@app.before_request    
def before_request():
    print("before_request() called")

@app.after_request
def after_request(response):
    print("after_request() called")
    return response

@app.teardown_request
def teardown_request(response):
    print("teardown_request() called")
    return response

if __name__ == "__main__":
    app.run(debug=True)