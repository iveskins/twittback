""" twittback main Flask application """

import flask

# pylint: disable=invalid-name
app = flask.Flask("twittback")


@app.route("/")
def index():
    return "Twittback"


if __name__ == "__main__":
    app.run()
