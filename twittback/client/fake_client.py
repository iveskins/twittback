import twittback.client


class FakeClient(twittback.client.Client):
    def __init__(self):
        self.timeline = list()

    def get_latest_tweets(self):
        return self.timeline
