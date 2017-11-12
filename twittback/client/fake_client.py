import twittback.client


class FakeClient(twittback.client.Client):
    def __init__(self):
        self.timeline = list()
        self._user = None
        self._following = list()

    def get_latest_tweets(self, since_id=None):
        if since_id:
            for tweet in self.timeline:
                if tweet.twitter_id <= since_id:
                    break
                yield tweet
        else:
            yield from self.timeline

    def set_user(self, user):
        self._user = user

    def user(self):
        return self._user

    def set_following(self, following):
        self._following = following

    def following(self):
        return self._following
