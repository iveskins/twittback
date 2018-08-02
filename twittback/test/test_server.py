import feedparser

import pytest


@pytest.fixture(autouse=True)
def init_repository(tweet_factory, repository, app, john, alice, bob, eve):
    tweet_1 = tweet_factory.make_tweet(1, "First tweet! ", date="2017-07-07")
    tweet_2 = tweet_factory.make_tweet(2, "Second tweet", date="2017-08-02")
    tweet_3 = tweet_factory.make_tweet(3, "Third tweet", date="2017-08-15")
    tweet_4 = tweet_factory.make_tweet(4, "Fourth tweet", date="2017-09-01")
    repository.add_tweets([tweet_1, tweet_2, tweet_3, tweet_4])
    repository.save_user(john)
    repository.save_following([alice, bob])
    repository.save_followers([eve])


def test_when_browsing_index(browser):
    """ can click on the 'by month' links """
    browser.open("/")
    assert "Welcome to TwittBack" in browser.page
    assert "4 tweets saved" in browser.page
    link = browser.html_soup.find("a", text="July")
    browser.clink_link(link)


def test_search_form(browser):
    browser.open("/search")


def test_perform_search(browser):
    browser.open("/search?pattern=First")
    assert "First tweet!" in browser.page


def test_view_tweet(browser):
    browser.open("/view/tweet/1")
    assert "First tweet!" in browser.page


def test_view_tweet_not_found(browser):
    browser.open("/view/tweet/42", allow_bad_status=True)
    assert "Not Found" in browser.page


def test_view_user(browser, john, alice, bob, eve):
    browser.open("/view/user")
    assert john.name in browser.page
    assert "Following" in browser.page
    assert alice.name in browser.page
    assert "Followers" in browser.page
    assert eve.name in browser.page


def test_feed(browser):
    browser.open("/feed.atom")
    parsed = feedparser.parse(browser.page)
    assert parsed.feed.title == "Twittback"
    assert len(parsed.entries) == 4
    first_entry = parsed.entries[0]
    assert "2017 Fri September" in first_entry.title


def test_feed_no_side_effect(browser):
    browser.open("/feed.atom")
    parsed = feedparser.parse(browser.page)
    assert len(parsed.entries) == 4

    browser.open("/feed.atom")
    parsed = feedparser.parse(browser.page)
    assert len(parsed.entries) == 4
