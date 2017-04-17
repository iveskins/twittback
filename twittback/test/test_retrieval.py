import twittback
import twittback.client
import twittback.storage

import pytest


class TweetFactory:
    def make_tweet(self, twitter_id, text):
        ret = twittback.Tweet()
        ret.twitter_id = twitter_id
        ret.text = text
        return ret


@pytest.fixture()
def tweet_factory():
    return TweetFactory()


def test_can_fetch_new_tweets(tweet_factory):
    tweet_1 = tweet_factory.make_tweet(1, "one")
    tweet_2 = tweet_factory.make_tweet(2, "two")
    tweet_3 = tweet_factory.make_tweet(3, "three")
    client = twittback.client.FakeClient()
    client.timeline = [
        tweet_3, tweet_2, tweet_1
    ]
    new_tweets = client.get_latest_tweets()
    assert new_tweets == [tweet_3, tweet_2, tweet_1]
