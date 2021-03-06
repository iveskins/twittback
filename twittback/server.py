from feedgenerator import Atom1Feed
import flask
from path import Path

import twittback.config
import twittback.repository
import twittback.presenter
import twittback.presenter.renderer


class Server:
    def __init__(self):
        self.app = None
        self.port = None
        self.db_path = None
        self.presenter = None
        self._repository = None

    @property
    def repository(self):
        if not self._repository:
            self._repository = twittback.repository.Repository(self.db_path)
        return self._repository

    @repository.setter
    def repository(self, value):
        self._repository = value

    def index(self):
        date_range = self.repository.date_range()
        user = self.repository.user()
        num_tweets = self.repository.num_tweets()
        return self.presenter.index(
            user=user, date_range=date_range, num_tweets=num_tweets
        )

    def not_found(self):
        return self.presenter.not_found()

    def favicon(self):
        return self.app.send_static_file("favicon.ico")

    def gen_feed(self):
        latest_tweets = self.repository.latest_tweets()
        return self.presenter.gen_feed(latest_tweets)

    def view_tweet(self, twitter_id):
        try:
            tweet = self.repository.tweet_by_id(twitter_id)
        except twittback.repository.NoSuchId:
            self.app.abort(404)
        return self.presenter.view_tweet(tweet)

    def view_user(self):
        user = self.repository.user()
        following = self.repository.following()
        followers = self.repository.followers()
        return self.presenter.view_user(user, following=following, followers=followers)

    def timeline(self, year, month):
        tweets_for_month = self.repository.tweets_for_month(year, month)
        return self.presenter.by_month(year, month, tweets_for_month)

    def search(self, pattern):
        max_search_results = 1000
        tweets = list(self.repository.search_tweet(pattern))
        error = None
        if len(tweets) >= max_search_results:
            error = "Your search for '%s' yielded more than %d results" % (
                pattern,
                max_search_results,
            )
        if not tweets:
            error = "No results found for '%s'" % pattern
        return self.presenter.search_results(pattern, tweets, error=error)

    def search_form(self):
        return self.presenter.search_form()


def read_config():
    return twittback.config.read_config()


def build_flask_app(config):
    flask_app = flask.Flask("twittback")
    flask_app.url_for = flask.url_for
    flask_app.abort = flask.abort
    flask_app.debug = config.get("debug", False)
    flask_app.port = config["port"]
    return flask_app


def build_feed(config):
    site_url = config["site_url"]
    feed_url = "%s/feed.atom" % site_url
    atom1_feed = Atom1Feed(
        title="Twittback", description="Latest tweets", link=site_url, feed_url=feed_url
    )
    return atom1_feed


def build_presenter(flask_app, feed, config):
    presenter = twittback.presenter.Presenter()
    presenter.app = flask_app
    renderer = twittback.presenter.renderer.Renderer()
    renderer.app = flask_app
    presenter.renderer = renderer
    presenter.feed = feed
    presenter.user_screen_name = config["user"]["screen_name"]
    return presenter


def build_server():
    app_config = read_config()
    server_config = app_config["server"]

    flask_app = build_flask_app(server_config)
    feed = build_feed(server_config)
    presenter = build_presenter(flask_app, feed, app_config)

    server = Server()

    db_path = Path(app_config["db"]["path"])
    server.db_path = db_path

    server.app = flask_app
    server.presenter = presenter
    server.port = server_config["port"]

    return server
