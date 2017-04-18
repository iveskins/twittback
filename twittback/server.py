""" twittback main Flask application """

import flask

import twittback.config
import twittback.repository
import twittback.presenter


class TwittBackFlaskApp(flask.Flask):
    repository = None

    def __init__(self):
        super().__init__("twittback")
        self.html_presenter = None
        self.db_path = None

    def get_repository(self):
        if self.repository is None:
            self.repository = twittback.repository.Repository(self.db_path)
        return self.repository


# pylint: disable=invalid-name
app = TwittBackFlaskApp()


@app.route("/")
def index():
    repository = app.get_repository()
    start_timestamp, end_timestamp = repository.date_range()
    return app.html_presenter.gen_index(start_timestamp, end_timestamp)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route("/timeline/<int:year>/<int:month>")
def show_by_month(year, month):
    repository = app.get_repository()
    tweets_for_month = repository.tweets_for_month(year, month)
    return app.html_presenter.by_month(year, month, tweets_for_month)


def setup():
    app_config = twittback.config.read_config()
    server_config = app_config["server"]
    app.config["APPLICATION_ROOT"] = server_config.get("application_root")
    app.debug = server_config.get("debug", False)
    app.html_presenter = twittback.presenter.HTMLPresenter()
    # Can't open sqlite3 connection here, otherwise it complains
    # about it being used in an other thread :/
    app.db_path = twittback.config.get_db_path()


# needs to be done outside main for uwsgi to work :/
setup()


if __name__ == "__main__":
    port = twittback.config.read_config()["server"]["port"]
    app.run(port=port)
