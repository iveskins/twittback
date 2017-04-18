import attr


@attr.s
class Tweet:
    twitter_id = attr.ib()
    text = attr.ib()
    timestamp = attr.ib(default=0)
