from twittback.repository import get_repository, NoSuchId
from twittback.client.twitter_client import get_twitter_client
import ui

repository = get_repository()
client = get_twitter_client()

timeline = open("dmerej-timeline.txt", "r")
to_add = list()
for line in timeline:
    id = int(line.split()[0])
    try:
        repository.tweet_by_id(id)
    except NoSuchId:
        ui.dot()
        tweet = client.get_tweet(id)
        to_add.append(tweet)

repository.add_tweets(to_add)
