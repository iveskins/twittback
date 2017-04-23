import abc
import twittback
from twittback.types import TweetSequence


class Client(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_latest_tweets(self) -> TweetSequence:
        pass

    @abc.abstractmethod
    def user(self) -> twittback.User:
        pass
