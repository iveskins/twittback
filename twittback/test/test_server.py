import pytest


@pytest.fixture(autouse=True)
def init_repository(tweet_factory, repository, app):
    print("Init repository")
    tweet_1 = tweet_factory.make_tweet(1, "one", date="2017-07-07")
    tweet_2 = tweet_factory.make_tweet(2, "two", date="2017-08-02")
    tweet_3 = tweet_factory.make_tweet(3, "three", date="2017-08-15")
    tweet_4 = tweet_factory.make_tweet(4, "four", date="2017-09-01")
    repository.add([tweet_1, tweet_2, tweet_3, tweet_4])
    app.db_path = ":memory:"
    app.repository = repository


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Welcome to TwittBack" in data
