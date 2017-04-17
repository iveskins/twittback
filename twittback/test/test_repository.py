import twittback.repository


def test_persistent_repository(tweet_factory, tmp_path):
    tweet_1 = tweet_factory.make_tweet(1, "one")
    tweet_2 = tweet_factory.make_tweet(2, "two")
    db_path = tmp_path.joinpath("twittback.db")
    repository = twittback.repository.SQLRepository(db_path)
    repository.add([tweet_1, tweet_2])

    assert repository.latest_tweet() == tweet_2

    repository = twittback.repository.SQLRepository(db_path)
    assert list(repository.all_tweets()) == [tweet_1, tweet_2]


def test_list_tweets_by_date(tweet_factory):
    tweet_1 = tweet_factory.make_tweet(1, "one", date="2017-07-07")
    tweet_2 = tweet_factory.make_tweet(2, "two", date="2017-08-02")
    tweet_3 = tweet_factory.make_tweet(3, "three", date="2017-08-15")
    tweet_4 = tweet_factory.make_tweet(4, "four", date="2017-09-01")

    repository = twittback.repository.InMemoryRepository()
    repository.add([tweet_1, tweet_2, tweet_3, tweet_4])
    assert repository.tweets_for_month(20167, 8) == [tweet_2, tweet_3]
