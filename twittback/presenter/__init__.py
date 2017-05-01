import itertools

import arrow

from .html_tweet import HTMLTweet


class Presenter:
    def __init__(self):
        self.renderer = None
        self.feed = None
        self.app = None

    def index(self, user, start_timestamp, end_timestamp):
        dates = self.collect_dates(start_timestamp, end_timestamp)
        year_groups = self.group_dates_by_year(dates)
        context = dict()
        context["user"] = user
        context["year_groups"] = year_groups
        return self.renderer.render("index.html", context)

    def gen_feed(self, latest_tweets):
        for tweet in latest_tweets:
            self.add_tweet_to_feed(tweet)
        return self.feed.writeString("utf-8")

    def add_tweet_to_feed(self, tweet):
        html_tweet = self.tweet_for_template(tweet)
        date = html_tweet.date
        permalink = html_tweet.permalink
        entry_id = date
        description = html_tweet.html
        self.feed.add_item(
            title=entry_id,
            link=permalink,
            description=description,
            pubdate=date,
            updated=date,
        )

    def by_month(self, year, month_index, tweets):
        context = dict()
        context["year"] = year
        context["month_name"] = self.get_month_name(month_index)
        context["tweets"] = self.tweets_for_template(tweets)
        return self.renderer.render("by_month.html", context)

    def search_results(self, pattern, tweets, *, error=None):
        context = dict()
        context["pattern"] = pattern
        context["error"] = error
        context["tweets"] = self.tweets_for_template(tweets)
        return self.renderer.render("search_results.html", context)

    def search_form(self):
        return self.renderer.render("search_form.html", dict())

    def view_tweet(self, tweet):
        context = dict()
        context["tweet"] = self.tweet_for_template(tweet)
        return self.renderer.render("view_tweet.html", context)

    def view_user(self, user, following):
        context = dict()
        context["user"] = user
        context["following"] = following
        return self.renderer.render("view_user.html", context)

    def not_found(self):
        return self.renderer.render("not_found.html", dict())

    def tweet_for_template(self, tweet):
        return HTMLTweet(self.app, tweet)

    def tweets_for_template(self, tweets):
        return [self.tweet_for_template(t) for t in tweets]

    @classmethod
    def collect_dates(cls, start_timestamp, end_timestamp):
        start_date = arrow.get(start_timestamp)
        end_date = arrow.get(end_timestamp)
        date = start_date.floor("month")
        dates = list()
        while date <= end_date.floor("month"):
            dates.append(date)
            date = date.shift(months=+1)
        return dates

    @classmethod
    def group_dates_by_year(cls, dates):
        year_groups = list()
        for year, group in itertools.groupby(dates, lambda x: x.year):
            months_list = [(x.strftime("%m"), x.strftime("%B")) for x in group]
            year_groups.append((str(year), months_list))
        return year_groups

    @classmethod
    def get_month_name(cls, month_index):
        date = arrow.Arrow(year=2000, day=1, month=month_index)
        return date.strftime("%B")

    @classmethod
    def get_month_number(cls, month_index):
        date = arrow.Arrow(year=2000, day=1, month=month_index)
        return date.strftime("%m")
