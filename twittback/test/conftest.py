import arrow
import bs4
import path

import twittback
import twittback.flask_app

import pytest


@pytest.fixture
def tmp_path(tmpdir):
    return path.Path(str(tmpdir))


class TweetFactory:
    def make_tweet(self, twitter_id, text, **kwargs):
        fixed_kwargs = self.fix_kwargs(kwargs)
        ret = twittback.Tweet(twitter_id=twitter_id, text=text, **fixed_kwargs)
        return ret

    @classmethod
    def fix_kwargs(cls, kwargs):
        date = kwargs.pop("date", None)
        if date:
            kwargs["timestamp"] = arrow.get(date).timestamp
        return kwargs


class Browser:
    def __init__(self, flask_client):
        self._flask_client = flask_client

    def open(self, url, allow_bad_status=False):
        response = self._flask_client.get(url)
        if not allow_bad_status:
            assert 200 <= response.status_code < 400
        self.page = response.data.decode()

    @property
    def html_soup(self):
        return bs4.BeautifulSoup(self.page, "html.parser")

    def clink_link(self, link):
        assert link is not None
        href = link.attrs["href"]
        self.open(href)


@pytest.fixture()
def browser(client):
    return Browser(client)


@pytest.fixture()
def tweet_factory():
    return TweetFactory()


@pytest.fixture()
def repository():
    return twittback.repository.Repository(":memory:")


# John follows Alice and Bob
@pytest.fixture
def john():
    return twittback.User(
        screen_name="john_doe",
        name="John Doe",
        location="Paris, France",
        description="Anonymous Coward",
    )


@pytest.fixture
def alice():
    return twittback.User(
        screen_name="alice", name="Alice", location="In Wonderland", description=""
    )


@pytest.fixture
def bob():
    return twittback.User(
        screen_name="bob", name="Bob Lennon", location="", description="Famous Guy"
    )


@pytest.fixture
def eve():
    return twittback.User(
        screen_name="Evan", name="Evil Evan", location="In Hell", description="Fanboy"
    )


@pytest.fixture()
def app(repository):
    server = twittback.flask_app.server
    server.repository = repository
    return twittback.flask_app.app
