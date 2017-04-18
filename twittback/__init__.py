import attr
import arrow


@attr.s
class Tweet:
    twitter_id = attr.ib()
    text = attr.ib()
    timestamp = attr.ib(default=0)

    @property
    def human_date(self):
        date = arrow.get(self.timestamp)
        return date.strftime("%Y %a %B %d %H:%m")
