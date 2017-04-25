import textwrap
from unittest import mock

import twittback
import twittback.presenter

def test_insert_spans():
    tweet = twittback.Tweet(
        twitter_id=1,
        text="Talking to @bob about #stuff"
    )
    app = mock.Mock()
    html_tweet = twittback.presenter.HTMLTweet(app, tweet)
    expected = '<pre>'
    expected += 'Talking to '
    expected += '<span class="handle">@bob</span> '
    expected += 'about '
    expected += '<span class="hashtag">#stuff</span>'
    expected += '</pre>'
    assert html_tweet.html == expected


def test_do_not_break_urls():
    tweet = twittback.Tweet(
        twitter_id=1,
        text="http://example.com#1 has an anchor"
    )
    app = mock.Mock()
    html_tweet = twittback.presenter.HTMLTweet(app, tweet)
    expected = '<pre>'
    expected += 'http://example.com#1 has an anchor'
    expected += '</pre>'
    assert html_tweet.html == expected
