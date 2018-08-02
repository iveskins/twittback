import textwrap
from unittest import mock

import twittback
import twittback.presenter


def test_insert_spans():
    tweet = twittback.Tweet(twitter_id=1, text="Talking to @bob about #stuff")
    expected_url = "http://example.com/search?pattern=stuff"
    app = mock.Mock()
    app.url_for = mock.Mock()
    app.url_for.return_value = "http://example.com/search?pattern=stuff"
    html_tweet = twittback.presenter.HTMLTweet(app, tweet)
    expected = "<pre>"
    expected += "Talking to "
    expected += '<span class="handle">@bob</span> '
    expected += "about "
    expected += '<a class="hashtag" href="%s">#stuff</a>' % expected_url
    expected += "</pre>"
    assert html_tweet.html == expected


def test_do_not_break_urls():
    tweet = twittback.Tweet(twitter_id=1, text="http://example.com#1 has an anchor")
    app = mock.Mock()
    html_tweet = twittback.presenter.HTMLTweet(app, tweet)
    expected = "<pre>"
    expected += "http://example.com#1 has an anchor"
    expected += "</pre>"
    assert html_tweet.html == expected
