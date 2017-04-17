import abc
from twittback.types import TweetSequence


class Client(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_latest_tweets(self) -> TweetSequence:
        pass
