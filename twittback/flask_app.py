""" twittback main Flask application """

import flask

import twittback.server


# pylint: disable=invalid-name
server = twittback.server.build_server()
app = server.app


@app.errorhandler(404)
# pylint: disable=unused-argument
def not_found(error):
    return server.not_found(), 404


@app.route("/")
def index():
    return server.index()


@app.route("/favicon.ico")
def favicon():
    return server.favicon()


@app.route("/feed.atom")
def feed():
    return server.gen_feed()


@app.route("/view/tweet/<int:twitter_id>")
def view_tweet(twitter_id):
    return server.view_tweet(twitter_id)


@app.route("/view/user")
def view_user():
    return server.view_user()


@app.route("/timeline/<int:year>/<int:month>")
def timeline(year, month):
    return server.timeline(year, month)


@app.route("/search")
def search():
    pattern = flask.request.args.get("pattern")
    if pattern:
        return server.search(pattern)
    else:
        return server.search_form()


if __name__ == "__main__":
    app.run(port=server.port)
