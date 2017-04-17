import abc

import twittback


class Storage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_latest_tweet(self):
        pass


class InMemoryStorage(Storage):
    def __init__(self):
        self.tweets = list()

    def get_latest_tweet(self):
        return self.tweets[-1]
