import argparse
import path
import json

import twittback.client
import twittback.storage


def import_tweets(base_path, storage):
    for json_path in base_path.files("*.json"):
        parsed_json = json.loads(json_path.text())
        storage.add(from_json(parsed_json))


def from_json(parsed_json):
    for json_data in parsed_json:
        yield twittback.client.TwitterClient.from_json(json_data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", type=path.Path)
    args = parser.parse_args()
    storage = twittback.storage.get_sql_storage()
    import_tweets(args.json_path, storage)


if __name__ == "__main__":
    main()
