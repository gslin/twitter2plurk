#!/usr/bin/env python3

import configparser
import plurk_oauth
import os
import sqlite3
import twitter

class Twitter2Plurk(object):
    def __init__(self):
        pass

    def start(self):
        home = os.environ['HOME']
        f_conf = '{}/.config/twitter2plurk/config.ini'.format(home)
        f_db = '{}/.config/twitter2plurk/entry.sqlite3'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        t_ak = c['default']['twitter_access_token']
        t_as = c['default']['twitter_access_token_secret']
        t_ck = c['default']['twitter_consumer_key']
        t_cs = c['default']['twitter_consumer_secret']
        t_user = c['default']['twitter_username']

        p_ak = c['default']['plurk_app_key']
        p_as = c['default']['plurk_app_secret']

        t = twitter.Api(access_token_key=t_ak, access_token_secret=t_as, consumer_key=t_ck, consumer_secret=t_cs)
        p = plurk_oauth.PlurkAPI(p_ak, p_as)
        s = sqlite3.connect(f_db)

        for status in sorted(list(t.GetUserTimeline(screen_name=t_user)), key=lambda x: x.id):
            text = status.text
            for u in status.urls:
                text = text.replace(u.url, u.expanded_url)

if '__main__' == __name__:
    t = Twitter2Plurk()
    t.start()
