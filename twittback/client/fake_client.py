import twittback.client


class FakeClient(twittback.client.Client):
    def __init__(self):
        self.timeline = list()
        self._user = None

    def get_latest_tweets(self):
        return self.timeline

    def set_user(self, user):
        self._user = user

    def user(self):
        return self._user
