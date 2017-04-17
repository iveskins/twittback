import html

import arrow
import twitter

import twittback.config
import twittback.client


MAX_TWEETS = 200


def get_twitter_client():
    config = twittback.config.read_config()
    client = TwitterClient(config)
    return client


class TwitterClient(twittback.client.Client):
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
            yield from_json(json_data)


def from_json(json_data):
    twitter_id = json_data["id"]
    text = json_data["text"]
    markdown = to_markdown(text, json_data)
    timestamp = to_timestamp(json_data["created_at"])
    return twittback.Tweet(twitter_id=twitter_id, text=markdown,
                            timestamp=timestamp)


def to_markdown(tweet_text, metadata):
    replacements = dict()
    entities = metadata["entities"]
    for start, end, replacement in process_urls(entities):
        replacements[start] = (end, replacement)
    for start, end, replacement in process_medias(entities):
        replacements[start] = (end, replacement)
    replaced_text = perform_replaces(tweet_text, replacements)
    return html.unescape(replaced_text)


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
    return "[%s](%s)" % (display_url, expanded_url)


def replacement_for_media(media):
    media_url = media["media_url_https"]
    return "![image](%s)" % (media_url)


def to_timestamp(created_at_str):
    date = arrow.Arrow.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")
    return date.timestamp


def main():
    client = get_twitter_client()
    latest_tweets = client.get_latest_tweets()
    import ipdb; ipdb.set_trace()
    for tweet in latest_tweets:
        print(tweet)


if __name__ == "__main__":
    main()
