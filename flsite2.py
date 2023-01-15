from flask import Flask, render_template, make_response

app = Flask(__name__)

menu = [
    {"title": "Home", "url": "index"}
    # {"title": "Add post", "url": "addPost"}
]


@app.route("/")
def index():
    # return render_template('index.html', menu=menu, posts=[])

    # 1 case
    # content = render_template('index.html', menu=menu, posts=[])
    # res = make_response(content)
    # res.headers['Content-Type'] = 'text/plain'
    # res.headers['Server'] = 'flasksite'

    # 2 case
    # img = None
    # with app.open_resource(app.root_path + "/static/img/dog/dog.jpg", mode="rb") as f:
    #     img = f.read()
    #
    # if img is None:
    #     return "None Image"
    #
    # res = make_response(img)
    # res.headers['Content-Type'] = 'image/jpg'

    # 3 case
    res = make_response("<h1>Error</h1>", 500)

    return res


if __name__ == "__main__":
    app.run(debug=True)