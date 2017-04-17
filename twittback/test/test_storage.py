import twittback.storage


def test_persistent_storage(tweet_factory, tmp_path):
    tweet_1 = tweet_factory.make_tweet(1, "one")
    tweet_2 = tweet_factory.make_tweet(2, "two")
    db_path = tmp_path.joinpath("twittback.db")
    storage = twittback.storage.SQLStorage(db_path)
    storage.add([tweet_1, tweet_2])

    assert storage.latest_tweet() == tweet_2

    storage = twittback.storage.SQLStorage(db_path)
    assert list(storage.all_tweets()) == [tweet_1, tweet_2]
