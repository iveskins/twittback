class Backupper:
    def __init__(self, *, client, repository):
        self.client = client
        self.repository = repository

    def yield_latest_tweets(self):
        latest_tweet = self.repository.latest_tweet()
        print("Feching latest tweets ...")
        tweets = self.client.get_latest_tweets()
        for tweet in tweets:
            if latest_tweet and (tweet.twitter_id <= latest_tweet.twitter_id):
                break
            yield tweet

    def backup(self):
        self.save_user_data()
        self.save_latest_tweets()

    def save_user_data(self):
        print("Saving user data ...", end=" ", flush=True)
        user = self.client.user()
        self.repository.save_user(user)
        print("done")

    def save_latest_tweets(self):
        latest_tweets = self.yield_latest_tweets()
        to_add = list(latest_tweets)
        self.repository.add_tweets(reversed(to_add))
        if to_add:
            print("Stored", len(to_add), "new tweet(s)")
        else:
            print("No new tweets")


def main():
    import twittback.client.twitter_client
    import twittback.repository

    client = twittback.client.twitter_client.get_twitter_client()
    repository = twittback.repository.get_repository()
    backupper = Backupper(client=client, repository=repository)
    backupper.backup()


if __name__ == "__main__":
    main()
