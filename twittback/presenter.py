import abc
import itertools

import arrow
import jinja2


class Renderer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def render(self, template_name: str, **context) -> str:
        pass


class HTMLPresenter:
    def __init__(self, renderer=None):
        if renderer:
            self.renderer = renderer
        else:
            self.renderer = JinjaRenderer()

    def gen_index(self, start_timestamp, end_timestamp):
        dates = list()
        date = arrow.get(start_timestamp)
        while date <= arrow.get(end_timestamp):
            dates.append(date)
            date = date.shift(months=1)
        context = dict()

        year_groups = list()

        def key(date):
            return date.year

        for year, group in itertools.groupby(dates, key):
            month_names = [get_month_name(x.month) for x in group]
            year_groups.append((str(year), month_names))

        context["year_groups"] = year_groups
        return self.renderer.render("index.html", context)


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


def get_month_name(month_number):
    """
    >>> get_month_short_name(4)
    'April'

    """
    date = arrow.Arrow(year=2000, day=1, month=month_number)
    return date.strftime("%B")


def main():
    renderer = JinjaRenderer()
    year_groups = [
        ("2017", ("10", "11", "12")),
        ("2018", ("01", "02")),
    ]
    out = renderer.render("index.html", {"year_groups" : year_groups})
    print(out)


if __name__ == "__main__":
    main()
