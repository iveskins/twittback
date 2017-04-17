import abc

import twitter

import twittback.config


MAX_TWEETS = 200


class Client(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_latest_tweets(self):
        return self.api.get_tweets_since(latest_id)


class TwitterClient(Client):
    def __init__(self, config):
        auth_dict = config["auth"]
        keys = ["token", "token_secret",
                "api_key", "api_secret"]
        auth_values = (auth_dict[key] for key in keys)
        auth = twitter.OAuth(*auth_values)
        self.api =  twitter.Twitter(auth=auth)
        self.screen_name = config["user"]["screen_name"]

    def get_latest_tweets(self):
        return self.api.statuses.user_timeline(
            screen_name=self.screen_name, count=MAX_TWEETS)


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
        print(tweet["id"], tweet["text"])


if __name__ == "__main__":
    main()
