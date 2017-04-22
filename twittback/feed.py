import arrow
import feedgenerator

import twittback.presenter


class FeedGenerator():
    def __init__(self, config):
        self.site_url = config["server"]["site_url"]
        feed_self_url = "%s/feed.atom" % self.site_url
        self.feed_generator = feedgenerator.Atom1Feed(
                title="Twittback",
                description="Latest tweets",
                link=self.site_url,
                feed_url=feed_self_url)

    def gen_feed(self, latest_tweets):

        for tweet in latest_tweets:
            self.add_tweet_to_feed(tweet)

        return self.feed_generator.writeString("utf-8")

    def add_tweet_to_feed(self, tweet):
        html_tweet = twittback.presenter.HTMLTweet.from_tweet(tweet)
        date = arrow.get(tweet.timestamp)
        permalink = "%s/view/%d" % (self.site_url, tweet.twitter_id)
        entry_id = date
        description = html_tweet.html
        self.feed_generator.add_item(
                title=entry_id,
                link=permalink,
                description=description,
                pubdate=date,
                updated=date,
        )
