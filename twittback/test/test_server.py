import pytest


@pytest.fixture(autouse=True)
def init_repository(tweet_factory, repository, app):
    tweet_1 = tweet_factory.make_tweet(1, "First tweet! ", date="2017-07-07")
    tweet_2 = tweet_factory.make_tweet(2, "Second tweet", date="2017-08-02")
    tweet_3 = tweet_factory.make_tweet(3, "Third tweet", date="2017-08-15")
    tweet_4 = tweet_factory.make_tweet(4, "Fourth tweet", date="2017-09-01")
    repository.add([tweet_1, tweet_2, tweet_3, tweet_4])
    app.db_path = ":memory:"
    app.repository = repository


def test_when_browsing_index(browser):
    """ can click on the 'by month' links """
    browser.open("/")
    assert "Welcome to TwittBack" in browser.page
    link = browser.html_soup.find("a", text="July")
    browser.clink_link(link)


def test_search_form(browser):
    browser.open("/search")


def test_perform_search(browser):
    browser.open("/search?pattern=First")
    assert "First tweet!" in browser.page
