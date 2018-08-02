import abc
import twittback
from twittback.types import TweetSequence, UserSequence


class Client(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_latest_tweets(self, since_id=None) -> TweetSequence:
        pass

    @abc.abstractmethod
    def user(self) -> twittback.User:
        pass

    @abc.abstractmethod
    def following(self) -> UserSequence:
        pass

    @abc.abstractmethod
    def followers(self) -> UserSequence:
        pass
