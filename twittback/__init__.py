import attr


@attr.s
class Tweet:
    twitter_id = attr.ib()
    text = attr.ib()
    timestamp = attr.ib(default=0)


@attr.s
class User:
    screen_name = attr.ib()
    name = attr.ib()
    description = attr.ib()
    location = attr.ib()
