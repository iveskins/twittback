import abc
import html
import itertools

import arrow
import jinja2
import markdown

import twittback

class Renderer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def render(self, template_name: str, context: dict) -> str:
        pass


class HTMLPresenter:
    def __init__(self, renderer=None):
        if renderer:
            self.renderer = renderer
        else:
            self.renderer = JinjaRenderer()

    def gen_index(self, start_timestamp, end_timestamp):
        dates = self.collect_dates(start_timestamp, end_timestamp)
        year_groups = self.group_dates_by_year(dates)
        context = dict()
        context["year_groups"] = year_groups
        return self.renderer.render("index.html", context)

    def by_month(self, year, month_index, tweets):
        context = dict()
        context["year"] = year
        context["month_name"] = self.get_month_name(month_index)
        context["tweets"] = [HTMLTweet.from_tweet(t) for t in tweets]
        return self.renderer.render("by_month.html", context)

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


class JinjaRenderer(Renderer):
    def __init__(self):
        loader = jinja2.PackageLoader("twittback", "templates")
        self.env = jinja2.Environment(loader=loader)

    def render(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)


class FakeRenderer(Renderer):
    def __init__(self):
        self.calls = list()

    def render(self, template_name, context):
        self.calls.append((template_name, context))


class HTMLTweet(twittback.Tweet):

    @property
    def human_date(self):
        date = arrow.get(self.timestamp)
        return date.strftime("%Y %a %B %d %H:%m")

    def to_html(self):
        return self.text

    @classmethod
    def from_tweet(cls, tweet):
        # We need to call HTMLTweet.__init__() with
        # the required **kwargs:
        return cls(**vars(tweet))
