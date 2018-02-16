# twitter2plurk

## Initializing sqlite3 database

    $ sqlite3 ~/.config/twitter2plurk/entry.sqlite3
    sqlite> CREATE TABLE entry (id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id STRING, created_at INTEGER);
