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
                UNIQUE(twitter_id));
            CREATE TABLE IF NOT EXISTS user(
                screen_name VARCHAR(500) NOT NULL,
                name VARCHAR(500),
                description VARCHAR(500),
                location VARCHAR(500),
                UNIQUE(screen_name));
            CREATE TABLE IF NOT EXISTS following(
                screen_name VARCHAR(500) NOT NULL,
                name VARCHAR(500),
                description VARCHAR(500),
                location VARCHAR(500),
                UNIQUE(screen_name));
        """
        self.connection.executescript(script)
        self.connection.commit()

    def add_tweets(self, tweets):
        query = """
            INSERT INTO tweets
                (twitter_id, text, timestamp) VALUES
                (?, ?, ?)
        """

        def yield_params():
            for tweet in tweets:
                yield self.tweet_to_row(tweet)

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
            return self.tweet_from_row(last_row)
        else:
            return None

    def latest_tweets(self):
        query = """
            SELECT twitter_id, text, timestamp FROM tweets
                   ORDER BY twitter_id DESC
                   LIMIT 10
        """
        for row in self.query_many(query):
            yield self.tweet_from_row(row)

    def all_tweets(self):
        query = """
            SELECT twitter_id, text, timestamp FROM tweets
                   ORDER BY twitter_id ASC
        """
        for row in self.query_many(query):
            yield self.tweet_from_row(row)

    def num_tweets(self):
        query = """
            SELECT count(twitter_id) FROM tweets
        """
        result = self.query_one(query)
        return result[0]

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
            yield self.tweet_from_row(row)

    def date_range(self):
        start_row = self.query_one("SELECT min(timestamp) FROM tweets")
        end_row = self.query_one("SELECT max(timestamp) FROM tweets")
        return (start_row[0], end_row[0])

    def tweet_by_id(self, twitter_id):
        query = """
            SELECT twitter_id, text, timestamp FROM tweets
                WHERE twitter_id=?
        """
        row = self.query_one(query, (twitter_id,))
        if not row:
            raise NoSuchId(twitter_id)
        return self.tweet_from_row(row)

    def set_text(self, twitter_id, text):
        query = """
            UPDATE tweets
                SET text = ?
                WHERE twitter_id = ?
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (text, twitter_id))
        self.connection.commit()

    def search_tweet(self, pattern):
        full_pattern = "%" + pattern + "%"
        query = """
            SELECT twitter_id, text, timestamp FROM tweets
                WHERE text MATCH ?
                ORDER BY twitter_id ASC
        """
        for row in self.query_many(query, full_pattern):
            yield self.tweet_from_row(row)

    @classmethod
    def tweet_from_row(cls, row):
        return twittback.Tweet(twitter_id=row["twitter_id"],
                               text=row["text"],
                               timestamp=row["timestamp"])

    @classmethod
    def tweet_to_row(cls, tweet):
        return (tweet.twitter_id, tweet.text, tweet.timestamp)

    def user(self):
        query = "SELECT screen_name, name, description, location FROM user"
        row = self.query_one(query)
        return self.user_from_row(row)

    def save_user(self, user):
        query = """
            INSERT OR REPLACE INTO user
                (screen_name, name, description, location) VALUES
                (?, ?, ?, ?)
        """
        params = self.user_to_row(user)
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()

    @classmethod
    def user_from_row(cls, row):
        return twittback.User(screen_name=row["screen_name"],
                              name=row["name"],
                              description=row["description"],
                              location=row["location"])

    @classmethod
    def user_to_row(cls, user):
        return (user.screen_name, user.name,
                user.description, user.location)

    def following(self):
        query = """
            SELECT screen_name, name, description, location
            FROM following
        """
        rows = self.query_many(query)
        for row in rows:
            yield self.user_from_row(row)

    def save_following(self, following):
        self.connection.execute("DELETE FROM following")
        self.connection.commit()

        query = """
            INSERT OR REPLACE INTO following
                (screen_name, name, description, location) VALUES
                (?, ?, ?, ?)
        """

        def yield_params():
            for user in following:
                yield self.user_to_row(user)

        self.connection.executemany(query, yield_params())
        self.connection.commit()

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
        return "<Repository in %s>" % self.db_path


def get_repository():
    config = twittback.config.read_config()
    return Repository(config["db"]["path"])
