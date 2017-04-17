import twittback
import twittback.backupper
import twittback.client.fake_client
import twittback.repository

import pytest


def test_backup_new_tweets(tweet_factory):
    """ Given 2 tweets in the repository, and 4 tweets
    in the timeline, store the tweets 3 and 4

    """
    tweet_1 = tweet_factory.make_tweet(1, "one")
    tweet_2 = tweet_factory.make_tweet(2, "two")
    tweet_3 = tweet_factory.make_tweet(3, "three")
    tweet_4 = tweet_factory.make_tweet(4, "four")

    repository = twittback.repository.InMemoryRepository()
    repository.add([tweet_1, tweet_2])
    client = twittback.client.fake_client.FakeClient()
    client.timeline = [
        tweet_4, tweet_3, tweet_2, tweet_1
    ]
    backupper = twittback.backupper.Backupper(repository=repository,
                                              client=client)
    backupper.backup()
    assert list(repository.all_tweets()) == [
        tweet_1, tweet_2, tweet_3, tweet_4
    ]


def test_first_backup(tweet_factory):
    tweet_1 = tweet_factory.make_tweet(1, "one")
    tweet_2 = tweet_factory.make_tweet(2, "two")
    repository = twittback.repository.InMemoryRepository()
    client = twittback.client.fake_client.FakeClient()
    client.timeline = [tweet_2, tweet_1]
    backupper = twittback.backupper.Backupper(repository=repository,
                                              client=client)
    backupper.backup()
    assert list(repository.all_tweets()) == [tweet_1, tweet_2]
