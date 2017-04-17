import abc
import typing

import arrow
import twitter

import twittback.config


MAX_TWEETS = 200


class Client(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_latest_tweets(self) -> typing.List[twittback.Tweet]:
        pass


class TwitterClient(Client):
    def __init__(self, config):
        auth_dict = config["auth"]
        keys = ["token", "token_secret",
                "api_key", "api_secret"]
        auth_values = (auth_dict[key] for key in keys)
        auth = twitter.OAuth(*auth_values)
        self.api = twitter.Twitter(auth=auth)
        self.screen_name = config["user"]["screen_name"]

    def get_latest_tweets(self):
        for json_data in self.api.statuses.user_timeline(
                screen_name=self.screen_name, count=MAX_TWEETS):
            yield self.from_json(json_data)

    @classmethod
    def from_json(cls, json_data):
        twitter_id = json_data["id"]
        text = json_data["text"]
        timestamp = cls.to_timestamp(json_data["created_at"])
        return twittback.Tweet(twitter_id=twitter_id, text=text,
                               timestamp=timestamp)

    @classmethod
    def to_timestamp(cls, created_at_str):
        date = arrow.Arrow.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")
        return date.timestamp



class FakeClient(Client):
    def __init__(self):
        self.timeline = list()

    def get_latest_tweets(self):
        return self.timeline


def get_twitter_client():
    config = twittback.config.read_config()
    client = TwitterClient(config)
    return client


def main():
    client = get_twitter_client()
    latest_tweets = client.get_latest_tweets()
    for tweet in latest_tweets:
        print(tweet)


if __name__ == "__main__":
    main()
