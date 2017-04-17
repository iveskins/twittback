class Backupper:
    def __init__(self, *, client, storage):
        self.client = client
        self.storage = storage

    def yield_latest_tweets(self):
        latest_tweet = self.storage.latest_tweet()
        latest_id = latest_tweet.twitter_id
        for tweet in self.client.get_latest_tweets():
            if tweet.twitter_id <= latest_id:
                break
            yield tweet

    def backup(self):
        latest_tweets = self.yield_latest_tweets()
        self.storage.add(reversed(list(latest_tweets)))
