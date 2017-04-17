import re

import arrow
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


@pytest.fixture()
def tweet_factory():
    return TweetFactory()


@pytest.fixture()
def repository():
    return twittback.repository.Repository(":memory:")
