from twittback import ui


class Backupper:
    def __init__(self, *, client, storage):
        self.client = client
        self.storage = storage

    def yield_latest_tweets(self):
        latest_tweet = self.storage.latest_tweet()
        ui.info("Feching latest tweets", ui.ellipsis)
        tweets = self.client.get_latest_tweets()
        for tweet in tweets:
            if latest_tweet and (tweet.twitter_id <= latest_tweet.twitter_id):
                break
            yield tweet

    def backup(self):
        latest_tweets = self.yield_latest_tweets()
        to_add = list(latest_tweets)
        self.storage.add(reversed(to_add))
        if to_add:
            ui.info("Stored", len(to_add), "new tweet(s)", ui.check)
        else:
            ui.info("No new tweets", ui.check)


def main():
    import twittback.client.twitter_client
    import twittback.storage

    client = twittback.client.twitter_client.get_twitter_client()
    storage = twittback.storage.get_sql_storage()
    backupper = Backupper(client=client, storage=storage)
    backupper.backup()


if __name__ == "__main__":
    main()
