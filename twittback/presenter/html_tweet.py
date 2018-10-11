import re

import arrow


class HTMLTweet:
    def __init__(self, app, tweet, user_screen_name):
        self.app = app
        self.tweet = tweet
        self.user_screen_name = user_screen_name

    @property
    def date(self):
        return arrow.get(self.tweet.timestamp)

    @property
    def human_date(self):
        return self.date.strftime("%Y %a %B %d %H:%M")

    @property
    def html(self):
        res = self.tweet.text
        res = self.insert_span_around_handles(res)
        res = self.handle_hashtags(res)
        return self.surround_with_pre(res)

    @property
    def twitter_url(self):
        return "https://twitter.com/%s/status/%s" % (
            self.user_screen_name,
            self.tweet.twitter_id,
        )

    @classmethod
    def surround_with_pre(cls, res):
        return "<pre>" + res + "</pre>"

    def handle_hashtags(self, text):
        def replace_hashtag(match):
            space_before = match.groups()[0]
            hashtag_name = match.groups()[1]
            search_url = self.app.url_for("search", pattern=hashtag_name)
            res = "{space_before}"
            res += '<a class="hashtag" href="{search_url}">#{hashtag_name}</a>'
            res = res.format(
                space_before=space_before,
                hashtag_name=hashtag_name,
                search_url=search_url,
            )
            return res

        return re.sub(r"(^|\s)#(\w+)", replace_hashtag, text)

    @classmethod
    def insert_span_around_handles(cls, text):
        return re.sub(r"(^|\s)@(\w+)", r'\1<span class="handle">@\2</span>', text)

    @property
    def permalink(self):
        return self.app.url_for("view_tweet", twitter_id=self.tweet.twitter_id)
