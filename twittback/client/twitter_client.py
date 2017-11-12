import arrow
import twitter

import twittback.config
import twittback.client


def get_twitter_client():
    config = twittback.config.read_config()
    client = TwitterClient(config)
    return client


class TwitterClient(twittback.client.Client):
    def __init__(self, config):
        auth_dict = config["auth"]
        self.api = twitter.Api(
            consumer_key=auth_dict["api_key"],
            consumer_secret=auth_dict["api_secret"],
            access_token_key=auth_dict["token"],
            access_token_secret=auth_dict["token_secret"],
            tweet_mode="extended",
        )

        self.screen_name = config["user"]["screen_name"]

    def get_latest_tweets(self, since_id=None):
        for tweet in self.api.GetUserTimeline(
                screen_name=self.screen_name, since_id=since_id):
            yield convert_tweet(tweet)

    def user(self):
        user = self.api.GetUser(screen_name=self.screen_name)
        return convert_user(user)

    def following(self):
        friends = self.api.GetFriends()
        yield from (convert_user(friend) for friend in friends)


def convert_user(user):
    return twittback.User(name=user.name,
                          screen_name=user.screen_name,
                          location=user.location,
                          description=user.description)


def convert_tweet(tweet):
    # TODO: urls are exposed in the python-twitter models, but
    # without their indices, so we have to use the json returned
    # by the twitter API directly
    # pylint: disable=protected-access
    metadata = tweet._json
    twitter_id = tweet.id
    fixed_text = fix_text(tweet.full_text, metadata)
    timestamp = to_timestamp(tweet.created_at)
    return twittback.Tweet(twitter_id=twitter_id, text=fixed_text,
                           timestamp=timestamp)


def fix_text(text, metadata):
    replacements = dict()
    entities = metadata["entities"]
    for start, end, replacement in process_urls(entities):
        replacements[start] = (end, replacement)
    for start, end, replacement in process_medias(entities):
        replacements[start] = (end, replacement)
    replaced_text = perform_replaces(text, replacements)
    return replaced_text


def perform_replaces(text, replacements):
    res = ""
    i = 0
    while i < len(text):
        if i in replacements:
            end, replacement_str = replacements[i]
            res += replacement_str
            i = end
        else:
            res += text[i]
            i += 1
    return res


def process_urls(entities):
    urls = entities.get("urls", list())
    for url in urls:
        start, end = url["indices"]
        yield start, end, replacement_for_url(url)


def process_medias(entities):
    medias = entities.get("media", list())
    for media in medias:
        start, end = media["indices"]
        yield start, end, replacement_for_media(media)


def replacement_for_url(url):
    expanded_url = url["expanded_url"]
    display_url = url["display_url"]
    return '<a href="%s">%s</a>' % (expanded_url, display_url)


def replacement_for_media(media):
    media_url = media["media_url_https"]
    return '<a href="%s">see image</a>' % (media_url)


def to_timestamp(created_at_str):
    date = arrow.Arrow.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")
    return date.timestamp


def main():
    client = get_twitter_client()
    latest_tweets = client.get_latest_tweets()
    for tweet in latest_tweets:
        print(tweet)
    following = client.following()
    for user in following:
        print(user)


if __name__ == "__main__":
    main()
