""" twittback main Flask application """

import flask

import twittback.config
import twittback.repository
import twittback.presenter


class TwittBackFlaskApp(flask.Flask):
    repository = None

    def __init__(self):
        super().__init__("twittback")
        self.presenter = None
        self.db_path = None

    def get_repository(self):
        if self.repository is None:
            self.repository = twittback.repository.Repository(self.db_path)
        return self.repository


# pylint: disable=invalid-name
app = TwittBackFlaskApp()


@app.errorhandler(404)
def not_found(error_unused):
    return app.presenter.not_found()


@app.route("/")
def index():
    repository = app.get_repository()
    start_timestamp, end_timestamp = repository.date_range()
    return app.presenter.index(start_timestamp, end_timestamp)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.route("/feed.atom")
def atom_feed():
    repository = app.get_repository()
    latest_tweets = repository.latest_tweets()
    return app.presenter.feed(latest_tweets)

@app.route("/view/tweet/<int:twitter_id>")
def view_tweet(twitter_id):
    repository = app.get_repository()
    try:
        tweet = repository.get_by_id(twitter_id)
    except twittback.repository.NoSuchId:
        flask.abort(404)
    return app.presenter.view_tweet(tweet)

@app.route("/timeline/<int:year>/<int:month>")
def show_by_month(year, month):
    repository = app.get_repository()
    tweets_for_month = repository.tweets_for_month(year, month)
    return app.presenter.by_month(year, month, tweets_for_month)


@app.route("/search")
def search():
    pattern = flask.request.args.get("pattern")
    if pattern:
        return perform_search(app, pattern)
    else:
        return render_search_form(app)


def perform_search(flask_app, pattern):
    max_search_results = 100
    repository = flask_app.get_repository()
    tweets = list(repository.search(pattern))
    error = None
    if len(tweets) >= max_search_results:
        error = "Your search for '%s' yielded more than %d results" % (
            pattern, max_search_results)
    if not tweets:
        error = "No results found for '%s'" % pattern
    presenter = flask_app.presenter
    return presenter.search_results(pattern, tweets, error=error)


def render_search_form(flask_app):
    return flask_app.presenter.search_form()


def setup():
    app_config = twittback.config.read_config()
    server_config = app_config["server"]
    app.config["APPLICATION_ROOT"] = server_config.get("application_root")
    app.debug = server_config.get("debug", False)
    feed_generator = twittback.feed.FeedGenerator(app_config)
    app.presenter = twittback.presenter.Presenter(
        feed_generator=feed_generator
    )
    # Can't open sqlite3 connection here, otherwise it complains
    # about it being used in an other thread :/
    app.db_path = twittback.config.get_db_path()


# needs to be done outside main for uwsgi to work :/
setup()


if __name__ == "__main__":
    port = twittback.config.read_config()["server"]["port"]
    app.run(port=port)
