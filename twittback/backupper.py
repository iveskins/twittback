class Backupper:
    def __init__(self, *, client, storage):
        self.client = client
        self.storage = storage

    def yield_latest_tweets(self):
        latest_tweet = self.storage.latest_tweet()
        for tweet in self.client.get_latest_tweets():
            if latest_tweet and (tweet.twitter_id <= latest_tweet.twitter_id):
                    break
            yield tweet

    def backup(self):
        latest_tweets = self.yield_latest_tweets()
        self.storage.add(reversed(list(latest_tweets)))


def main():
    import twittback.client
    import twittback.storage

    client = twittback.client.get_twitter_client()
    storage = twittback.storage.get_sql_storage()
    backupper = Backupper(client=client, storage=storage)
    backupper.backup()


if __name__ == "__main__":
    main()
