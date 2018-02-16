# twitter2plurk

## Setuping configuration

In `~/.config/twitter2plurk/config.ini`:

    [default]
    plurk_app_key = x
    plurk_app_secret = x
    twitter_access_token = x
    twitter_access_token_secret = x
    twitter_consumer_key = x
    twitter_consumer_secret = x
    twitter_username = x

## Initializing sqlite3 database

    $ sqlite3 ~/.config/twitter2plurk/entry.sqlite3
    sqlite> CREATE TABLE entry (id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id STRING, created_at INTEGER);
