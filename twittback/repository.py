import arrow
from path import Path
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import twittback
import twittback.config


class NoSuchId(Exception):
    def __init__(self, twitter_id):
        super().__init__(twitter_id)
        self.twitter_id = twitter_id


Base = declarative_base()


class Tweet(Base):
    __tablename__ = "tweets"

    twitter_id = Column(Integer, primary_key=True)
    text = Column(Text)
    timestamp = Column(Integer)

    def to_tweet(self):
        return twittback.Tweet(
            twitter_id=self.twitter_id, text=self.text, timestamp=self.timestamp
        )

    @classmethod
    def from_(cls, tweet):
        return cls(
            twitter_id=tweet.twitter_id, text=tweet.text, timestamp=tweet.timestamp
        )


class _UserModel:
    screen_name = Column(String, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    location = Column(Text)

    @classmethod
    def from_(cls, user):
        return cls(
            screen_name=user.screen_name,
            name=user.name,
            description=user.description,
            location=user.location,
        )

    def to_user(self):
        return twittback.User(
            screen_name=self.screen_name,
            description=self.description,
            location=self.location,
            name=self.name,
        )


class User(Base, _UserModel):
    __tablename__ = "user"


class Following(Base, _UserModel):
    __tablename__ = "following"


class Repository:
    def __init__(self, db_path):
        self.db_path = db_path
        connect_string = "sqlite:///" + db_path
        engine = create_engine(connect_string)
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()
        if self.db_path == ":memory:" or not self.db_path.exists():
            self.init_db(engine)

    def query(self, *args, **kwargs):
        return self.session.query(*args, **kwargs)

    def add(self, *args, **kwargs):
        return self.session.add(*args, **kwargs)

    def commit(self):
        return self.session.commit()

    @classmethod
    def init_db(cls, engine):
        Base.metadata.create_all(engine)

    def add_tweets(self, tweets):
        for tweet in tweets:
            to_add = Tweet.from_(tweet)
            self.add(to_add)

        self.commit()

    def latest_tweet(self):
        latest_tweets = self.latest_tweets()
        try:
            latest_tweet = next(latest_tweets)
            return latest_tweet
        except StopIteration:
            return None

    def latest_tweets(self):
        query = self.query(Tweet).order_by(Tweet.twitter_id.desc())
        for entry in query:
            yield entry.to_tweet()

    def all_tweets(self):
        query = self.query(Tweet).order_by(Tweet.twitter_id.asc())
        for entry in query:
            yield entry.to_tweet()

    def num_tweets(self):
        return self.query(Tweet).count()

    def tweets_for_month(self, year, month_number):
        start_date = arrow.Arrow(year, month_number, 1)
        end_date = start_date.shift(months=+1)

        query = (
            self.query(Tweet)
            .order_by(Tweet.twitter_id.asc())
            .filter(start_date.timestamp < Tweet.timestamp)
            .filter(Tweet.timestamp < end_date.timestamp)
        )
        for entry in query:
            yield entry.to_tweet()

    def date_range(self):
        start_row = self.query(func.min(Tweet.timestamp)).scalar()
        end_row = self.query(func.max(Tweet.timestamp)).scalar()
        return (start_row, end_row)

    def tweet_by_id(self, twitter_id):
        entry = self._tweet_entry_by_id(twitter_id)
        return entry.to_tweet()

    def set_text(self, twitter_id, text):
        entry = self._tweet_entry_by_id(twitter_id)
        entry.text = text
        self.commit()

    def search_tweet(self, pattern):
        full_pattern = "%" + pattern + "%"
        query = self.query(Tweet).filter(Tweet.text.ilike(full_pattern))
        for entry in query:
            yield entry.to_tweet()

    def _tweet_entry_by_id(self, twitter_id):
        entry = self.query(Tweet).filter(Tweet.twitter_id == twitter_id).one_or_none()
        if not entry:
            raise NoSuchId(twitter_id)
        return entry

    def user(self):
        entry = self.query(User).one()
        return entry.to_user()

    def save_user(self, user):
        self.query(User).delete()

        entry = User.from_(user)
        entry.screen_name = user.screen_name
        entry.name = user.name
        entry.description = user.description
        entry.location = user.location

        self.add(entry)
        self.commit()

    def following(self):
        return self._get_related_users(Following)

    def save_following(self, following):
        return self._set_related_users(Following, following)

    def _get_related_users(self, userClass):
        for entry in self.query(userClass).all():
            yield entry.to_user()

    def _set_related_users(self, userClass, users):
        self.query(userClass).delete()
        for user in users:
            self.add(userClass.from_(user))
        self.commit()


def get_repository():
    config = twittback.config.read_config()
    db_path = Path(config["db"]["path"])
    db_path.parent.makedirs_p()
    return Repository(db_path)
