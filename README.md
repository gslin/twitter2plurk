# twitter2plurk

This script will use Twitter API to read user's timeline, then post to Plurk.

## Setting up configuration

In `~/.config/twitter2plurk/config.ini`:

    [default]
    plurk_app_key = x
    plurk_app_secret = x
    plurk_token = x
    plurk_token_secret = x
    twitter_access_token = x
    twitter_access_token_secret = x
    twitter_consumer_key = x
    twitter_consumer_secret = x
    twitter_username = x

## Initializing sqlite3 database

    $ sqlite3 ~/.config/twitter2plurk/entry.sqlite3
    sqlite> CREATE TABLE entry (id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id TEXT UNIQUE, created_at INTEGER);

## License

Please check `LICENSE` file.
