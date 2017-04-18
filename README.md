Twittback
=========

Nice and user-friendly backup of your twitter timeline


# Features

* Clean code
* Incremental backup of your timeline
* Full-text search
* Old school pagination
* Chronological order
* No javascript

# Installation

* Create an app on https://apps.twitter.com
* Create `~/.config/twittback.yml`:

```yaml
auth:
  api_key: <api key>
  api_secret: <api secret>

  token: <token>
  token_secret: <token secret>

user:
  screen_name: <screen name>

db:
  path: <path>

server:
  port: <port>
  debug: true
```

* `pip3 install -e . --user`

*  Run `twittback` to fetch your latests tweets (can be done
   in a `cron` job or a `systemd` timer for instance)

* Run the server with `python3 twittback/server.py`


# Screenshots

## Welcome page

![index screenshot](scrot/index.png?raw=true)

## Detailed view

![by month screenshot](scrot/by_month.png?raw=true)

# Live instance

https://dmerej.info/twittback
