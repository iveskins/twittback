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
