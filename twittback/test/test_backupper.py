import twittback
import twittback.backupper
import twittback.client.fake_client
import twittback.repository

import pytest


@pytest.fixture
def fake_client(john, alice, bob):
    client = twittback.client.fake_client.FakeClient()
    client.set_user(john)
    client.set_following([alice, bob])
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
    fake_client.timeline = [tweet_4, tweet_3, tweet_2, tweet_1]
    backupper = twittback.backupper.Backupper(repository=repository, client=fake_client)
    backupper.backup()
    assert list(repository.all_tweets()) == [tweet_1, tweet_2, tweet_3, tweet_4]


def test_first_backup(tweet_factory, repository, fake_client):
    tweet_1 = tweet_factory.make_tweet(1, "one")
    tweet_2 = tweet_factory.make_tweet(2, "two")
    fake_client.timeline = [tweet_2, tweet_1]
    backupper = twittback.backupper.Backupper(repository=repository, client=fake_client)
    backupper.backup()
    assert list(repository.all_tweets()) == [tweet_1, tweet_2]


def test_stores_user_info(repository, fake_client, john):
    backupper = twittback.backupper.Backupper(repository=repository, client=fake_client)
    backupper.backup()
    assert repository.user() == john


def test_stores_following(repository, fake_client, alice, bob):
    backupper = twittback.backupper.Backupper(repository=repository, client=fake_client)

    backupper.backup()
    following = repository.following()
    assert list(following) == [alice, bob]


def test_when_unfollowing(repository, fake_client, alice, bob):
    backupper = twittback.backupper.Backupper(repository=repository, client=fake_client)
    backupper.backup()

    fake_client.set_following([alice])

    backupper.backup()
    assert list(repository.following()) == [alice]


def test_followerrs(repository, fake_client, bob):
    fake_client.set_followers([bob])

    backupper = twittback.backupper.Backupper(repository=repository, client=fake_client)
    backupper.backup()

    assert list(repository.followers()) == [bob]
