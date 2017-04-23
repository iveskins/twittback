import twittback
import twittback.backupper
import twittback.client.fake_client
import twittback.repository

import pytest


@pytest.fixture
def fake_client(john):
    client = twittback.client.fake_client.FakeClient()
    client.set_user(john)
    return client


def test_backup_new_tweets(tweet_factory, repository, fake_client):
    """ Given 2 tweets in the repository, and 4 tweets
    in the timeline, store the tweets 3 and 4

    """
    tweet_1 = tweet_factory.make_tweet(1, "one")
    tweet_2 = tweet_factory.make_tweet(2, "two")
    tweet_3 = tweet_factory.make_tweet(3, "three")
    tweet_4 = tweet_factory.make_tweet(4, "four")

    repository.add_tweets([tweet_1, tweet_2])
    fake_client.timeline = [
        tweet_4, tweet_3, tweet_2, tweet_1
    ]
    backupper = twittback.backupper.Backupper(repository=repository,
                                              client=fake_client)
    backupper.backup()
    assert list(repository.all_tweets()) == [
        tweet_1, tweet_2, tweet_3, tweet_4
    ]


def test_first_backup(tweet_factory, repository, fake_client):
    tweet_1 = tweet_factory.make_tweet(1, "one")
    tweet_2 = tweet_factory.make_tweet(2, "two")
    fake_client.timeline = [tweet_2, tweet_1]
    backupper = twittback.backupper.Backupper(repository=repository,
                                              client=fake_client)
    backupper.backup()
    assert list(repository.all_tweets()) == [tweet_1, tweet_2]


def test_stores_user_info(repository, fake_client):
    backupper = twittback.backupper.Backupper(repository=repository,
                                              client=fake_client)
    backupper.backup()
    user = repository.user()
    assert user.name == "John Doe"
    assert user.location == "Paris, France"
    assert user.description == "Anonymous Coward"
