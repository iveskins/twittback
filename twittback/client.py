import abc
import typing

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
            yield self.to_tweet(json_data)

    @classmethod
    def to_tweet(cls, json_data):
        twitter_id = json_data["id"]
        text = json_data["text"]
        return twittback.Tweet(twitter_id=twitter_id, text=text)


class FakeClient(Client):
    def __init__(self):
        self.timeline = list()

    def get_latest_tweets(self):
        return self.timeline


def main():
    config = twittback.config.read_config()
    client = TwitterClient(config)
    latest_tweets = client.get_latest_tweets()
    for tweet in latest_tweets:
        print(tweet)


if __name__ == "__main__":
    main()
