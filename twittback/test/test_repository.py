import twittback.repository

import pytest


def test_persistent_repository(tweet_factory, tmp_path):
    tweet_1 = tweet_factory.make_tweet(1, "one")
    tweet_2 = tweet_factory.make_tweet(2, "two")
    db_path = tmp_path.joinpath("twittback.db")
    repository = twittback.repository.Repository(db_path)
    repository.add_tweets([tweet_1, tweet_2])

    assert repository.latest_tweet() == tweet_2

    repository = twittback.repository.Repository(db_path)
    assert list(repository.all_tweets()) == [tweet_1, tweet_2]


def test_list_tweets_by_date(tweet_factory, repository):
    tweet_1 = tweet_factory.make_tweet(1, "one", date="2017-07-07")
    tweet_2 = tweet_factory.make_tweet(2, "two", date="2017-08-02")
    tweet_3 = tweet_factory.make_tweet(3, "three", date="2017-08-15")
    tweet_4 = tweet_factory.make_tweet(4, "four", date="2017-09-01")
    repository.add_tweets([tweet_1, tweet_2, tweet_3, tweet_4])

    actual = repository.tweets_for_month(2017, 8)
    assert list(actual) == [tweet_2, tweet_3]


def test_get_date_range(tweet_factory, repository):
    tweet_1 = tweet_factory.make_tweet(1, "one", timestamp=1400)
    tweet_2 = tweet_factory.make_tweet(2, "two", timestamp=1550)
    tweet_3 = tweet_factory.make_tweet(3, "three", timestamp=1600)
    repository.add_tweets([tweet_1, tweet_2, tweet_3])

    assert repository.date_range() == (1400, 1600)


def test_tweet_by_id(tweet_factory, repository):
    tweet_1 = tweet_factory.make_tweet(1, "one", timestamp=1400)
    tweet_2 = tweet_factory.make_tweet(2, "two", timestamp=1550)
    repository.add_tweets([tweet_1, tweet_2])

    assert repository.tweet_by_id(1) == tweet_1
    assert repository.tweet_by_id(2) == tweet_2
    with pytest.raises(twittback.repository.NoSuchId):
        repository.tweet_by_id(3)


def test_user(repository, john):
    repository.save_user(john)
    assert repository.user() == john
