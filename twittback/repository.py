import abc
import sqlite3

from twittback.types import TweetSequence
import twittback
import twittback.config


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def all_tweets(self) -> TweetSequence:
        pass

    @abc.abstractmethod
    def latest_tweet(self) -> twittback.Tweet:
        pass

    @abc.abstractmethod
    def add(self, tweets: TweetSequence):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self.tweets = list()

    def add(self, tweets):
        self.tweets.extend(tweets)

    def all_tweets(self):
        return self.tweets

    def latest_tweet(self):
        if not self.tweets:
            return None
        return self.tweets[-1]


class SQLRepository(Repository):
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        script = """
            CREATE VIRTUAL TABLE IF NOT EXISTS tweets USING fts4 (
                twitter_id INTEGER NOT NULL,
                text VARCHAR(500) NOT NULL,
                timestamp INTEGER NOT NULL
                UNIQUE(twitter_id))
        """
        self.connection.executescript(script)
        self.connection.commit()

    def add(self, tweets):
        sql = """
            INSERT INTO tweets
                (twitter_id, text, timestamp) VALUES
                (?, ?, ?)
        """

        def yield_params():
            for tweet in tweets:
                yield self.to_row(tweet)

        self.connection.executemany(sql, yield_params())
        self.connection.commit()

    def latest_tweet(self):
        sql = """
            SELECT twitter_id, text, timestamp FROM tweets
                   ORDER BY twitter_id DESC
                   LIMIT 1
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
            return self.from_row(res)
        else:
            return None

    def all_tweets(self):
        sql = """
            SELECT twitter_id, text, timestamp FROM tweets
                   ORDER BY twitter_id ASC
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            yield self.from_row(row)

    @classmethod
    def from_row(cls, row):
        return twittback.Tweet(twitter_id=row["twitter_id"],
                               text=row["text"],
                               timestamp=row["timestamp"])

    @classmethod
    def to_row(cls, tweet):
        return (tweet.twitter_id, tweet.text, tweet.timestamp)


def get_sql_repository():
    config = twittback.config.read_config()
    db_path = config["db"]["path"]
    return SQLRepository(db_path)
