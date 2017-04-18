import re

import arrow
import bs4
import path

import twittback
import twittback.server

import pytest


@pytest.fixture()
def app():
    return twittback.server.app


@pytest.fixture
def tmp_path(tmpdir):
    return path.Path(str(tmpdir))


class TweetFactory:
    def make_tweet(self, twitter_id, text, **kwargs):
        fixed_kwargs = self.fix_kwargs(kwargs)
        ret = twittback.Tweet(
            twitter_id=twitter_id, text=text,
            **fixed_kwargs)
        return ret

    @classmethod
    def fix_kwargs(cls, kwargs):
        date = kwargs.pop("date", None)
        if date:
            kwargs["timestamp"] = arrow.get(date).timestamp
        return kwargs


class Browser():
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

    def clink_link(self, link_id):
        link = self.soup.find("a", id=link_id)
        self._flask_client.get(link.attributes["href"])


@pytest.fixture()
def browser(client):
    return Browser(client)


@pytest.fixture()
def tweet_factory():
    return TweetFactory()


@pytest.fixture()
def repository():
    return twittback.repository.Repository(":memory:")
