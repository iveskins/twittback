import argparse
import os
import subprocess
import sys
import tempfile

import twittback.repository


def edit(repository, twitter_id):
    try:
        tweet = repository.tweet_by_id(twitter_id)
    except twittback.repository.NoSuchId as e:
        sys.exit("No such id: %s" % twitter_id)
    _, path = tempfile.mkstemp()
    with open(path, "w") as stream:
        stream.write(tweet.text)
    process = subprocess.run(["nvim", path])
    if process.returncode != 0:
        os.remove(path)
        sys.exit("Edit failed")
    else:
        with open(path, "r") as stream:
            new_text = stream.read()
            repository.set_text(twitter_id, new_text)
            os.remove(path)


def main():
    repository = twittback.repository.get_repository()
    parser = argparse.ArgumentParser()
    parser.add_argument("twitter_id", type=int)
    args = parser.parse_args()
    edit(repository, args.twitter_id)


if __name__ == "__main__":
    main()
