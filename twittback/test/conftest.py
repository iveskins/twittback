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
        ret = twittback.Tweet(
            twitter_id=twitter_id, text=text,
            **kwargs)
        return ret


@pytest.fixture()
def tweet_factory():
    return TweetFactory()
