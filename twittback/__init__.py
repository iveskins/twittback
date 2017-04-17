import attr


@attr.s
class Tweet:
    def __init__(self):
        self.twitter_id = attr.ib()
        self.text = attr.ib()
