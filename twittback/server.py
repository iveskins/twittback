""" twittback main Flask application """

import flask

import twittback.config
import twittback.repository

# pylint: disable=invalid-name
app = flask.Flask("twittback")


@app.route("/")
def index():
    return "Twittback"


def setup():
    config = twittback.config.read_config()
    server_config = config["server"]
    app.config["APPLICATION_ROOT"] = server_config.get("application_root")
    app.debug = server_config.get("debug", False)
    repository = twittback.repository.get_repository()
    app._repository = repository


# needs to be done outside main for uwsgi to work :/
setup()


if __name__ == "__main__":
    config = twittback.config.read_config()
    port = config["server"]["port"]
    app.run(port=port)
