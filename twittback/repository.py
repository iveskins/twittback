import sqlite3

import arrow

import twittback
import twittback.config


class NoSuchId(Exception):
    def __init__(self, twitter_id):
        super().__init__(twitter_id)
        self.twitter_id = twitter_id


class Repository:
    def __init__(self, db_path):
        self.db_path = db_path
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
        query = """
            INSERT INTO tweets
                (twitter_id, text, timestamp) VALUES
                (?, ?, ?)
        """

        def yield_params():
            for tweet in tweets:
                yield self.to_row(tweet)

        self.connection.executemany(query, yield_params())
        self.connection.commit()

    def latest_tweet(self):
        query = """
            SELECT twitter_id, text, timestamp FROM tweets
                   ORDER BY twitter_id DESC
                   LIMIT 1
        """
        last_row = self.query_one(query)
        if last_row:
            return self.from_row(last_row)
        else:
            return None

    def all_tweets(self):
        query = """
            SELECT twitter_id, text, timestamp FROM tweets
                   ORDER BY twitter_id ASC
        """
        for row in self.query_many(query):
            yield self.from_row(row)

    def tweets_for_month(self, year, month_number):
        start_date = arrow.Arrow(year, month_number, 1)
        end_date = start_date.shift(months=+1)

        query = """
           SELECT twitter_id, text, timestamp FROM tweets
                WHERE (timestamp > ?) AND (timestamp < ?)
                ORDER BY twitter_id ASC
        """
        for row in self.query_many(query,
                                   start_date.timestamp,
                                   end_date.timestamp):
            yield self.from_row(row)

    def date_range(self):
        start_row = self.query_one("SELECT min(timestamp) FROM tweets")
        end_row = self.query_one("SELECT max(timestamp) FROM tweets")
        return (start_row[0], end_row[0])

    def get_by_id(self, twitter_id):
        query = """
            SELECT twitter_id, text, timestamp FROM tweets
                WHERE twitter_id=?
        """
        row = self.query_one(query, (twitter_id,))
        if not row:
            raise NoSuchId(twitter_id)
        return self.from_row(row)

    def search(self, pattern):
        full_pattern = "%" + pattern + "%"
        query = """
            SELECT twitter_id, text, timestamp FROM tweets
                WHERE text MATCH ?
                ORDER BY twitter_id ASC
        """
        for row in self.query_many(query, full_pattern):
            yield self.from_row(row)

    @classmethod
    def from_row(cls, row):
        return twittback.Tweet(twitter_id=row["twitter_id"],
                               text=row["text"],
                               timestamp=row["timestamp"])

    @classmethod
    def to_row(cls, tweet):
        return (tweet.twitter_id, tweet.text, tweet.timestamp)

    def query_one(self, query, *args):
        cursor = self.connection.cursor()
        cursor.execute(query, *args)
        res = cursor.fetchone()
        if res:
            return res
        else:
            return None

    def query_many(self, query, *args):
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        yield from cursor.fetchall()

    def __str__(self):
        return f"<Repository in {self.db_path}>"


def get_repository():
    db_path = twittback.config.get_db_path()
    return Repository(db_path)
